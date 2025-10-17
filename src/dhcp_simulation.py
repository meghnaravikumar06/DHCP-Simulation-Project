import threading
import time
import csv

# CONFIGURATION
IP_POOL = [f"192.168.1.{i}" for i in range(2, 20)]  # IP pool
LEASE_TIME = 15  # seconds, for demo purposes
STATUS_INTERVAL = 5  # seconds between status displays
LOG_FILE = "../results/dhcp_log.csv"

# GLOBAL VARIABLES
assigned_ips = {}  # client_id : (ip, lease_expiry)
lock = threading.Lock()  # For thread-safe operations

# HELPER FUNCTIONS
def log_event(event):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event])
    print(f"[{timestamp}] {event}")

def discover(client_id):
    log_event(f"DHCP Discover Sent | Client: {client_id}")

def offer(client_id, ip):
    log_event(f"DHCP Offer Sent    | Client: {client_id} | IP: {ip}")

def ack(client_id, ip):
    log_event(f"DHCP ACK Sent      | Client: {client_id} | IP: {ip}")
    log_event(f"Client Received IP | Client: {client_id} | IP: {ip}")

def assign_ip(client_id):
    with lock:
        available_ips = [ip for ip in IP_POOL if ip not in [x[0] for x in assigned_ips.values()]]
        if not available_ips:
            log_event(f"Client {client_id}: No IPs available!")
            return None
        ip = available_ips[0]
        expiry = time.time() + LEASE_TIME
        assigned_ips[client_id] = (ip, expiry)
        offer(client_id, ip)
        time.sleep(1)  # simulate client request time
        ack(client_id, ip)
        return ip

def release_ip(client_id):
    with lock:
        if client_id in assigned_ips:
            ip = assigned_ips[client_id][0]
            del assigned_ips[client_id]
            log_event(f"Client {client_id}: Released IP {ip}")

def check_leases():
    while True:
        time.sleep(1)
        with lock:
            now = time.time()
            expired_clients = [cid for cid, (_, exp) in assigned_ips.items() if exp < now]
            for cid in expired_clients:
                ip = assigned_ips[cid][0]
                del assigned_ips[cid]
                log_event(f"Lease Expired      | Client: {cid} | IP: {ip}")

def display_status():
    while True:
        time.sleep(STATUS_INTERVAL)
        with lock:
            available_ips = [ip for ip in IP_POOL if ip not in [x[0] for x in assigned_ips.values()]]
            print(f"\n--- Status ---")
            print(f"Available IPs: {available_ips}")
            print(f"Assigned IPs: {assigned_ips}")
            print(f"---------------\n")

# CLIENT SIMULATION
def client_simulation(client_id):
    discover(client_id)
    ip = assign_ip(client_id)
    # Hold lease until expiry
    while ip and client_id in assigned_ips:
        time.sleep(1)

# MAIN EXECUTION
def main():
    # Clear log file
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Event"])

    # Start lease checker thread
    lease_thread = threading.Thread(target=check_leases, daemon=True)
    lease_thread.start()

    # Start status display thread
    status_thread = threading.Thread(target=display_status, daemon=True)
    status_thread.start()

    # Start multiple client threads
    client_threads = []
    for i in range(1, 6):  # simulate 5 clients
        t = threading.Thread(target=client_simulation, args=(f"C{i}",))
        t.start()
        client_threads.append(t)
        time.sleep(0.5)  # stagger clients

    # Wait for all clients to finish
    for t in client_threads:
        t.join()

if __name__ == "__main__":
    main()
