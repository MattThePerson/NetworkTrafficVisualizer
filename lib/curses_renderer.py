from typing import Any, Callable
import time
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
        # self.screen.timeout(1) # necessary?
        self.rows, self.cols = self.screen.getmaxyx()
        
        # self.colors = [ curses.init_pair(i, i, i) for i in range(1, 10) ]
        self.colors = [ curses.init_pair(i+10, col, curses.COLOR_BLACK) for i, col in enumerate(some_colors) ]
        
        self.footer_color_number = 2
        curses.init_pair(self.footer_color_number, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    
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
        self.screen.addstr(3, 0, str(len(state.exchange_objects)))
        
        for idx, eo in enumerate(state.exchange_objects[-80:]):
            color_pair_num = idx % len(self.colors) + 10
            self.putstr(6+idx, 0, eo['show_data'], curses.color_pair(color_pair_num))
        
    def render_header(self, app: Any):
        ...
    
    def render_footer(self, app: Any):
        proc_tt_ms = round(app.compute_tt_mean * 1000, 1)
        ups = -1
        if app.update_count > 0:
            ups = round( app.update_count / (time.time() - app.start_time) ,1)
        string = ' uc={:<7} ups={:<4} proc_tt={:<5}ms'.format( app.update_count, ups, proc_tt_ms)
        string += ' ' * self.cols
        self.putstr(-1, 0, string, curses.color_pair(self.footer_color_number))
    
    
    def render_debug_menu(self, app: Any):
        ...
    
    def render_pause_overlay(self):
        self.putstr(5, 5, 'PAUSED')
    
    #endregion

    #region helpers
    
    def putstr(self, y: int, x: int, to_write: str, col=None):
        if to_write == '':
            return
        if y < 0:   y = self.rows + y
        if x < 0:   x = self.cols + x
        to_write = str(to_write)[:(self.cols-1-x)]
        args = (y, x, to_write, col) if col else (y, x, to_write)
        self.screen.addstr(*args) # type: ignore
    
    #endregion