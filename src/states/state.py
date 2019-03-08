class _State(object):
    def __init__(self, persist={}):
        self.persist = persist
        self.next = None
        self.done = False
        self.quit = False

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        pass

    def update(self, dt, keys):
        pass

    def display(self, surf, dt):
        pass
