import socket
import threading
from queue import Queue

def scan_port(ip, port):
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        result = sock.connect_ex((ip, port))
        sock.close()
        
        return result == 0
    
    except Exception:
        return False

def scan_ports(ip, ports, threads = 100):
    
    open_ports = []
    lock = threading.Lock()
    queue = Queue()
    
    unique_ports = set(ports)
    
    for port in unique_ports:
        queue.put(port)
        
    def worker():
        
        while not queue.empty():
            try:
                port = queue.get(timeout = 1)
                
                if scan_port(ip, port):
                    with lock:
                        open_ports.append(port)
                queue.task_done()
            except:
                break
                
    thread_list = []
    
    for _ in range(threads):
        t = threading.Thread(target = worker)
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    queue.join()
    
    return sorted(open_ports)