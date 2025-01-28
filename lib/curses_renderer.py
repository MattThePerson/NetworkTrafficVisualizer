from typing import Any, Callable
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

# CRAP
some_colors = [curses.COLOR_RED, curses.COLOR_GREEN,
            curses.COLOR_YELLOW, curses.COLOR_BLUE, curses.COLOR_MAGENTA,
            curses.COLOR_CYAN, curses.COLOR_WHITE]



class CursesRenderer():
    
    initialized = False
    
    def init(self):
        self.initialized = True
        self.screen = curses.initscr()
        curses.start_color()
        curses.curs_set(0)
        self.screen.nodelay(True)
        self.screen.timeout(1)
        self.rows, self.cols = self.screen.getmaxyx()
        self.updates_count = 0 # REMOVE!!!
        
        # self.colors = [ curses.init_pair(i, i, i) for i in range(1, 10) ]
        self.colors = [ curses.init_pair(i+1, col, curses.COLOR_BLACK) for i, col in enumerate(some_colors) ]
    
    def handle_input(self, toggle_pause_func: Callable[..., Any], stop_app_func: Callable[..., Any]):
        key = self.screen.getch()
        if key == ord('q'):
            stop_app_func()
        elif key == ord('p'):
            toggle_pause_func()
        elif key == ord('t'):
            ...
            # toggle mode
        elif key == ord('d'):
            ...
            # toggle debug menu
    
    def refresh(self):
        self.screen.refresh()
    
    def erase(self):
        self.screen.erase()
    
    def end(self):
        if self.initialized:
            curses.endwin() # dunno what this does
    
    #region renderers
    
    def render_screen(self, state: Any):
        self.screen.addstr(1, 0, "size: " + str((self.rows, self.cols)))
        self.screen.addstr(2, 0, "Try Russian text: Привет")
        self.screen.addstr(3, 0, str(self.updates_count))
        self.screen.addstr(4, 0, str(len(state.exchange_objects)))
        
        for idx, eo in enumerate(state.exchange_objects[-90:]):
            color_pair_num = idx % len(self.colors) + 1
            self.screen.addstr(6+idx, 0, eo['show_data'][:self.cols], curses.color_pair(color_pair_num))
        
        self.updates_count += 1

    def render_header(self, render_state: dict[str, Any]):
        ...
    
    def render_footer(self):
        ...
        
    def render_debug_menu(self):
        ...
    
    def render_pause_overlay(self):
        self.putstr(5, 5, 'PAUSED')
    
    #endregion

    #region helpers
    
    def putstr(self, *args: Any):
        self.screen.addstr(*args)
    
    #endregion