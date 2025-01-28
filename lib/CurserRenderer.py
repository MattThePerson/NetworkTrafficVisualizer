import sys

try:
    import curses
except ImportError:
    if sys.platform == "win32":
        raise ImportError(
            "The 'curses' module is required. Please install the 'windows-curses' package on Windows."
        )
    else:
        raise
# import curses

class CursesRenderer():
    
    initialized = False
    
    def init(self):
        self.initialized = True
        self.screen = curses.initscr()
        curses.curs_set(0)
        self.screen.nodelay(True)
        self.screen.addstr(0, 0, 'HELLOOOO')

        self.rows, self.cols = self.screen.getmaxyx()
        self.updates_count = 0
        
    def update(self, state):
        self.screen.addstr(1, 0, "size: " + str((self.rows, self.cols)))
        self.screen.addstr(2, 0, "Try Russian text: Привет")
        self.screen.addstr(3, 0, str(self.updates_count))
        self.screen.addstr(4, 0, str(len(state.packets)))
        
        for idx, packet in enumerate(state.packets[-30:]):
            self.screen.addstr(6+idx, 0, packet.summary())
        
        self.updates_count += 1
    
    def handle_input(self):
        ...
    
    def refresh(self):
        self.screen.refresh()
    
    def update_header(self, render_state):
        ...
    
    def update_footer(self):
        ...
    
    def end(self):
        if self.initialized:
            curses.endwin() # dunno what this does
