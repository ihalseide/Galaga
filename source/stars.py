import random
from collections import namedtuple
from dataclasses import dataclass

from . import constants as c

NUM_OF_RANDOM_STARS = 64

StarLayer = namedtuple("StarLayer", "speed colors")


@dataclass
class TwinklingPhase:
    on_time: int
    off_time: int
    current_time: int = 0
    is_shown: bool = True


LAYERS = StarLayer(0.050, (c.RED, c.LIGHT_GREEN)), \
         StarLayer(0.075, (c.YELLOW, c.BLUE, c.WHITE))

TWINKLING_PHASES = TwinklingPhase(150, 140), TwinklingPhase(210, 200), TwinklingPhase(310, 300), \
                   TwinklingPhase(410, 300), TwinklingPhase(510, 300)


@dataclass
class Star:
    """
    A star particle, that has color, moves, and takes up a single pixel
    """
    start_x: int
    start_y: float
    color: tuple
    layer_num: int
    twinkle_phase: int
    speed: float
    show: bool = True


def random_star() -> Star:
    x = random.randint(0, c.GAME_SIZE.width)
    y = random.randint(0, c.GAME_SIZE.height)
    layer = random.randint(0, len(LAYERS) - 1)
    color = random.choice(LAYERS[layer].colors)
    phase = random.randint(0, len(TWINKLING_PHASES) - 1)
    return Star(x, y, color, layer, phase, speed=LAYERS[layer].speed)


class StarField:
    """
    Aesthetic stars for the background
    """

    def __init__(self):
        self._moving: int = 1
        self.stars = [random_star() for _ in range(NUM_OF_RANDOM_STARS)]
        self.twinkling_timers = [phase for phase in TWINKLING_PHASES]
        self.current_time = 0

    @property
    def moving(self) -> int:
        return self._moving

    @moving.setter
    def moving(self, direction: int):
        if direction < 0:
            self._moving = -1
        elif direction > 0:
            self._moving = 1
        else:
            self._moving = 0

    def update(self, delta_time: int):
        self.current_time += delta_time
        # update each timer
        for timer in self.twinkling_timers:
            timer.current_time += delta_time
            if timer.is_shown and timer.current_time >= timer.on_time:
                timer.current_time = 0
                timer.is_shown = False
            elif not timer.is_shown and timer.current_time >= timer.off_time:
                timer.current_time = 0
                timer.is_shown = True

    def display(self, screen):
        for star in self.stars:
            is_shown = self.twinkling_timers[star.twinkle_phase].is_shown
            if is_shown:
                y = round((star.start_y + (star.speed * self.current_time * self._moving)) % c.GAME_SIZE.height)
                screen.set_at((star.start_x, y), star.color)
