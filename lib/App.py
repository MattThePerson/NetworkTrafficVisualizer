import time

class App:
    
    def __init__(self, ups_target):
        self.ups_target = ups_target
        self.is_running = True
        self.paused = False
        self.show_debug_menu = False
        
        self.start_time = None
        self.update_count = 0


    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.is_running = False


    def running(self):
        return self.is_running


    def sleep(self):
        self.update_count += 1
        time.sleep(16/1000)

    def togglePause(self):
        self.paused = not self.paused


    # GETTERS
    def getRenderState(self):
        return {}