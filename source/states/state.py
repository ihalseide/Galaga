class _State(object):
    def __init__(self):
        self.start_time = None
        self.current_time = 0
        self.persist = {}
        self.next = None
        self.done = False
        self.quit = False

    def startup(self, time, persist={}):
        self.current_time = self.start_time = time
        self.persist = persist

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        pass

    def update(self, dt, keys):
        """
        Should be called by subclasses that want time.
        """
        self.current_time += dt

    def display(self, surf, dt):
        pass
