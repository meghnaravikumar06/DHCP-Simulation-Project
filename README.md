# DHCP Simulation Project

## Project Title
**Simulation of Dynamic Host Configuration Protocol (DHCP) Server with IP Pool Management, Lease Expiry, and Conflict Management**

---

## Team Members
- **24BAI1284** – S Rahul  
- **24BAI1134** – Meghna Ravikumar  

---

## Objective
To simulate the working of a **DHCP Server** (as defined in RFC 2131) that dynamically assigns IP addresses to clients, manages lease expiry, handles conflicts, and recycles addresses back to the pool.

---

## Features
- Implements DHCP **DORA Process** (Discover, Offer, Request, Acknowledge).  
- **IP Pool Management** – Assigns addresses from a defined pool.  
- **Lease Expiry Handling** – Frees IPs after lease timeout.  
- **Conflict Detection** – Prevents multiple assignment of the same IP.  
- **Logging** – Saves all events (Discover/Offer/Request/Ack/Expiry) to a CSV file.  
- **Multi-client Simulation** – Simulates multiple clients using threading.  
- **Status Display** – Periodic display of available and assigned IPs.  

---

## Implementation
- **Language:** Python 3 (standard libraries only – `threading`, `time`, `csv`)  
- **Server Functions:**  
  - `discover()` → Client requests IP.  
  - `offer()` → Server offers an available IP.  
  - `request()` → Client requests offered IP.  
  - `ack()` → Server acknowledges and assigns lease.  
  - `release_expired_leases()` → Returns expired IPs to pool.  
- **Client Simulation:** Each client runs on a separate thread, requests IP, and logs output.  

 ---

  ## How to Run
  
  Clone this repo
  ```bash
  git clone https://github.com/<your-username>/DHCP-Simulation-Project.git
  cd DHCP-Simulation-Project/src
```
  Run the simulation
  ```bash
  python3 dhcp_simulation.py
  ```
  Logs will be saved in:
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

## Report Contents
- Abstract
- Objective
- Background: DHCP, RFC 2131, DORA sequence
- Implementation (server, client, lease management)
- Results (logs, screenshots, diagrams)
- Conclusion

