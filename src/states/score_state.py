
from .state import _State

class Scored(_State):
    def __init__(self, persist={}):
        _State.__init__(self, persist)
        ...
