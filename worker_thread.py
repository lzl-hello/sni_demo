# worker_thread.py
import csv
import threading
import queue
import time
import logging
import pandas as pd
import os
from collections import defaultdict

# 设置 WorkerThread 的日志记录器
logger = logging.getLogger('worker_thread')
logger.setLevel(logging.DEBUG)

# 检查是否已经添加处理器，避免重复添加
if not logger.handlers:
    worker_handler = logging.FileHandler('./log/worker_threads.log')
    worker_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    worker_handler.setFormatter(formatter)
    logger.addHandler(worker_handler)
    logger.propagate = False  # 防止日志传播到根记录器

class WorkerThread(threading.Thread):
    def __init__(self, app_name, timeout=60):
        super().__init__()
        self.app_name = app_name
        self.packet_queue = queue.Queue()
        self.running = True
        self.timeout = timeout
        self.last_packet_time = time.time()
        self.packets = []
        self.statistics = defaultdict(int)
        self.lock = threading.Lock()

        # 文件路径（如果需要保存统计数据）
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        safe_app_name = self.app_name.replace(" ", "_")  # 替换空格以避免文件名问题
        self.csv_file = f'./output/{safe_app_name}_statistics.csv'

        # 初始化CSV写入队列
        self.csv_queue = queue.Queue()
        self.csv_stop_event = threading.Event()
        self.csv_writer_thread = threading.Thread(target=self.csv_writer, args=(self.csv_queue, self.csv_file, self.csv_stop_event), daemon=True)
        self.csv_writer_thread.start()
        logger.debug(f"WorkerThread {self.app_name} 的CSV写入线程已启动。")

    def run(self):
        logger.info(f"WorkerThread {self.app_name} 已启动。")
        try:
            while self.running or not self.packet_queue.empty():
                try:
                    packet_info = self.packet_queue.get(timeout=1)
                    self.last_packet_time = time.time()
                    self.process_packet(packet_info)
                except queue.Empty:
                    continue  # 检查是否需要停止
        except Exception as e:
            logger.error(f"Error in WorkerThread {self.app_name}: {e}")
        finally:
            self.save_results()

    def csv_writer(self, queue, csv_file, stop_event):
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists or os.stat(csv_file).st_size == 0:
                writer.writerow(['packet_count', 'bytes'])  # 写入表头
                logger.debug(f"WorkerThread {self.app_name} 写入CSV表头: ['packet_count', 'bytes']")
            while not stop_event.is_set() or not queue.empty():
                try:
                    row = queue.get(timeout=1)
                    writer.writerow(row)
                    f.flush()  # 确保数据被写入磁盘
                    logger.debug(f"WorkerThread {self.app_name} 写入CSV行: {row}")
                except Exception as e:
                    logger.error(f"WorkerThread {self.app_name} 写入CSV时出错: {e}")

    def enqueue_packet(self, packet_info):
        self.packet_queue.put(packet_info)
        logger.debug(f"数据包已加入WorkerThread {self.app_name} 的队列。")

    def process_packet(self, packet_info):
        # 这里可以添加更复杂的处理逻辑
        with self.lock:
            self.packets.append(packet_info)
            self.statistics['packet_count'] += 1
            self.statistics['bytes'] += packet_info.get('length', 0)
            logger.debug(f"WorkerThread {self.app_name}: packet_count={self.statistics['packet_count']}, bytes={self.statistics['bytes']}")

            # 将统计数据放入CSV队列
            row = [self.statistics['packet_count'], self.statistics['bytes']]
            self.csv_queue.put(row)
            logger.debug(f"WorkerThread {self.app_name} 统计数据已加入CSV队列: {row}")

    def save_results(self):
        # 停止CSV写入线程
        self.csv_stop_event.set()
        self.csv_writer_thread.join()
        logger.debug(f"WorkerThread {self.app_name} 的CSV写入线程已停止。")

        # 保存其他结果（如果有需要）
        logger.info(f"WorkerThread {self.app_name} 已完成所有任务并退出。")

    def stop(self):
        self.running = False
        logger.debug(f"WorkerThread {self.app_name} 收到停止信号。")
