from typing import Any
import argparse
from multiprocessing import Process, Queue
import signal
import time
from lib import AppState
from lib import CursesRenderer
from lib import App
from lib import packet_sniffer


# MAIN
def main(args: argparse.Namespace):
    
    app = App(ups_target=60)
    state = AppState()
    renderer = CursesRenderer()
    
    sniffer_messages: Queue[Any] = Queue() # messages from sniffer process
    sniffer_process = Process(
        target=packet_sniffer,
        args=(sniffer_messages,)
    )

    # start shit
    sniffer_process.start()
    
    if args.text_mode:
        text_mode(sniffer_messages)
    else:
        gui_mode(app, state, renderer, sniffer_messages)
    
    sniffer_process.terminate()
    sniffer_process.join()
    print('App closed. Goodbye!')



# GUI MODE
def gui_mode(app: App, state: AppState, renderer: CursesRenderer, sniffer_messages: Any):
    """ Sniffer messages is of type multiprocess.Queue[dict[str, Any]] """
    signal.signal(signal.SIGINT, lambda s, f: app.stop()) # handle ctrl+c
    
    renderer.init()
    app.start()
    
    # update loop
    while app.running():
        
        while not sniffer_messages.empty():
            state.add_packet(sniffer_messages.get_nowait()) # why nowait?
        
        if not app.paused:
            state.update() # pass in app.time() ?

            renderer.erase()
            renderer.render_screen(state) # 
            renderer.render_header(app)
            renderer.render_footer(app)
            
        else:
            renderer.render_pause_overlay()
        
        if app.show_debug_menu:
            renderer.render_debug_menu(app)
        
        renderer.refresh()
        renderer.handle_input(toggle_pause_func=app.togglePause, stop_app_func=app.stop) # pause, refresh (state), toggle mode
        
        app.sleep()

    # end shit
    renderer.end()
    return



# TEXT MODE
def text_mode(sniffer_messages: Any):
    """ Sniffer messages is of type multiprocess.Queue[dict[str, Any]] """
    print('Listening for packets ...')
    try:
        while True:
            while not sniffer_messages.empty():
                packet_obj = sniffer_messages.get()
                print(packet_obj['summary'])
            time.sleep(1/60)
    except KeyboardInterrupt:
        print('\n... interrupted with CTRL-C')
        return




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Python script for visualizing the flow of traffic over your network right in the terminal!")

    # filter
    parser.add_argument("--iface", help="")
    parser.add_argument("--filter", help="")
    parser.add_argument("--protocol", help="")
    parser.add_argument("--port", help="")
    parser.add_argument("--incoming-only", action="store_true", help="incoming or outgoing packets")
    parser.add_argument("--outgoing-only", action="store_true", help="incoming or outgoing packets")
    parser.add_argument("--packets-larger-than", help="", type=int)
    parser.add_argument("--packets-smaller-than", help="", type=int)
    parser.add_argument("--count", help="", type=int)
    
    # display
    parser.add_argument("--text-mode", action="store_true", help="list caught packets in a wireshark-esque way")
    parser.add_argument("--fade-time", action="store_true", help="")
    parser.add_argument("--byte-mode", action="store_true", help="represent data stream as bytes instead of bits")
    parser.add_argument("--max-exchange-stacking'", help="max thickness of a 'relationship", type=int)
    parser.add_argument("--non-stacking-mode", action="store_true", help="don't group (stack) exchanges in same relationship")
    parser.add_argument("--no-ip-resolve", action="store_true", help="Dont show IPs resolved names")
    
    # logging
    parser.add_argument("--log-file", help="")
    parser.add_argument("--pcap", help="Export to a .pcap file for later analysis in Wireshark")
    parser.add_argument("--list-ifs", action="store_true", help="")
    parser.add_argument("--simulate-log", action="store_true", help="reads packets from log file and simulates their arrival")

    args = parser.parse_args()
    # print('calling main() ...')
    main(args)