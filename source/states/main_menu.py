
from .state import _State
from .. import scoring

class Menu(_State):
    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)

        self.scores = scoring.get_scores()

        state = None
        print("Scores", "    {} . . . {}".format(*self.scores[0]), sep="\n")
