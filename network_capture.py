# network_capture.py
from doctest import debug

import pyshark
import pandas as pd
import datetime
import logging
import matplotlib.pyplot as plt
import asyncio
import nest_asyncio
import signal
import sys
import threading
import time
import os
import csv
from queue import Queue, Empty
from collections import defaultdict
from matplotlib import font_manager
from pyshark.capture.capture import TSharkCrashException

from db_classify_traffic import classify_traffic_from_db
from worker_thread import WorkerThread

# 确保目录存在
os.makedirs('./log/', exist_ok=True)
os.makedirs('./output/', exist_ok=True)

# 设置主模块的日志记录器
logger = logging.getLogger('network_capture')
logger.setLevel(logging.DEBUG)

# 创建文件处理器
network_handler = logging.FileHandler('./log/network_capture.log')
network_handler.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
network_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(network_handler)
logger.propagate = False  # 防止日志传播到根记录器

logger.debug("必要的目录已创建或已存在。")

# 解决嵌套事件循环问题
nest_asyncio.apply()

# 定义要捕获的网络接口，例如 'eth0'、'Wi-Fi' 等
INTERFACE = r"\Device\NPF_{382B8322-0D2A-47B8-B366-CF6FD3C226C0}"  # 根据实际接口更新

# 输出CSV文件路径
OUTPUT_CSV = './output/network_traffic.csv'

# 初始化CSV写入队列
csv_queue = Queue()

# 定义CSV写入线程
def csv_writer(queue, csv_file, columns, stop_event):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(csv_file).st_size == 0:
            writer.writerow(columns)  # 写入表头
            logger.debug(f"写入CSV表头: {columns}")
        while not stop_event.is_set() or not queue.empty():
            try:
                row = queue.get(timeout=1)
                writer.writerow(row)
                f.flush()  # 确保数据被写入磁盘
                logger.debug(f"写入CSV行: {row}")
            except Empty:
                continue
            except Exception as e:
                logger.error(f"写入CSV时出错: {e}")

# 初始化数据存储的列，包括新的特征
columns = [
    'Timestamp', 'Source IP', 'Destination IP', 'Source Port',
    'Destination Port', 'Protocol', 'SNI', 'Category',
    'Packet Size', 'Time Since Last Packet'
]

# 创建停止事件
stop_event = threading.Event()

# 启动CSV写入线程
writer_thread = threading.Thread(target=csv_writer, args=(csv_queue, OUTPUT_CSV, columns, stop_event), daemon=True)
writer_thread.start()
logger.debug("CSV写入线程已启动。")

# 管理所有子线程
worker_threads = {}
# 锁用于线程安全
worker_lock = threading.Lock()

# 四元组到线程的映射
tuple_to_thread = {}
# 定义超时时间（秒）
THREAD_TIMEOUT = 60

# 维护每个流的最后一个包时间戳
flow_last_time = defaultdict(float)
# 锁用于保护 flow_last_time
flow_time_lock = threading.Lock()

# 事件用于优雅关闭
shutdown_event = threading.Event()

def normalize_flow_tuple(src_ip, src_port, dst_ip, dst_port):
    """
    标准化四元组，确保双向流量的四元组一致。
    """
    if (src_ip, src_port) <= (dst_ip, dst_port):
        return (src_ip, src_port, dst_ip, dst_port)
    else:
        return (dst_ip, dst_port, src_ip, src_port)

