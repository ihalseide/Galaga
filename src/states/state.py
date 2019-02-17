class _State(object):
    def __init__(self):
        self.persist = {}
        self.next = None
        self.done = False
        self.quit = False

    def startup(self, persist={}):
        self.persist = persist

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        pass

    def update(self, dt, keys):
        pass

    def display(self, surf, dt):
        pass
