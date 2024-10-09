import pyshark
import pandas as pd
import datetime
import logging
import asyncio
import nest_asyncio
import signal
import sys

# 解决嵌套事件循环问题
nest_asyncio.apply()

# 日志配置
logging.basicConfig(filename='../log/sni.log', level=logging.ERROR)

# 定义要捕获的网络接口，例如 'eth0'、'Wi-Fi' 等
INTERFACE = r"\Device\NPF_{382B8322-0D2A-47B8-B366-CF6FD3C226C0}"

# 输出CSV文件路径
OUTPUT_CSV = '../output/sni_capture.csv'

# 初始化数据存储
columns = ['Timestamp', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol', 'SNI']
data = []

# 定义捕获回调函数
def packet_callback(packet):
    try:
        timestamp = datetime.datetime.fromtimestamp(float(packet.sniff_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        src_port = packet[packet.transport_layer].srcport
        dst_port = packet[packet.transport_layer].dstport
        protocol = packet.transport_layer.upper()

        # 尝试提取SNI
        sni = None
        if 'tls' in packet:
            try:
                tls_layer = packet['tls']
                sni = getattr(tls_layer, 'handshake_extensions_server_name', None)
            except AttributeError:
                sni = None

        # 只处理有SNI的流量
        if sni:
            print(f"提取到SNI: {sni}")
            # 添加到数据列表
            data.append([timestamp, src_ip, dst_ip, src_port, dst_port, protocol, sni])

    except AttributeError:
        # 忽略没有IP层或传输层的包
        pass
    except Exception as e:
        logging.error(f"Error processing packet: {e}")

async def capture_packets():
    print(f"Starting packet capture on interface {INTERFACE}...")
    capture = pyshark.LiveCapture(interface=INTERFACE, bpf_filter='tcp or udp')

    def handle_interrupt(signum, frame):
        print("\nCapture interrupted. Saving captured data...")
        capture.eventloop.stop()
        save_data()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        await capture.apply_on_packets(packet_callback)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        # 释放资源
        await capture.close_async()
        save_data()

def save_data():
    # 转换为DataFrame
    df = pd.DataFrame(data, columns=columns)

    # 保存到CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Packet capture complete. Data saved to {OUTPUT_CSV}")

if __name__ == '__main__':
    # 启动异步捕获
    try:
        asyncio.run(capture_packets())
    except SystemExit:
        print("Capture terminated by user.")
    except RuntimeError:
        # 忽略由事件循环关闭导致的RuntimeError
        pass