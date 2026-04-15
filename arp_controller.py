# ============================================
# SDN ARP Handling Controller (FULL VERSION)
# Features:
# - ARP Interception
# - ARP Reply Generation (Controller-based)
# - Host Discovery
# - Flow Rule Installation
# ============================================

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, arp

log = core.getLogger()

# Tables
arp_table = {}      # IP -> MAC
mac_to_port = {}    # MAC -> Port


def _handle_PacketIn(event):
    packet = event.parsed
    in_port = event.port

    if not packet:
        return

    # Learn MAC -> Port
    mac_to_port[packet.src] = in_port

    # ============================================
    # 🔹 ARP HANDLING
    # ============================================
    if packet.type == ethernet.ARP_TYPE:
        a = packet.payload

        # Learn IP -> MAC
        arp_table[a.protosrc] = a.hwsrc
        log.info("Learned ARP: %s -> %s", a.protosrc, a.hwsrc)

        # ========================================
        # 🔹 IF REQUEST → GENERATE REPLY
        # ========================================
        if a.opcode == arp.REQUEST:

            if a.protodst in arp_table:
                log.info("Generating ARP reply for %s", a.protodst)

                # Create ARP reply
                arp_reply = arp()
                arp_reply.opcode = arp.REPLY
                arp_reply.hwsrc = arp_table[a.protodst]   # MAC of destination
                arp_reply.hwdst = a.hwsrc                # requester MAC
                arp_reply.protosrc = a.protodst          # destination IP
                arp_reply.protodst = a.protosrc          # requester IP

                # Wrap in Ethernet frame
                eth = ethernet()
                eth.type = ethernet.ARP_TYPE
                eth.src = arp_reply.hwsrc
                eth.dst = arp_reply.hwdst
                eth.payload = arp_reply

                # Send reply back
                msg = of.ofp_packet_out()
                msg.data = eth.pack()
                msg.actions.append(of.ofp_action_output(port=in_port))
                event.connection.send(msg)

                return
            else:
                log.info("Unknown ARP target, flooding")

    # ============================================
    # 🔹 NORMAL FORWARDING LOGIC
    # ============================================
    if packet.dst in mac_to_port:
        out_port = mac_to_port[packet.dst]

        # Install flow rule
        flow = of.ofp_flow_mod()
        flow.match.dl_dst = packet.dst

        flow.priority = 10
        flow.idle_timeout = 30
        flow.hard_timeout = 60

        flow.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(flow)

        # Send current packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

        log.debug("Flow installed + packet forwarded")

    else:
        # Flood if unknown
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("✅ Advanced ARP Controller Started (Reply Enabled)")
