import socket
import threading
from queue import Queue

print("FAST PYTHON PORT SCANNER")

target = input("Enter target IP or website: ")

try:
    target_ip = socket.gethostbyname(target)
except:
    print("Invalid target")
    exit()

print(f"\nScanning target: {target_ip}")
print("Scanning ports 1-1024...\n")

queue = Queue()
open_ports = []

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        result = s.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
            print(f"[OPEN] Port {port}")
    finally:
        s.close()

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

for port in range(1, 1025):
    queue.put(port)

thread_list = []

for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)
    thread.start()

queue.join()

print("\nScan Completed.")
print("Open Ports:", open_ports)