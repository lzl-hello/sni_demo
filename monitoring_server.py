# monitoring_server.py

import eventlet
eventlet.monkey_patch()

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
import queue

# 配置常量（请根据实际情况修改）
__MSG_TRANSFER_EVENT__ = 'update'  # 事件名称
__BOT_NAMESPACE__ = '/'  # 命名空间，默认为根命名空间
__SOCKET_PORT__ = 5000  # 服务器端口
__SOCKET_HOST__ = '0.0.0.0'  # 服务器主机

# 初始化 Flask 应用和 SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')  # 使用 eventlet 作为异步模式

# 设置日志记录器
logger = logging.getLogger('monitoring_server')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个文件处理器，日志文件名为 'monitoring.log'
log_file = './log/monitoring.log'
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')  # 5MB per file, keep 5 backups
file_handler.setLevel(logging.DEBUG)  # 设置文件处理器的日志级别

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 添加文件处理器到记录器
logger.addHandler(file_handler)

# 移除根记录器的 StreamHandler，避免日志输出到控制台
logging.getLogger().handlers = [handler for handler in logging.getLogger().handlers if not isinstance(handler, logging.StreamHandler)]

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

# 维护一个全局消息队列
msg_queue = queue.Queue()

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

def flush_queue():
    while not msg_queue.empty():
        msg = msg_queue.get()
        try:
            # 执行业务发送逻辑，此处可以正确获取上下文
            socketio.emit(__MSG_TRANSFER_EVENT__, msg, namespace=__BOT_NAMESPACE__)
            logger.debug(f"发送消息到客户端: {msg}")
        except Exception as e:
            logger.error(f"发送消息失败: {e}")

def handle_queue():
    while True:
        flush_queue()
        socketio.sleep(1)  # 使用 socketio.sleep 而不是 time.sleep

@socketio.on("disconnect", namespace=__BOT_NAMESPACE__)
def disconnect():
    global is_connect
    is_connect = False
    logger.info("connect disabled!!")

@socketio.on("connect", namespace=__BOT_NAMESPACE__)
def connect():
    global is_connect
    is_connect = True
    logger.info("connect enabled!")
    # 启动后台任务处理消息队列
    socketio.start_background_task(target=handle_queue)

def background_thread():
    while True:
        try:
            # 读取子线程统计数据
            worker_data = read_worker_csv()
            # 如果有新数据，则将数据放入消息队列
            if worker_data:
                emit_data = {
                    'workers': sanitize_data(worker_data),
                    'history': sanitize_data(defaultdict_to_dict(history_worker_data))
                }
                msg_queue.put(emit_data)
                logger.debug(f"数据已入队: {emit_data}")
        except Exception as e:
            logger.error(f"后台线程出现异常: {e}")
        time.sleep(READ_INTERVAL)

if __name__ == '__main__':
    # 启动后台线程
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    logger.debug("后台线程已启动。")
    # 运行 Flask 应用
    socketio.run(app, host=__SOCKET_HOST__, port=__SOCKET_PORT__, debug=True, use_reloader=False)
