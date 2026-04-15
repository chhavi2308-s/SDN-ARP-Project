# SDN-Based ARP Handling with Controller-Generated Replies (Mininet + POX)

---

## 📌 Problem Statement

In traditional networks, the Address Resolution Protocol (ARP) uses broadcast communication to resolve IP addresses into MAC addresses. This leads to unnecessary network flooding, increased latency, and inefficient bandwidth usage.

This project implements a Software Defined Networking (SDN) solution where a centralized controller intercepts ARP requests, learns host mappings, and generates ARP replies directly—reducing broadcast traffic and improving network efficiency.

---

## 🎯 Objectives

* Demonstrate controller–switch interaction using SDN
* Intercept and process ARP packets at the controller
* Generate ARP replies from the controller (ARP proxy behavior)
* Implement match–action flow rules using OpenFlow
* Enable host discovery through dynamic learning
* Analyze network behavior and performance

---

## 🛠️ Tools & Technologies

* Mininet (Network Emulator)
* POX Controller (Python-based SDN controller)
* Open vSwitch (OVS)
* OpenFlow Protocol (v1.0)
* Python

---

## 🏗️ Network Topology

Single-switch topology with three hosts:

h1 ---

h2 ---- s1
/
h3 ---/

* 1 Switch (s1)
* 3 Hosts (h1, h2, h3)
* Remote SDN Controller (POX)

---

## ▶️ Execution Steps

### 1. Start POX Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG arp_controller
```

### 2. Start Mininet

```bash
sudo mn --controller=remote,ip=127.0.0.1 --topo=single,3 --switch ovs,protocols=OpenFlow10
```

### 3. Test Connectivity (Learning Phase)

```bash
h1 ping h2
```

### 4. Clear ARP Cache (to force ARP request again)

```bash
h1 arp -d 10.0.0.2
```

### 5. Test Again (Reply Generation Phase)

```bash
h1 ping h2
```

### 6. View Flow Table

```bash
sh ovs-ofctl dump-flows s1
```

### 7. Throughput Test

```bash
iperf
```

---

## 🧠 Working Explanation

### 🔹 Step 1: Packet Interception

When a switch receives a packet without a matching rule, it sends a **PacketIn** message to the controller.

### 🔹 Step 2: Learning (Host Discovery)

The controller learns:

* MAC → Port mapping
* IP → MAC mapping (ARP table)

### 🔹 Step 3: ARP Request Handling

* If destination IP is **unknown** → request is flooded
* If destination IP is **known** → controller generates ARP reply

### 🔹 Step 4: ARP Reply Generation (Key Feature)

* Controller constructs ARP reply packet
* Sends it directly to requester
* Eliminates broadcast requirement

### 🔹 Step 5: Flow Rule Installation

* Match: Destination MAC (`dl_dst`)
* Action: Forward to specific port

Flow Parameters:

* Priority = 10
* Idle Timeout = 30 seconds
* Hard Timeout = 60 seconds

### 🔹 Step 6: Optimized Forwarding

After learning:

* Switch handles packets directly
* Controller involvement is minimized

---

## 🔁 Test Scenarios

### ✅ Scenario 1: Initial Communication

* ARP mapping not present
* Packet flooded
* Controller learns mapping

### ✅ Scenario 2: Optimized Communication

* ARP mapping exists
* Controller generates ARP reply
* No flooding occurs

---

## 📸 Proof of Execution

Include the following screenshots in your repository:

1. **Ping Results**

   * Successful connectivity between hosts
   * # SDN-Based ARP Handling with Controller-Generated Replies (Mininet + POX)
<img width="1920" height="1002" alt="image" src="https://github.com/user-attachments/assets/01c4a06f-4c03-425a-9873-944025580b70" />

2. **Controller Logs**

   * Learned ARP entries
   * ARP reply generation logs
  <img width="781" height="456" alt="image" src="https://github.com/user-attachments/assets/d3e9a2ad-6dd7-464b-a5d4-6a8b96ac6a73" />


3. **Flow Table**

   * Output of:

     ```bash
     sh ovs-ofctl dump-flows s1
     ```
     <img width="952" height="126" alt="image" src="https://github.com/user-attachments/assets/3909058a-60ea-4c47-841a-d14c7f71eed4" />


4. **Throughput Test (iperf)**

   * Stable data transfer performance
<img width="566" height="61" alt="image" src="https://github.com/user-attachments/assets/c268753f-3ece-4d94-82a1-4c7df450db91" />

---

## 📊 Performance Analysis

* Initial packets trigger controller interaction (PacketIn events)
* ARP broadcast occurs only during learning phase
* Controller-generated ARP replies eliminate repeated broadcasts
* Flow rules reduce controller dependency
* Reduced latency after initial learning
* Stable throughput observed using iperf

---

## 📈 Results

* Successful controller–switch interaction
* ARP interception and processing implemented
* Controller-generated ARP replies achieved
* Reduced network flooding
* Efficient match–action flow rule execution

---

## 👨‍💻 Conclusion

This project demonstrates how SDN enables intelligent and centralized network control. By intercepting ARP packets and generating replies at the controller, the system reduces unnecessary broadcast traffic, improves efficiency, and enhances network performance.

---

## 🚀 Future Enhancements

* Implement firewall (traffic filtering / blocking)
* Extend to multi-switch topology
* Add QoS (Quality of Service) policies
* Integrate monitoring and analytics dashboards

---

## 📚 References

* Mininet Documentation
* POX Controller Documentation
* OpenFlow Switch Specification

---

## 👤 Author

**Chhavi Siddarth Wadhwa**

---
