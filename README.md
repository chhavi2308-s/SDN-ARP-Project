# SDN-Based ARP Handling using Mininet and POX

---

## 📌 Problem Statement

In traditional networks, Address Resolution Protocol (ARP) requests are broadcast to all hosts, causing unnecessary network flooding and inefficient bandwidth utilization.

This project implements a Software Defined Networking (SDN) solution where a centralized controller intelligently handles ARP requests by learning IP-to-MAC mappings and reducing broadcast traffic.

---

## 🎯 Objective

- Demonstrate controller–switch interaction using SDN  
- Implement ARP handling using an OpenFlow controller  
- Design and apply match–action flow rules  
- Observe and analyze network behavior  

---

## 🛠️ Tools & Technologies

- Mininet  
- POX Controller  
- Open vSwitch (OVS)  
- OpenFlow Protocol  
- Python  

---

## 🏗️ Network Topology

Single switch topology with three hosts:

h1 ---\
       \
h2 ---- s1
       /
h3 ---/

---

## ▶️ Execution Steps

### Step 1: Start Controller
cd ~/pox
./pox.py log.level --DEBUG arp_controller

### Step 2: Start Mininet
sudo mn --controller=remote --topo=single,3 --switch ovs,protocols=OpenFlow10

### Step 3: Test Connectivity
pingall

---

## 🧠 Working Explanation

- When a packet arrives at the switch without a matching rule, it is sent to the controller (PacketIn).
- The controller learns:
  - MAC → Port mapping  
  - IP → MAC mapping (ARP table)  
- If the destination is known:
  - A flow rule is installed in the switch  
  - Packet is forwarded directly  
- If unknown:
  - Packet is flooded  
- After learning:
  - Subsequent packets are handled directly by the switch  

---

## 🔁 Flow Rule Design

- Match: Destination MAC address (dl_dst)  
- Action: Forward to corresponding output port  

Flow Parameters:
- Priority = 10  
- Idle Timeout = 30 seconds  
- Hard Timeout = 60 seconds  

---

## 🧪 Test Scenarios

Scenario 1: Initial Communication
- ARP mapping not present  
- Packet is flooded  
- Controller learns mapping  

Scenario 2: Subsequent Communication
- Mapping exists  
- No flooding  
- Direct forwarding using flow rules  

---

## 📸Proof of Execution

1. Ping Results
*** Results: 0% dropped (6/6 received)
   <img width="863" height="479" alt="image" src="https://github.com/user-attachments/assets/5dfc3457-9fc9-45a1-b705-a90969615cd8" />

3. Controller Logs
Learned ARP: 10.0.0.x -> xx:xx
Flow installed
<img width="969" height="489" alt="image" src="https://github.com/user-attachments/assets/301177c2-78cb-4ecf-a5da-95361e47beb5" />

5. Flow Table
sh ovs-ofctl dump-flows s1
<img width="1385" height="126" alt="image" src="https://github.com/user-attachments/assets/8c1196f1-d260-45e5-8759-e8e04d0e0530" />

6. Throughput Test
iperf h1 h2
<img width="753" height="256" alt="image" src="https://github.com/user-attachments/assets/25c441c6-3f3d-455d-a4ec-dbfe0d0d6443" />


## 📊 Performance Analysis

- Initial packets trigger controller involvement (PacketIn events)  
- Flow rules are dynamically installed in the switch  
- Subsequent packets bypass the controller  
- Reduced ARP broadcast traffic  
- Lower latency after learning phase  
- Stable throughput observed using iperf  

---

## 📈 Results

- Successful controller–switch interaction  
- Correct implementation of match–action flow rules  
- Reduced network flooding  
- Improved forwarding efficiency  

---

## 👨‍💻 Conclusion

This project demonstrates how SDN enables intelligent network control by separating the control plane from the data plane. By handling ARP at the controller, unnecessary broadcast traffic is reduced, improving network efficiency and performance.

---

## 🚀 Future Enhancements

- Implement firewall rules (traffic filtering)  
- Extend to multi-switch topology  
- Add QoS (Quality of Service)  
- Integrate monitoring and analytics  

---

## 📚 References

- Mininet Documentation  
- POX Documentation  
- OpenFlow Switch Specification  
