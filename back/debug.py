from scapy.all import sniff, wrpcap

def simple_scapy_capture():
    print("开始简单捕获，持续10秒...")
    packets = sniff(timeout=10, filter="tcp or udp")
    wrpcap("simple_capture_scapy.pcap", packets)
    print("简单捕获完成，保存到 simple_capture_scapy.pcap")

if __name__ == "__main__":
    simple_scapy_capture()
