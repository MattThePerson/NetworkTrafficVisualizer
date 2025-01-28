from typing import Any
import math
import random


class AppState:
    
    max_packets = 1000
    
    def __init__(self):
        self.packets: list[Any] = [None] * self.max_packets
        self.packets_idx = 0
        self.exchange_objects: list[dict[str, Any]] = []
        self.relationships: list[dict[str, Any]] = []
        self.used_colors = []
        
        self.packet_speed = 120 # chars / s
    
    def add_packet(self, packet: dict[str, Any]):
        idx = self.add_packet_to_memory(packet)
        binary_data = self.hex_string_to_binary_string(packet['hex'])
        exch_obj: dict[str, Any] = {
            'packet_idx': idx,
            'hex': list(reversed(packet['hex'])),
            'binary': list(reversed(binary_data)),
            'speed': self.packet_speed + random.randint(-30, 30),
            'chars_to_print': len(binary_data),
            'color': self.get_random_color(),
            'show_data': '',
            'show_idx': 0, # float
        }
        self.exchange_objects.append(exch_obj)
    
    
    def update(self):
        # return
        max_width = 90
        for eo in self.exchange_objects:
            idx = math.floor(eo['show_idx'])
            eo['show_idx'] += eo['speed'] / 60 # need to know time or UPS or something
            while idx < math.floor(eo['show_idx']) and idx < len(eo['binary']):
                eo['show_data'] = eo['binary'][idx] + eo['show_data']
                idx += 1
            eo['show_data'] = eo['show_data']

    def add_packet_to_memory(self, packet: dict[str, Any]) -> int:
        idx = self.packets_idx
        self.packets[idx] = packet
        self.packets_idx += 1
        if self.packets_idx >= self.max_packets:
            self.packets_idx = 0
        return idx
    
    
    def get_random_color(self):
        return (50, 190, 130)
    
    #region STATIC METHODS
    @staticmethod
    def hex_string_to_binary_string(hex_str: str):
        return ''.join([ '{:0>4b}'.format( int(hex_dig, 16)) for hex_dig in hex_str ])


    #endregion
