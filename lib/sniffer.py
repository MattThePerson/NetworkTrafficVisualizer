from typing import Any
import scapy.all as scapy
import json

def hex_string_to_binary_string_SUPERFUCKINGOPTIMIZED_ONELINERRRRR(hex_str: str):
    return ''.join([ '{:0>4b}'.format( int(hex_dig, 16)) for hex_dig in hex_str ])


def hex_string_to_binary_string(hex_str: str):
    def hex_digit_to_binary(hex_str: str):
        integer = int(hex_str, 16)
        return '{:0>4b}'.format(integer)
    binary_str = ''
    for hex_digit in hex_str:
        binary_str += hex_digit_to_binary(hex_digit)
    return binary_str


def packet_to_json(packet: scapy.Packet) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    obj['summary'] = packet.summary()
    obj['sniffed_on'] = str(packet.sniffed_on)
    obj['time'] = packet.time
    obj['len'] = len(bytes(packet))
    obj['hex'] = bytes(packet).hex()
    obj['binary'] = hex_string_to_binary_string_SUPERFUCKINGOPTIMIZED_ONELINERRRRR(obj['hex'])
    obj['json'] = json.loads(packet.json())
    return obj


def packet_sniffer(queue: Any):
    def handle_packet(packet: scapy.Packet):
        # print(packet.summary())
        queue.put(packet_to_json(packet))
    
    scapy.sniff(
        prn=handle_packet,
        store=False,
        filter=None,
        iface=None,
    )