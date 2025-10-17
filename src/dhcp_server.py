import socket
import threading
import time
import csv
import os

SERVER_PORT = 5005
BUFFER_SIZE = 1024
IP_POOL = [f"192.168.1.{i}" for i in range(2, 20)]
LEASE_TIME = 30
LOG_FILE = "results/dhcp_log.csv"
STATUS_INTERVAL = 5

leases = {}
lock = threading.Lock()

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

with open(LOG_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Event"])

def log_event(event):
    timestamp = time.strftime('%H:%M:%S', time.localtime())
    try:
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event])
    except PermissionError:
        print(f"[{timestamp}] ERROR: Cannot write to log file!")
    print(f"[{timestamp}] {event}")

def release_expired_leases():
    while True:
        time.sleep(1)
        now = time.time()
        expired_clients = []
        with lock:
            for client_id, (ip, expiry) in leases.items():
                if expiry <= now:
                    expired_clients.append(client_id)
            for client_id in expired_clients:
                ip, _ = leases.pop(client_id)
                IP_POOL.append(ip)
                log_event(f"Lease expired | Client: {client_id} | IP: {ip}")

def display_status():
    while True:
        time.sleep(STATUS_INTERVAL)
        with lock:
            available_ips = [ip for ip in IP_POOL if ip not in [x[0] for x in leases.values()]]
            print("\n--- DHCP Server Status ---")
            print(f"Available IPs: {available_ips}")
            print(f"Assigned IPs: {leases}")
            print("--------------------------\n")

def handle_client(data, addr, server_socket):
    msg = data.decode()
    client_id = f"{addr[0]}:{addr[1]}"
    with lock:
        if msg == "DISCOVER":
            if IP_POOL:
                offered_ip = IP_POOL[0]
                log_event(f"DISCOVER received | Client: {client_id}")
                server_socket.sendto(f"OFFER:{offered_ip}".encode(), addr)
                log_event(f"OFFER sent | Client: {client_id} | IP: {offered_ip}")
        elif msg.startswith("REQUEST:"):
            requested_ip = msg.split(":")[1]
            if requested_ip in IP_POOL:
                IP_POOL.remove(requested_ip)
                leases[client_id] = (requested_ip, time.time() + LEASE_TIME)
                server_socket.sendto(f"ACK:{requested_ip}".encode(), addr)
                log_event(f"ACK sent | Client: {client_id} | IP: {requested_ip}")
            else:
                server_socket.sendto(f"NACK:{requested_ip}".encode(), addr)
                log_event(f"NACK sent | Client: {client_id} | IP: {requested_ip}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(('', SERVER_PORT))
    print(f"DHCP Server running on port {SERVER_PORT}")

    threading.Thread(target=release_expired_leases, daemon=True).start()
    threading.Thread(target=display_status, daemon=True).start()

    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            threading.Thread(target=handle_client, args=(data, addr, server_socket), daemon=True).start()
        except Exception as e:
            log_event(f"Error in main server loop: {e}")

if __name__ == "__main__":
    start_server()
