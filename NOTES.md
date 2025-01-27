## IDEAS

- relationships (src, dst pairing) given a line and a color in the terminal
- IPs given unique colors
- Shows TCP stage and flags
- visual showing direction of flow (left is down, right is up) and rate determined by size
- keeps track of number of bytes (and up) transfered (number on each side for up and down)
- relationships slowly fade out, and are hydrated upon new 
- DNS resolve ip addr to name

TOP BAR:
- Top bar with uptime, total up/down, selected filters
- bar indicator for how many connections in the last 10 seconds
- recording indicator

BOTTOM BAR:
- showing most recent 'renewed' away ip address

CONTROLS:
- `p` to pause/unpause
- `t` toggle text mode
- `d` show debug menu
- `ctrl+r` refresh

QUESTIONS:
- What about interfaces? how to show? LEARN
- How to determine packet size (packet['IP'].len or len(packet))

- How to define 'home' IPs?
    import ipaddress
    ipaddress.ip_address(ip).is_private

# Options
--iface
--filter
--protocol
--port
--direction  // incoming or outgoing packets
--packets-larger-than
--packets-smaller-than

--no-ip-resolve  // dont reverse DNS resolve IPs
--vertical (maybe not)
--text-mode  // list connections like wireshark
--fade-time
--byte-mode  // represents data stream as bytes instead of bits
--max-exchange-stacking  // max thickness of a 'relationship'
--non-stacking-mode  // don't group (stack) exchanges in same relationship

--log-file  // 
--pcap  // Export to a .pcap file for later analysis in Wireshark
--list-ifs
--simulate-log  // reads packets from log file and simulates their arrival
