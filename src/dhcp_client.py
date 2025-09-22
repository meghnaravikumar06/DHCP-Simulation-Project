import socket
import time

SERVER_PORT = 5005
BUFFER_SIZE = 1024

# Protocol constants
DISCOVER = "DISCOVER"
OFFER = "OFFER"
REQUEST = "REQUEST"
ACK = "ACK"
NACK = "NACK"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.settimeout(5)

def dhcp_discover():
    client_socket.sendto(DISCOVER.encode(), ('<broadcast>', SERVER_PORT))
    try:
        data, server_addr = client_socket.recvfrom(BUFFER_SIZE)
        if data.decode().startswith(OFFER):
            offered_ip = data.decode().split(":")[1]
            dhcp_request(server_addr, offered_ip)
    except socket.timeout:
        print("No OFFER received, retrying...")
        time.sleep(2)

def dhcp_request(server_addr, offered_ip):
    client_socket.sendto(f"{REQUEST}:{offered_ip}".encode(), server_addr)
    try:
        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        msg = data.decode()
        if msg.startswith(ACK):
            lease_time = int(msg.split(":")[2])  # server sends ACK:ip:lease
            print(f"Lease granted for {offered_ip} (lease={lease_time}s)")
            lease_loop(offered_ip, lease_time, server_addr)
        elif msg.startswith(NACK):
            print("Request denied. Restarting DISCOVER.")
    except socket.timeout:
        print("No ACK/NACK received, restarting DISCOVER.")

def lease_loop(ip, lease_time, server_addr):
    # Simulate lease monitoring
    renew_time = lease_time // 2
    expire_time = lease_time
    start = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed >= renew_time:
            print(f"Renewing lease for {ip}...")
            client_socket.sendto(f"{REQUEST}:{ip}".encode(), server_addr)
            try:
                data, _ = client_socket.recvfrom(BUFFER_SIZE)
                msg = data.decode()
                if msg.startswith(ACK):
                    lease_time = int(msg.split(":")[2])
                    print(f"Lease renewed for {ip} (lease={lease_time}s)")
                    # reset timer
                    start = time.time()
                    renew_time = lease_time // 2
                    expire_time = lease_time
                    continue
                else:
                    print("Renewal failed, restarting DISCOVER.")
                    return
            except socket.timeout:
                print("No response on renewal, restarting DISCOVER.")
                return

        if elapsed >= expire_time:
            print(f"Lease expired for {ip}, restarting DISCOVER.")
            return

        time.sleep(1)

def main():
    while True:
        dhcp_discover()
        time.sleep(2)  # prevent tight loop

if __name__ == "__main__":
    main()
