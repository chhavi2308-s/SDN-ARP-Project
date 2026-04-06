# SDN-Based ARP Handling using Mininet and POX

## 📌 Problem Statement

In traditional networks, Address Resolution Protocol (ARP) requests are broadcast to all hosts, causing unnecessary network flooding and inefficient bandwidth utilization.

This project implements a Software Defined Networking (SDN) solution where a centralized controller intelligently handles ARP requests by learning IP-to-MAC mappings and reducing broadcast traffic.

---

## 🎯 Objective

* Demonstrate controller–switch interaction using SDN
* Implement ARP packet handling using an OpenFlow controller
* Design match–action flow rules
* Observe and analyze network behavior

---

## 🛠️ Tools & Technologies

* Mininet
* POX
* Open vSwitch (OVS)
* Python

---

## 🏗️ Network Topology

* Single switch topology
* Three hosts (h1, h2, h3) connected to switch (s1)

---

## ⚙️ Setup Instructions

### 1. Install Mininet

```bash
sudo apt update
sudo apt install mininet -y
```

### 2. Install POX Controller

```bash
sudo apt install git -y
git clone https://github.com/noxrepo/pox
cd pox
```

---

## ▶️ Execution Steps

### Step 1: Run Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG arp_controller
```

### Step 2: Run Mininet Topology

```bash
sudo mn --controller=remote --topo=single,3
```

### Step 3: Test Connectivity

```bash
pingall
```

---

## 📊 Expected Output

### Ping Result

```
*** Results: 0% dropped (6/6 received)
```

### Controller Logs

```
Learned ARP: 10.0.0.x -> xx:xx:xx
ARP Reply available
Flow installed + packet forwarded
```

---

## 🧠 Working Explanation

1. When a host sends a packet, the switch forwards it to the controller (Packet-In event).
2. The controller extracts ARP information and stores IP–MAC mappings.
3. If the destination is known:

   * Flow rule is installed in the switch
   * Packet is forwarded directly
4. If the destination is unknown:

   * Packet is flooded
5. Subsequent packets are handled directly by the switch using installed flow rules

---

## 🧪 Test Scenarios

### ✅ Scenario 1: Initial Communication

* ARP request is unknown
* Controller floods the packet
* Mapping is learned

### ✅ Scenario 2: Subsequent Communication

* ARP mapping exists
* No flooding required
* Faster communication

---

## 📸 Proof of Execution

Include screenshots of:

1. Ping results (`pingall`)
2. Controller logs (ARP learning and flow installation)
3. Flow table:

```bash
sudo ovs-ofctl dump-flows s1
```

4. Throughput test:

```bash
iperf h1 h2
```

---

## 📈 Performance Observation

* Reduced ARP flooding after learning phase
* Improved efficiency in subsequent communication
* Faster packet forwarding due to installed flow rules

---

## 📚 References

* Mininet Documentation
* POX Documentation
* OpenFlow Switch Specification

---

## 👨‍💻 Conclusion

This project demonstrates how SDN enables intelligent network management by separating the control plane from the data plane. By implementing ARP handling at the controller, unnecessary broadcast traffic is reduced, leading to improved network efficiency and performance.

---

## 🚀 Future Enhancements

* Implement firewall rules (allow/block traffic)
* Add Quality of Service (QoS) mechanisms
* Extend to multi-switch topologies

---

