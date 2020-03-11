__author__ = "Izak Halseide"

import random
from typing import Tuple, List

import pygame

from data import constants as c

# Constants for just the stars
NUM_OF_RANDOM_STARS = 64
# blue is in the list twice so that it is  selected more often
LAYERS = (
    {'speed': 0.060, 'colors': (pygame.Color("red"), pygame.Color("lightgreen"))},
    {'speed': 0.100, 'colors': (pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('white'))}
)

# true = on, false = off
TWINKLING_PHASES = [{True: 150, False: 140},
                    {True: 210, False: 200},
                    {True: 310, False: 300},
                    {True: 410, False: 300},
                    {True: 510, False: 300}]


class Star(object):
    """
    A star object, that has color, moves, and takes up a single pixel
    """

    def __init__(self, loc: Tuple[int, int], color, layer: int, twinkle_phase: int = 0):
        self.x: float = loc[0]
        self.y: float = loc[1]
        self.color: pygame.Color = color
        self.layer: int = layer
        self.show: bool = True
        self.twinkle_phase: int = twinkle_phase
        self.pixel_location = None

    def update(self, dt, move=1):
        if move:
            # update position
            speed = LAYERS[self.layer]['speed']
            new_y = self.y + speed * dt * move
            new_y = new_y % c.GAME_HEIGHT  # wrap around screen
            self.y = new_y
        self.pixel_location = round(self.x), round(self.y)

    def draw(self, screen):
        screen.set_at(self.pixel_location, self.color)


def random_star(rng: random.Random = random) -> Star:
    x = rng.randint(0, c.GAME_WIDTH)
    y = rng.randint(0, c.GAME_HEIGHT)
    layer = rng.randint(0, len(LAYERS) - 1)
    color = rng.choice(LAYERS[layer]['colors'])
    phase = rng.randint(0, len(TWINKLING_PHASES) - 1)
    return Star((x, y), color=color, layer=layer, twinkle_phase=phase)


class Stars(object):
    """
    Aesthetic stars for the background
    """

    def __init__(self):
        self.rng = random.Random()
        self.rng.seed(101)
        self._moving: int = 1
        self._stars: List[Star] = [random_star(self.rng) for _ in range(NUM_OF_RANDOM_STARS)]
        self.twinkling_timers: List[int] = [0 for _ in TWINKLING_PHASES]
        self.shown_twinkling_phases: List[bool] = [True for _ in TWINKLING_PHASES]

    def set_moving(self, direction: int):
        if direction < 0:
            self._moving = -1
        elif direction > 0:
            self._moving = 1
        else:
            self._moving = 0

    def update(self, dt):
        for s in self._stars:
            s.update(dt, self._moving)
        # update twinkling timers
        for i in range(len(self.twinkling_timers)):
            self.twinkling_timers[i] += dt
            if self.shown_twinkling_phases[i] and self.twinkling_timers[i] >= TWINKLING_PHASES[i][True]:
                self.twinkling_timers[i] = 0
                self.shown_twinkling_phases[i] = False
            elif not self.shown_twinkling_phases[i] and self.twinkling_timers[i] >= TWINKLING_PHASES[i][False]:
                self.twinkling_timers[i] = 0
                self.shown_twinkling_phases[i] = True

    def display(self, screen):
        for star in self._stars:
            if self.shown_twinkling_phases[star.twinkle_phase]:
                star.draw(screen)
