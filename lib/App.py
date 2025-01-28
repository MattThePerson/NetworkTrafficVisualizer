from typing import Any
import numpy as np
import time

class App:
    
    def __init__(self, ups_target: int):
        self.ups_target: int = ups_target
        self.is_running = True
        self.paused = False
        self.show_debug_menu = False
        self.update_count = 0
        
        self.start_time: float = 0
        self.last_wakeup_time: float
        self.compute_tt_arr: list[float] = [0] # time taken in seconds to
        self.compute_tt_mean: float = 0


    def start(self):
        self.start_time = time.time()
        self.last_wakeup_time = self.start_time

    def stop(self):
        self.is_running = False


    def running(self):
        return self.is_running


    def sleep(self):
        comp_tt = time.time() - self.last_wakeup_time
        self.compute_tt_arr.append(comp_tt)
        if len(self.compute_tt_arr) > 5: # rolling mean window size
            self.compute_tt_arr.pop(0)
        self.compute_tt_mean = float(np.mean(self.compute_tt_arr))

        time_left = 1/self.ups_target - comp_tt
        if time_left > 0:
            time.sleep(time_left)
        self.last_wakeup_time = time.time()
        self.update_count += 1

    def togglePause(self):
        self.paused = not self.paused
