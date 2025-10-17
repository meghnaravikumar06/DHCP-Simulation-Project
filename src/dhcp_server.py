import socket
import threading
import time
import csv
import os

# Ensure the directory exists
os.makedirs('results', exist_ok=True)

LOG_FILE = 'results/dhcp_log.csv'

# Initialize log file
with open(LOG_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Event"])  # optional header

SERVER_PORT = 5005
BUFFER_SIZE = 1024
IP_POOL = [f'192.168.1.{i}' for i in range(2, 20)]
LEASE_TIME = 30  # seconds
leases = {}

# Function to log events
def log_event(event):
    timestamp = time.strftime('%H:%M:%S')
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event])
    print(f"[{timestamp}] {event}")

# Function to release expired leases
def release_expired_leases():
    while True:
        now = time.time()
        expired_clients = [c for c, (ip, exp) in leases.items() if exp <= now]
        for client_id in expired_clients:
            ip, _ = leases.pop(client_id)
            IP_POOL.append(ip)
            log_event(f"Lease expired | Client: {client_id} | IP: {ip}")
        time.sleep(1)

# Function to handle client messages
def handle_client(data, addr, server_socket):
    msg = data.decode()
    client_id = addr[0] + ':' + str(addr[1])
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
            log_event(f"REQUEST received & ACK sent | Client: {client_id} | IP: {requested_ip}")
        else:
            server_socket.sendto(f"NACK:{requested_ip}".encode(), addr)
            log_event(f"REQUEST received & NACK sent | Client: {client_id} | IP: {requested_ip}")

# Start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))
    log_event(f"DHCP Server started on port {SERVER_PORT}")

    # Start lease management thread
    threading.Thread(target=release_expired_leases, daemon=True).start()

    # Listen for clients
    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            threading.Thread(target=handle_client, args=(data, addr, server_socket), daemon=True).start()
        except KeyboardInterrupt:
            log_event("Server shutting down...")
            break

if __name__ == "__main__":
    start_server()
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
    server_socket.bind(('', SERVER_PORT))  # listen on all interfaces
    print(f"DHCP Server running on port {SERVER_PORT} (broadcast enabled)")

    threading.Thread(target=release_expired_leases, daemon=True).start()

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        threading.Thread(target=handle_client, args=(data, addr, server_socket)).start()

if __name__ == "__main__":
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Event"])
    start_server()
