import scapy.all as scapy


def handle_packet(packet, queue):
    # print(packet.summary())
    queue.put(packet)


def packet_sniffer(queue):
    scapy.sniff(
        prn=lambda packet: handle_packet(packet, queue),
        store=False,
        filter=None,
        iface=None,
    )