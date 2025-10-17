import socket
import time

SERVER_PORT = 5005
BUFFER_SIZE = 1024
LEASE_TIME = 30

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.settimeout(5)

def dhcp_discover():
    client_socket.sendto(b"DISCOVER", ('<broadcast>', SERVER_PORT))
    try:
        data, addr = client_socket.recvfrom(BUFFER_SIZE)
        msg = data.decode()
        if msg.startswith("OFFER:"):
            offered_ip = msg.split(":")[1]
            print(f"OFFER received from {addr[0]}: {offered_ip}")
            return offered_ip, addr[0]
    except socket.timeout:
        print("No offer received, retrying...")
    return None, None

def dhcp_request(ip, server_ip):
    client_socket.sendto(f"REQUEST:{ip}".encode(), (server_ip, SERVER_PORT))
    try:
        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        msg = data.decode()
        if msg.startswith("ACK:"):
            assigned_ip = msg.split(":")[1]
            print(f"ACK received: {assigned_ip}")
            return assigned_ip
        elif msg.startswith("NACK:"):
            print(f"NACK received for IP {ip}")
    except socket.timeout:
        print("No ACK received, retrying...")
    return None

if __name__ == "__main__":
    while True:
        offered_ip, server_ip = dhcp_discover()
        if offered_ip and server_ip:
            assigned_ip = dhcp_request(offered_ip, server_ip)
            if assigned_ip:
                print(f"Assigned IP: {assigned_ip}")
                time.sleep(LEASE_TIME)
