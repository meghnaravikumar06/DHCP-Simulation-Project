# DHCP Simulation Project

## Project Title
**Simulation of Dynamic Host Configuration Protocol (DHCP) Server with IP Pool Management, Lease Expiry, and Conflict Management**

---

## Team Members
- **24BAI1284** – S Rahul  
- **24BAI1134** – Meghna Ravikumar  

---

## Objective
To simulate the working of a DHCP Server (as defined in RFC 2131) that dynamically assigns IP addresses to clients, manages lease expiry, handles conflicts, and recycles addresses back to the pool. The simulation also allows **clients to automatically discover the server** over the LAN using UDP broadcast.

---

## Features
- Implements **DHCP DORA Process** (Discover, Offer, Request, Acknowledge).  
- **IP Pool Management** – Assigns addresses from a defined pool.  
- **Lease Expiry Handling** – Frees IPs after lease timeout.  
- **Conflict Detection** – Prevents multiple assignment of the same IP.  
- **Broadcast-based Server Discovery** – Clients automatically find the server in the network.  
- **Logging** – Saves all events (Discover/Offer/Request/Ack/Expiry) to a CSV file.  
- **Multi-client Simulation** – Simulates multiple clients using Python threads.  
- **Status Display** – Periodic display of available and assigned IPs.


---

## Implementation
**Language:** Python 3 (standard libraries only – `threading`, `socket`, `time`, `csv`)  

### Server (`dhcp_server.py`)
- Listens for **DISCOVER messages** from clients via UDP broadcast.  
- Sends **OFFER** for available IPs.  
- Handles **REQUEST** and responds with **ACK/NACK**.  
- Tracks **lease time** and returns expired IPs to the pool.  
- Logs all events to `results/dhcp_log.csv`.

### Client (`dhcp_client.py`)
- Broadcasts **DISCOVER** to find DHCP server automatically.  
- Receives **OFFER**, sends **REQUEST**, and waits for **ACK**.  
- Displays assigned IP and waits for lease expiry before requesting again.

---

  ## How to Run
  
  Clone this repo
  ```bash
  git clone https://github.com/meghnaravikumar06/DHCP-Simulation-Project.git
  cd DHCP-Simulation-Project/src
```
  Run the server (Laptop A)
  ```bash
  python3 dhcp_server.py
  ```
  - The server will print its IP and start listening for client broadcasts.

  Run the client (Laptop B)
  ```bash
  python3 dhcp_client.py
  ```
  - The client will broadcast DISCOVER messages.
  - Server responds with OFFER → client sends REQUEST → server replies with ACK.
  - IP assignment and lease expiry are displayed in console.
  
  Logs will automatically be saved locally in:
  ```bash
  results/dhcp_log.csv
```
---

## Sample Output
```bash
  [12:00:01] DHCP Discover Sent | Client: C1 | IP:
  [12:00:01] DHCP Offer Sent    | Client: C1 | IP: 192.168.1.5
  [12:00:02] DHCP ACK Sent      | Client: C1 | IP: 192.168.1.5
  [12:00:02] Client Received IP | Client: C1 | IP: 192.168.1.5
  ...
  [12:00:22] Lease Expired      | Client: C1 | IP: 192.168.1.5
```
  ---

## Notes
- Both laptops must be connected to the same LAN (Wi-Fi, mobile hotspot, or router).
- No manual server IP entry is required — the client discovers the server automatically.
- Ensure firewall allows UDP traffic on port 5005.

## Report Contents
- Abstract
- Objective
- Background: DHCP, RFC 2131, DORA sequence
- Implementation (server, client, lease management, broadcast discovery)
- Results (logs, screenshots, diagrams)
- Conclusion

