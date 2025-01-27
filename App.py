# import curses
import multiprocessing
import signal
import time
import scapy.all as scapy
import sys

from lib import AppState
from lib import CursesRenderer


### HELPER FUNCTIONS ###

def keyboard_interrupt_handler(sig, frame, process, renderer):
    print("Keyboard interrupt received. Closing the sniffer...")
    process.terminate()
    process.join()
    print("Sniffer process terminated.")
    renderer.end()
    sys.exit(0)


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


# APP
def App(args):
    
    queue = multiprocessing.Queue() # messages from sniffer process
    state = AppState()
    renderer = CursesRenderer()
    sniffer_process = multiprocessing.Process(target=packet_sniffer, args=(queue,))

    signal.signal(signal.SIGINT, lambda sig, frame: keyboard_interrupt_handler(sig, frame, sniffer_process, renderer))
    
    # start shit
    sniffer_process.start()

    renderer.init()
    
    # render state
    UPS_target = 60
    start_time = time.time()
    update_count = 0
    pause = False
    show_debug_menu = False
    running = True
    while running:
        
        if not queue.empty():
            packet = queue.get_nowait()
            state.add_packet(packet)
        
        state.update() # updates app state

        renderer.update(state) # 
        renderer.update_header()
        renderer.update_footer()
        
        renderer.handle_input(state, ...) # inputs can affect render state AND app state (refresh)
        renderer.refresh() 
        
        time.sleep(16/1000)
        update_count += 1

    sniffer_process.join()

