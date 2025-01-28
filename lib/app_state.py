from typing import Any


class AppState:
    
    def __init__(self):
        self.packets: list[dict[str, Any]] = []
        self.exchange_objects = []
        self.relationships = []
    
    def add_packet(self, packet: dict[str, Any]):
        self.packets.append(packet)
    
    def update(self):
        ...
