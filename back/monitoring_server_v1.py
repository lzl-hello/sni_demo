# monitoring_server.py

import atexit
import csv
from logging.handlers import RotatingFileHandler
import os
import subprocess
import threading
import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import time
import logging
from collections import defaultdict
import queue


# 配置常量
__MSG_TRANSFER_EVENT__ = 'update'
__BOT_NAMESPACE__ = '/'
__SOCKET_PORT__ = 5000
__SOCKET_HOST__ = '0.0.0.0'

# 初始化 Flask 应用和 SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# 设置日志记录器
logger = logging.getLogger('monitoring_server')
logger.setLevel(logging.DEBUG)

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

# 全局变量
is_monitoring = False
# 主 CSV 文件路径
MAIN_CSV = './output/network_traffic.csv'

WORKER_CSV_DIR = './output/'

READ_INTERVAL = 5

last_main_csv_line = 0

last_worker_csv_lines = {}

history_worker_data = defaultdict(lambda: {'packet_count': [], 'bytes': []})

msg_queue = queue.Queue()

@app.route('/')
def index():
    logger.debug("Rendering index.html")
    return render_template('index.html')

process = None 

@app.route('/start_monitor', methods=['POST'])
def start_monitor():
    """启动监控"""
    global is_monitoring, process
    if not is_monitoring:
        is_monitoring = True
        # 启动另一个 Python 文件作为子进程
        process = subprocess.Popen(['python', './network_capture.py'])
        logger.info("------ Started network_capture.py. ------")
        print(process)
    return jsonify({"status": "started"})

@app.route('/stop_monitor', methods=['POST'])
def stop_monitor():
    """停止监控"""
    global is_monitoring, process
    if is_monitoring and process:
        # 终止子进程
        process.terminate()
        process = None  # 清空 process 引用
    is_monitoring = False
    logger.info("------ End network_capture.py. ------")
    return jsonify({"status": "stopped"})

def read_worker_csv():
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
    """后台线程，用于模拟数据读取并通过Socket.IO发送"""
    # global is_monitoring
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
    """处理消息队列，将消息发送给前端"""
    while True:
        while not msg_queue.empty():
            msg = msg_queue.get()
            socketio.emit(__MSG_TRANSFER_EVENT__, msg, namespace=__BOT_NAMESPACE__)
            logger.debug(f"发送消息到客户端: {msg}")
        socketio.sleep(1)

@socketio.on("connect", namespace=__BOT_NAMESPACE__)
def connect():
    logger.info("Client connected")
    socketio.start_background_task(target=handle_queue)

@socketio.on("disconnect", namespace=__BOT_NAMESPACE__)
def disconnect():
    logger.info("Client disconnected")

def cleanup():
    """在服务器结束时终止子进程"""
    global process
    if process:
        process.terminate()
        logger.info("Network_capture.py terminated during server shutdown.")
        process = None

# 注册 cleanup 函数，使其在程序退出时执行
atexit.register(cleanup)


if __name__ == '__main__':

    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    
    thread.start()
    logger.debug("后台线程已启动。")
    
    socketio.run(app, host=__SOCKET_HOST__, port=__SOCKET_PORT__)
    
