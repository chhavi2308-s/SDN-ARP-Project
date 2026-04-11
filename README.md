# SDN-Based ARP Handling using Mininet and POX

---

## 📌 Problem Statement

In traditional networks, Address Resolution Protocol (ARP) requests are broadcast to all hosts, causing:
- Unnecessary network flooding  
- Increased bandwidth usage  
- Reduced network efficiency  

This project implements an SDN-based solution where a centralized controller intelligently handles ARP requests by learning IP-to-MAC mappings and reducing broadcast traffic.

---

## 🎯 Objective

- Demonstrate controller–switch interaction using SDN  
- Implement ARP packet handling using an OpenFlow controller  
- Design and apply match–action flow rules  
- Observe and analyze network behavior and performance  

---

## 🛠️ Tools & Technologies

- Mininet  
- POX Controller  
- Open vSwitch (OVS)  
- OpenFlow Protocol (OpenFlow 1.0)  
- Python  

---

## 🏗️ Network Topology

- Single switch topology  
- Three hosts (h1, h2, h3) connected to switch (s1)  

---

## ⚙️ Setup Instructions

### 1. Install Mininet
```bash
sudo apt update
sudo apt install mininet -y
2. Install POX Controller
sudo apt install git -y
git clone https://github.com/noxrepo/pox
cd pox
▶️ Execution Steps
Step 0: Clean previous Mininet state (IMPORTANT)
sudo mn -c
Step 1: Run Controller
cd ~/pox
./pox.py log.level --DEBUG arp_controller
Step 2: Run Mininet Topology (Force OpenFlow 1.0)
sudo mn --controller=remote --topo=single,3 --switch ovs,protocols=OpenFlow10
Step 3: Test Connectivity
pingall
📊 Expected Output
Ping Result
*** Results: 0% dropped (6/6 received)
Controller Logs
Learned ARP: 10.0.0.x -> xx:xx:xx
Flow installed + packet forwarded
🧠 Working Explanation
When a host sends a packet, the switch checks its flow table.
If no rule exists, the packet is sent to the controller (Packet-In event).
The controller:
Learns MAC → Port mapping
Learns IP → MAC mapping (ARP table)
If the destination is known:
A flow rule is installed in the switch
Packet is forwarded directly
If the destination is unknown:
Packet is flooded
After learning:
Subsequent packets are handled directly by the switch

After flow rule installation, packets are processed in the data plane, reducing controller overhead.

🔁 Flow Rule Design (Match–Action)
Match Fields:
Destination MAC address (dl_dst)
Action:
Forward packet to corresponding output port
Flow Parameters:
Priority = 10
Idle Timeout = 30 seconds
Hard Timeout = 60 seconds
🧪 Test Scenarios
✅ Scenario 1: Initial Communication
ARP mapping unknown
Packet is flooded
Controller learns mapping
✅ Scenario 2: Subsequent Communication
ARP mapping exists
No flooding required
Faster communication using installed flow rules
📸 Proof of Execution
1. Ping Results (pingall)
<img width="1139" height="643" alt="image" src="https://github.com/user-attachments/assets/ce177a7d-e184-4120-848a-a9e357d2be73" />
2. Controller Logs (ARP Learning & Flow Installation)
<img width="892" height="406" alt="image" src="https://github.com/user-attachments/assets/e48e2427-507a-4332-9ae8-8237c747148d" />
3. Flow Table Verification
sh ovs-ofctl dump-flows s1
<img width="1405" height="317" alt="image" src="https://github.com/user-attachments/assets/35f7180b-17e1-4e8f-b9cb-b105d55084ef" />
4. Throughput Test
iperf h1 h2
<img width="717" height="118" alt="image" src="https://github.com/user-attachments/assets/cb72346c-6f8e-4712-b9b7-3b5ef7fe30b8" />
📈 Performance Observation & Analysis
Initial packets trigger controller involvement (Packet-In events)
Flow rules are dynamically installed in the switch
Subsequent packets bypass the controller
Reduced ARP broadcast traffic
Improved latency after learning phase
Stable throughput observed using iperf
⚠️ Troubleshooting
Issue: RTNETLINK error (File exists)
sudo mn -c
Issue: No flow rules visible
Ensure controller is running
Use OpenFlow 1.0:
--switch ovs,protocols=OpenFlow10
Issue: Command not found
sh ovs-ofctl dump-flows s1
📚 References
Mininet Documentation
POX Documentation
OpenFlow Switch Specification
👨‍💻 Conclusion

This project demonstrates how SDN enables intelligent network management by separating the control plane from the data plane. By implementing ARP handling at the controller, unnecessary broadcast traffic is reduced, improving overall network efficiency and performance.

🚀 Future Enhancements
Implement firewall rules (allow/block traffic)
Add Quality of Service (QoS) mechanisms
Extend to multi-switch topologies
