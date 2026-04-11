from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import arp

log = core.getLogger()

arp_table = {}
mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    in_port = event.port

    if not packet:
        return

    # Learn MAC → Port
    mac_to_port[packet.src] = in_port

    # Handle ARP
    if packet.type == packet.ARP_TYPE:
        a = packet.payload

        arp_table[a.protosrc] = a.hwsrc
        log.info("Learned ARP: %s -> %s", a.protosrc, a.hwsrc)

        if a.protodst in arp_table:
            log.info("ARP Reply available for %s", a.protodst)
        else:
            log.info("Unknown destination, flooding")

    # Forwarding logic
    if packet.dst in mac_to_port:
        out_port = mac_to_port[packet.dst]

        # Install flow rule
        msg = of.ofp_flow_mod()
        msg.match.dl_dst = packet.dst

        # ⭐ IMPROVEMENTS
        msg.priority = 10
        msg.idle_timeout = 30
        msg.hard_timeout = 60

        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

        # Send current packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

        log.debug("Flow installed + packet forwarded")

    else:
        # Flood
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("ARP + Forwarding Controller Started")
