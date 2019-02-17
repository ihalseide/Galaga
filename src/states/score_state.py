
from .state import _State

class Scored(_State):
    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)
        ...
