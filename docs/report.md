# DHCP Simulation Project Report

## Project Title
**Simulation of Dynamic Host Configuration Protocol (DHCP) Server with IP Pool Management, Lease Expiry, and Conflict Management**

## Team Members
- 24BAI1284 – S Rahul  
- 24BAI1134 – Meghna Ravikumar

---

## 1. Abstract
This project simulates a DHCP server as defined in RFC 2131. It dynamically assigns IP addresses to clients, manages lease expiry, handles conflicts, and logs all events. The simulation uses Python threads to mimic multiple clients interacting with a DHCP server concurrently.

---

## 2. Objective
- Simulate DHCP DORA process (Discover, Offer, Request, Acknowledge)  
- Implement IP pool management  
- Handle lease expiry and automatically recycle IPs  
- Detect and prevent IP conflicts  
- Log all events to a CSV file  
- Display periodic status of assigned and available IPs  

---

## 3. Background
**Dynamic Host Configuration Protocol (DHCP)** allows network devices to obtain IP addresses automatically. RFC 2131 defines the standard DORA process:  

1. **Discover** – Client requests an IP.  
2. **Offer** – Server proposes an available IP.  
3. **Request** – Client requests the offered IP.  
4. **Acknowledge (ACK)** – Server confirms the assignment and lease duration.  

Additional server responsibilities include lease management, conflict detection, and logging.

---

## 4. Implementation

### Language & Libraries
- Python 3.x  
- Standard libraries: `threading`, `time`, `csv`  

### Server Functions
- `discover(client_id)` – logs client's Discover message  
- `offer(client_id, ip)` – logs offered IP  
- `ack(client_id, ip)` – confirms IP assignment  
- `assign_ip(client_id)` – allocates available IP from pool  
- `release_ip(client_id)` – releases IP manually  
- `check_leases()` – daemon thread that frees expired IPs  
- `display_status()` – daemon thread displaying periodic pool status  

### Client Simulation
- Each client runs on a separate thread  
- Requests an IP, waits for lease expiry  
- All events logged and displayed  

---

## 5. Sample Output

**Console Output:**

```bash
[12:00:01] DHCP Discover Sent | Client: C1 | IP:
[12:00:01] DHCP Offer Sent    | Client: C1 | IP: 192.168.1.5
[12:00:02] DHCP ACK Sent      | Client: C1 | IP: 192.168.1.5
[12:00:02] Client Received IP | Client: C1 | IP: 192.168.1.5
...
[12:00:22] Lease Expired      | Client: C1 | IP: 192.168.1.5
```

**Status Display (Periodic):**
```bash
--- Status ---
Available IPs: ['192.168.1.5', '192.168.1.6', ...]
Assigned IPs: {'C1': ('192.168.1.2', 1700000000.0), 'C2': ('192.168.1.3', 1700000005.0)}
```

  ---


**CSV Log (`results/dhcp_log.csv`):**
- Timestamp | Event  
- `12:00:01 | DHCP Discover Sent | Client: C1`  
- `12:00:01 | DHCP Offer Sent | Client: C1 | IP: 192.168.1.2`  
- …  

> Capture screenshots of console output and CSV log for submission.

---

## 6. Conclusion
The DHCP simulation project successfully demonstrates:

- Dynamic IP allocation from a defined pool  
- Lease expiry and automatic recycling  
- Conflict prevention during assignment  
- Multi-client interaction using threads  
- Logging and periodic status display  

The project validates the working of DHCP as per RFC 2131 and provides a clear understanding of DORA operations and IP management.

---

## 7. References
- RFC 2131 – Dynamic Host Configuration Protocol  
- Python 3 Documentation (`threading`, `csv`, `time`)  
- GitHub repository: [DHCP-Simulation-Project](https://github.com/meghnaravikumar06/DHCP-Simulation-Project)
