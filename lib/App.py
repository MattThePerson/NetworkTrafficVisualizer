from typing import Any
import time

class App:
    
    def __init__(self, ups_target: int):
        self.ups_target: int = ups_target
        self.is_running = True
        self.paused = False
        self.show_debug_menu = False
        self.update_count = 0
        
        self.start_time: float
        self.last_wakeup_time: float
        self.update_time_taken: float


    def start(self):
        self.start_time = time.time()
        self.last_wakeup_time = self.start_time

    def stop(self):
        self.is_running = False


    def running(self):
        return self.is_running


    def sleep(self):
        self.update_time_taken = time.time() - self.last_wakeup_time
        time_left = 1/self.ups_target - self.update_time_taken
        if time_left > 0:
            time.sleep(time_left)
        self.last_wakeup_time = time.time()
        self.update_count += 1

    def togglePause(self):
        self.paused = not self.paused


    # GETTERS
    def getRenderState(self) -> dict[Any, Any]:
        return {}