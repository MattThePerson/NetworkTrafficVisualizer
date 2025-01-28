from typing import Any
import scapy.all as scapy
import json


def packet_to_json(packet: scapy.Packet) -> dict[str, Any] | None:
    obj = None
    for layer in reversed(packet.layers()):
        curr_obj = packet[layer].fields
        if obj:
            curr_obj['payload'] = obj
        obj = curr_obj
    obj = json.loads(json.dumps(obj, default=str))
    return obj


def scapy_packet_to_json(packet: scapy.Packet) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    obj['summary'] = packet.summary()
    obj['sniffed_on'] = str(packet.sniffed_on)
    obj['time'] = packet.time
    obj['len'] = len(bytes(packet))
    obj['hex'] = bytes(packet).hex()
    obj['json'] = packet_to_json(packet)
    return obj


def packet_sniffer(queue: Any):
    def handle_packet(packet: scapy.Packet):
        packet_obj = scapy_packet_to_json(packet)
        if packet_obj:
            queue.put(packet_obj)
    
    scapy.sniff(
        prn=handle_packet,
        store=False,
        filter=None,
        iface=None,
    )