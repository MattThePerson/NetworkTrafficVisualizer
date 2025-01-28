from dataclasses import dataclass

@dataclass
class AppState:
    
    packets = []
    exchange_objects = []
    relationships = []
    
    def add_packet(self, packet):
        self.packets.append(packet)
    
    def update(self):
        ...