def packet_callback(packet):
    try:
        logger.debug("处理一个新的数据包。")
        timestamp = datetime.datetime.fromtimestamp(float(packet.sniff_timestamp)).strftime('%Y-%m-%d %H:%M:%S')

        # 检查是否存在 'IP' 层
        if 'IP' not in packet:
            logger.warning("Packet does not have 'IP' layer.")
            return  # 跳过不包含 'IP' 层的数据包

        ip_layer = packet['IP']
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst

        # 检查是否存在传输层
        if 'TCP' in packet:
            transport_layer = 'TCP'
        elif 'UDP' in packet:
            transport_layer = 'UDP'
        else:
            logger.warning("Packet does not have TCP or UDP layer.")
            return  # 跳过不包含传输层的数据包

        transport = packet[transport_layer]
        src_port = transport.srcport
        dst_port = transport.dstport
        protocol = transport_layer.upper()

        # 提取包级别特征
        packet_size = int(packet.length)

        # 标准化四元组
        flow_tuple = normalize_flow_tuple(src_ip, src_port, dst_ip, dst_port)

        # 计算 time_since_last_packet
        with flow_time_lock:
            last_time = flow_last_time.get(flow_tuple, None)
            current_time = time.time()
            if last_time is not None:
                time_since_last_packet = current_time - last_time
            else:
                time_since_last_packet = 0.0  # 第一个包
            flow_last_time[flow_tuple] = current_time

        # 尝试提取 SNI
        sni = None
        if 'tls' in packet:
            try:
                tls_layer = packet['tls']
                sni = getattr(tls_layer, 'handshake_extensions_server_name', None)
                if sni:
                    print(f"提取到SNI: {sni}")
                logger.debug(f"提取到SNI: {sni}")
            except AttributeError:
                sni = None
                logger.debug("数据包中没有SNI字段。")

        if sni:
            # 分类流量
            category, app_name = classify_traffic_from_db(sni, protocol)
            logger.debug(f"流量分类: Category={category}, App Name={app_name}")
        else:
            # 分配默认类别
            category, app_name = "Unclassified", "Unclassified"
            logger.debug(f"没有提取到SNI，分配默认类别: Category={category}, App Name={app_name}")

        # 添加到数据列表并写入CSV
        row = [
            timestamp, src_ip, dst_ip, src_port, dst_port,
            protocol, sni if sni else '', category,
            packet_size, round(time_since_last_packet, 6)
        ]
        csv_queue.put(row)
        logger.debug(f"数据包信息已加入CSV队列: {row}")

        # 分发到子线程
        dispatch_packet({
            'timestamp': timestamp,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'sni': sni,
            'category': category,
            'app_name': app_name,
            'length': packet_size,
            'time_since_last_packet': time_since_last_packet,
            'flow_tuple': flow_tuple  # 添加 flow_tuple 到 packet_info
        })

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received in packet_callback.")
        shutdown_event.set()  # 通知主线程进行清理
    except AttributeError as e:
        logger.error(f"AttributeError: {e}")
    except Exception as e:
        logger.error(f"Error processing packet: {e}")

def dispatch_packet(packet_info):
    app_name = packet_info['app_name']
    sni = packet_info['sni']
    src_ip = packet_info['src_ip']
    dst_ip = packet_info['dst_ip']
    src_port = packet_info['src_port']
    dst_port = packet_info['dst_port']

    # 标准化四元组
    flow_tuple = normalize_flow_tuple(src_ip, src_port, dst_ip, dst_port)
    logger.debug(f"标准化后的四元组: {flow_tuple}")

    with worker_lock:
        if app_name and app_name not in ["Unknown App", "Other SNI", "Database Error", "Unclassified"]:
            # 有 SNI，按应用名称分发
            if app_name not in worker_threads:
                logger.debug(f"启动新的WorkerThread: {app_name}")
                # 创建新的子线程
                worker = WorkerThread(app_name)
                worker_threads[app_name] = worker
                worker.start()
            worker = worker_threads[app_name]
            worker.enqueue_packet(packet_info)
            logger.debug(f"数据包已分发到WorkerThread: {app_name}")

            # 记录四元组到 tuple_to_thread
            if flow_tuple not in tuple_to_thread:
                tuple_to_thread[flow_tuple] = worker
                logger.debug(f"四元组 {flow_tuple} 已关联到 WorkerThread: {app_name}")
            else:
                logger.debug(f"四元组 {flow_tuple} 已存在于 tuple_to_thread，关联的 WorkerThread: {tuple_to_thread[flow_tuple].app_name}")

        else:
            # 无 SNI 或分配到默认类别，根据四元组匹配
            if flow_tuple in tuple_to_thread:
                worker = tuple_to_thread[flow_tuple]
                worker.enqueue_packet(packet_info)
                logger.debug(f"数据包已分发到已有的WorkerThread: {worker.app_name} (四元组: {flow_tuple})")
            else:
                # 分配到默认的“Unclassified”线程
                default_app = "Unclassified"
                if default_app not in worker_threads:
                    logger.debug("启动新的WorkerThread: Unclassified")
                    worker = WorkerThread(default_app)
                    worker_threads[default_app] = worker
                    worker.start()
                worker = worker_threads[default_app]
                worker.enqueue_packet(packet_info)
                logger.debug("数据包已分发到默认的WorkerThread: Unclassified")
                # 不记录默认线程的四元组，以避免将所有未分类的数据包都关联到一个线程

