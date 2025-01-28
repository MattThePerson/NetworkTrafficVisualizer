import argparse
import multiprocessing
import signal
from lib import AppState
from lib import CursesRenderer
from lib import App
from lib import packet_sniffer



# MAIN
def main(args):
    
    app = App(ups_target=60)
    state = AppState()
    renderer = CursesRenderer()
    queue = multiprocessing.Queue() # messages from sniffer process
    sniffer_process = multiprocessing.Process(
        target=packet_sniffer,
        args=(queue,)
    )

    signal.signal(signal.SIGINT, lambda s, f: app.stop()) # handle ctrl+c
    
    # start shit
    sniffer_process.start()
    renderer.init()
    app.start()
    
    # update loop
    while app.running():
        
        while not queue.empty():
            state.add_packet(queue.get_nowait())
        
        if not app.paused:
            state.update() # pass in app.time() ?

            renderer.erase()
            renderer.render_screen(state) # 
            renderer.render_header(app.getRenderState()) # app state
            renderer.render_footer()
            
        else:
            renderer.render_pause_overlay()
        
        if app.show_debug_menu:
            renderer.render_debug_menu()
        renderer.refresh()
        renderer.handle_input(toggle_pause_func=app.togglePause, stop_app_func=app.stop) # pause, refresh (state), toggle mode
        
        app.sleep()

    # end shit
    renderer.end()
    sniffer_process.terminate()
    sniffer_process.join()
    print('App closed. Goodbye!')




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Python script for visualizing the flow of traffic over your network!")

    # filter
    parser.add_argument("--iface", help="")
    parser.add_argument("--filter", help="")
    parser.add_argument("--protocol", help="")
    parser.add_argument("--port", help="")
    parser.add_argument("--direction", help="incoming or outgoing packets") # inputs?
    parser.add_argument("--packets-larger-than", help="", type=int)
    parser.add_argument("--packets-smaller-than", help="", type=int)
    
    # display
    parser.add_argument("--vertical", action='store_true', help="") # (maybe not?)
    parser.add_argument("--text-mode", action='store_true', help="list caught packets in a wireshark-esque way")
    parser.add_argument("--fade-time", action='store_true', help="")
    parser.add_argument("--byte-mode", action='store_true', help="represent data stream as bytes instead of bits")
    parser.add_argument("--max-exchange-stacking'", help="max thickness of a 'relationship", type=int)
    parser.add_argument("--non-stacking-mode", action='store_true', help="don't group (stack) exchanges in same relationship")
    parser.add_argument("--no-ip-resolve", action='store_true', help="Dont show IPs resolved names")
    
    # logging
    parser.add_argument("--log-file", help="")
    parser.add_argument("--pcap", help="Export to a .pcap file for later analysis in Wireshark")
    parser.add_argument("--list-ifs", action='store_true', help="")
    parser.add_argument("--simulate-log", action='store_true', help="reads packets from log file and simulates their arrival")

    args = parser.parse_args()
    # print('calling main() ...')
    main(args)