# Network Traffic Visualizer!

_Visualize network connections in a colorful TUI_

## Description

Your computer is constantly making connections on the network. This TUI (Terminal User Interface) visualizes connections as they happen, grouping together packets to/from to the same IP and showing the literal 1s and 0s flow accross the screen. Unique connections have their own color to distinguish them and the attributes of the connection such as amount of data and frequency of connections are indicated with faster flow of bits and larger grouping of connections.

## Running

Because this tool sniffs network packets it requires admin privileges.

**First-time setup** — run once from the project root to create a virtual environment and install dependencies:

```bash
# Linux / macOS
./tools/install.sh

# Windows (PowerShell)
.\tools\install.ps1
```

**Run the app** — requires elevated privileges:

```bash
# Linux / macOS
sudo ./tools/run.sh

# Windows (PowerShell — open as Administrator)
.\tools\run.ps1
```

## Options

```sh
--iface
--filter
--protocol
--port
--direction             // incoming or outgoing packets
--packets-larger-than
--packets-smaller-than

--no-ip-resolve             // dont reverse DNS resolve IPs
--vertical                  // display connections vertically
--text-mode                 // list connections like wireshark
--fade-time
--byte-mode                 // represents data stream as bytes instead of bits
--max-exchange-stacking     // max thickness of a 'relationship'
--non-stacking-mode         // dont group or stack exchanges in same relationship

--log-file
--pcap                      // Export to a .pcap file for later analysis in Wireshark
--list-ifs
--simulate-log              // reads packets from log file and simulates their arrival
```