def monitor_workers():
    logger.debug("启动监控线程。")
    while not shutdown_event.is_set():
        time.sleep(30)  # 检查间隔
        current_time = time.time()
        with worker_lock:
            to_remove = []
            for app_name, worker in list(worker_threads.items()):
                if current_time - worker.last_packet_time > THREAD_TIMEOUT:
                    logger.debug(f"停止WorkerThread: {app_name}")
                    worker.stop()
                    to_remove.append(app_name)
            for app_name in to_remove:
                del worker_threads[app_name]
                logger.debug(f"已移除WorkerThread: {app_name}")
                # 从 tuple_to_thread 中移除关联的四元组
                tuples_to_remove = [t for t, w in tuple_to_thread.items() if w.app_name == app_name]
                for t in tuples_to_remove:
                    del tuple_to_thread[t]
                    logger.debug(f"已从 tuple_to_thread 中移除四元组: {t}")
    # 清理四元组映射中已停止的线程
    with worker_lock:
        to_remove_tuples = [t for t, w in tuple_to_thread.items() if not w.is_alive()]
        for t in to_remove_tuples:
            del tuple_to_thread[t]
            logger.debug("已移除已停止的四元组映射。")

async def capture_packets():
    print(f"Starting packet capture on interface {INTERFACE}...")
    logger.info(f"Starting packet capture on interface {INTERFACE}...")
    capture = pyshark.LiveCapture(
        interface=INTERFACE,
        bpf_filter='tcp or udp',
    )

    loop = asyncio.get_event_loop()

    # 定义信号处理器
    def handle_interrupt():
        print("\nCapture interrupted. Saving captured data...")
        logger.info("捕获被中断，开始保存数据。")
        shutdown_event.set()  # 通知监控线程停止
        # 关闭捕获
        asyncio.create_task(capture.close_async())

    # 在支持的情况下添加信号处理器
    try:
        loop.add_signal_handler(signal.SIGINT, handle_interrupt)
    except NotImplementedError:
        # 在 Windows 上，add_signal_handler 不支持 SIGINT
        pass

    # 启动监控线程
    monitor_thread = threading.Thread(target=monitor_workers, daemon=True)
    monitor_thread.start()
    logger.debug("监控线程已启动。")

    try:
        await capture.apply_on_packets(packet_callback)
    except TSharkCrashException as e:
        logger.error(f"TShark 崩溃: {e}")
        shutdown_event.set()
    except asyncio.CancelledError:
        logger.info("捕获任务被取消。")
    except Exception as e:
        logger.error(f"Unexpected error during packet capture: {e}")
    finally:
        # 释放资源
        await capture.close_async()
        save_data()

def save_data():
    logger.info("开始保存主数据和统计信息。")
    # 因为数据已实时写入CSV，此处无需再次写入
    # 只是确保所有队列中的数据已被写入
    stop_event.set()  # 通知CSV写入线程停止
    writer_thread.join()
    logger.debug("CSV写入线程已停止。")

    # 优雅关闭 WorkerThreads
    with worker_lock:
        for worker in worker_threads.values():
            worker.stop()
    logger.debug("已通知所有WorkerThreads停止。")
    # 等待所有 WorkerThreads 完成
    for worker in list(worker_threads.values()):
        worker.join()
        logger.debug(f"已等待WorkerThread完成: {worker.app_name}")

    logger.info("所有数据保存完成。")

# 启动异步捕获
if __name__ == "__main__":
    try:
        asyncio.run(capture_packets())
    except KeyboardInterrupt:
        print("Capture interrupted by user.")
        logger.info("捕获被用户终止。")
    except Exception as e:
        logger.error(f"RuntimeError: {e}")
