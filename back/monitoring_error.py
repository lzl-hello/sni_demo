# monitoring_server.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import csv
import time
import threading
import os
import logging
from collections import defaultdict
import json
from logging.handlers import RotatingFileHandler
import eventlet

eventlet.monkey_patch()

# 初始化 Flask 应用和 SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')  # 使用 eventlet 作为异步模式

# 设置日志记录器
logger = logging.getLogger('monitoring_server')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个文件处理器，日志文件名为 'monitoring.log'
log_file = 'monitoring.log'
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5,
                                   encoding='utf-8')  # 5MB per file, keep 5 backups
file_handler.setLevel(logging.DEBUG)  # 设置文件处理器的日志级别

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 添加文件处理器到记录器
logger.addHandler(file_handler)

# 移除根记录器的 StreamHandler，避免日志输出到控制台
logging.getLogger().handlers = [handler for handler in logging.getLogger().handlers if
                                not isinstance(handler, logging.StreamHandler)]

# 主 CSV 文件路径
MAIN_CSV = './output/network_traffic.csv'

# 子线程统计 CSV 文件所在目录
WORKER_CSV_DIR = './output/'

# 读取 CSV 的时间间隔（秒）
READ_INTERVAL = 5

# 存储上次读取的主 CSV 行数
last_main_csv_line = 0

# 存储每个子线程的上次读取行数
last_worker_csv_lines = {}

# 存储历史数据
history_worker_data = defaultdict(lambda: {'packet_count': [], 'bytes': []})


@app.route('/')
def index():
    logger.debug("Rendering index.html")
    return render_template('index.html')  # 确保 index.html 在 templates/ 目录下


def read_main_csv():
    global last_main_csv_line
    data = []
    if os.path.isfile(MAIN_CSV):
        try:
            with open(MAIN_CSV, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= last_main_csv_line:
                        data.append(row)
                last_main_csv_line = i + 1 if 'i' in locals() else 0
            logger.debug(f"读取主 CSV 数据: {data}")
        except Exception as e:
            logger.error(f"读取主 CSV 失败: {e}")
    else:
        logger.warning(f"主 CSV 文件不存在: {MAIN_CSV}")
    return data


def read_worker_csv():
    data = {}
    for filename in os.listdir(WORKER_CSV_DIR):
        if filename.endswith('_statistics.csv'):
            app_name = filename.replace('_statistics.csv', '')
            filepath = os.path.join(WORKER_CSV_DIR, filename)
            if app_name not in last_worker_csv_lines:
                last_worker_csv_lines[app_name] = 0
            rows = []
            try:
                with open(filepath, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for i, row in enumerate(reader):
                        if i >= last_worker_csv_lines[app_name]:
                            rows.append(row)
                    last_worker_csv_lines[app_name] = i + 1 if 'i' in locals() else 0
                if rows:
                    latest_row = rows[-1]
                    app_name_clean = app_name.replace('_', ' ').strip()  # 恢复应用名称中的空格并去除多余空格
                    data[app_name_clean] = latest_row
                    # 更新历史数据
                    try:
                        history_worker_data[app_name_clean]['packet_count'].append(int(latest_row['packet_count']))
                        history_worker_data[app_name_clean]['bytes'].append(int(latest_row['bytes']))
                    except ValueError as ve:
                        logger.error(f"转换数据错误 - 应用: {app_name_clean}, 错误: {ve}, 数据: {latest_row}")
                    logger.debug(f"读取子线程 CSV 数据 - {app_name_clean}: {latest_row}")
            except Exception as e:
                logger.error(f"读取子线程 CSV 文件失败: {filepath}, 错误: {e}")
    return data


def sanitize_data(data):
    """递归地清理数据中的特殊字符"""
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    elif isinstance(data, str):
        return data.replace('\n', ' ').replace('\r', ' ').strip()
    else:
        return data


def defaultdict_to_dict(d):
    """递归地将 defaultdict 转换为 dict"""
    if isinstance(d, defaultdict):
        d = {k: defaultdict_to_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        d = [defaultdict_to_dict(item) for item in d]
    elif isinstance(d, dict):
        d = {k: defaultdict_to_dict(v) for k, v in d.items()}
    return d


def background_thread():
    while True:
        try:
            # 读取主 CSV 数据
            main_data = read_main_csv()
            # 读取子线程统计数据
            worker_data = read_worker_csv()
            # 如果有新数据，则通过 SocketIO 发送给客户端
            if main_data or worker_data:
                # 清理数据
                sanitized_main = sanitize_data(main_data)
                sanitized_workers = sanitize_data(worker_data)
                sanitized_history = sanitize_data(defaultdict_to_dict(history_worker_data))

                emit_data = {
                    'main': sanitized_main,
                    'workers': sanitized_workers,
                    'history': sanitized_history
                }

                # 确保数据可以被 JSON 序列化
                try:
                    json_data = json.dumps(emit_data, ensure_ascii=False)
                    logger.debug(f"发送数据到客户端: {json_data}")
                    socketio.emit('update', emit_data)
                except TypeError as te:
                    logger.error(f"JSON 序列化失败: {te}, 数据: {emit_data}")

            # 发送测试数据
            test_emit_data = {
                'main': [],
                'workers': {
                    'TestApp': {
                        'flow_tuple': '1.1.1.1:443->2.2.2.2:80',
                        'app_name': 'TestApp',
                        'packet_count': '100',
                        'bytes': '50000',
                        'current_packet_size': '100',
                        'time_since_last_packet': '0.5'
                    }
                },
                'history': {
                    'TestApp': {
                        'packet_count': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                        'bytes': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
                    }
                }
            }
            logger.debug(f"发送测试数据到客户端: {json.dumps(test_emit_data, ensure_ascii=False)}")
            socketio.emit('update', test_emit_data)

        except Exception as e:
            logger.error(f"后台线程出现异常: {e}")
        time.sleep(READ_INTERVAL)


@socketio.on('connect')
def handle_connect():
    logger.info('客户端已连接')


@socketio.on('disconnect')
def handle_disconnect():
    logger.info('客户端已断开连接')


if __name__ == '__main__':
    # 启动后台线程
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    logger.debug("后台线程已启动。")
    # 运行 Flask 应用
    socketio.run(app, host='0.0.0.0', port=5000)
