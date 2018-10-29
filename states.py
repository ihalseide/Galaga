
import math
import random

import pygame
from pygame.math import Vector2

import score
import resources as r
import game_objects as gobs
import constants as c

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

class StartState(_State):
    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)

        self.scores = score.get_scores()

        state = None
        print("Scores", "    {} . . . {}".format(*self.scores[0]), sep="\n")

class ScoreState(_State):
    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)
        ...
