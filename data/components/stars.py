# TODO: fix star twinkling
import random
from typing import Tuple, List

import pygame

from .. import constants as c

# Constants for just the stars
NUM_OF_RANDOM_STARS = 58
# blue is in the list twice so that it is  selected more often
LAYERS = (
	{c.SPEED: 60, c.COLORS: (pygame.Color("red"), pygame.Color("lightgreen"))},
	{c.SPEED: 100, c.COLORS: (pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('white'))}
)
TWINKLING_PHASES = [0.2, 0.31, 0.56]

STAR_DATA = (
	('blue', 1, 2),	('blue', 1, 2),	('blue', 1, 2),	('blue', 1, 0),	('blue', 1, 0),	('blue', 1, 0),	('blue', 1, 0),
	('blue', 1, 0),	('blue', 1, 0),	('blue', 1, 2),	('blue', 1, 0),	('blue', 1, 2),	('blue', 1, 1),	('blue', 1, 1),
	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),
	('blue', 1, 1),	('blue', 1, 1),	('blue', 1, 1),
	('yellow', 1, 0), ('yellow', 1, 1),	('yellow', 1, 0), ('yellow', 1, 1), ('yellow', 1, 0), ('yellow', 1, 1),
	('yellow', 1, 0), ('yellow', 1, 1), ('yellow', 1, 0), ('yellow', 1, 1), ('yellow', 1, 0), ('yellow', 1, 1),
	('white', 1, 0), ('white', 1, 2),
	('red', 0, 0), ('red', 0, 0), ('red', 0, 2), ('red', 0, 1), ('red', 0, 0), ('red', 0, 0), ('red', 0, 2),
	('red', 0, 1), ('red', 0, 1), ('red', 0, 0), ('red', 0, 0), ('red', 0, 1),
	('green', 0, 1), ('green', 0, 2), ('green', 0, 1), ('green', 0, 0), ('green', 0, 1), ('green', 0, 2),
	('green', 0, 1), ('green', 0, 2)
)
# print('star data', len(STAR_DATA))


class Star(object):
	"""
	Graphical object for the background
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
			speed = LAYERS[self.layer][c.SPEED]
			new_y = self.y + round(speed * dt * move)
			new_y = new_y % c.GAME_HEIGHT # wrap around screen
			self.y = new_y
		self.pixel_location = round(self.x), round(self.y)

	def draw(self, screen):
		screen.set_at(self.pixel_location, self.color)


def _random_star() -> Star:
	x = random.randint(0, c.GAME_WIDTH)
	y = random.randint(0, c.GAME_HEIGHT)
	layer = random.randint(0, len(LAYERS) - 1)
	color = random.choice(LAYERS[layer][c.COLORS])
	phase = random.randint(0, len(TWINKLING_PHASES))
	return Star((x, y), color=color, layer=layer, twinkle_phase=phase)


def star_from_data_tuple(d: tuple):
	x, y = random.randint(0, c.GAME_WIDTH), random.randint(0, c.GAME_HEIGHT)
	color, layer, phase = d
	return Star((x, y), pygame.Color(color), layer=layer, twinkle_phase=phase)


class Stars(object):

	def __init__(self):
		self._moving: int = 1
		self._stars: List[Star] = [star_from_data_tuple(d) for d in STAR_DATA]
		self.twinkling_timers: List[int] = [0 for x in TWINKLING_PHASES]
		self.shown_twinkling_phases: List[bool] = [True for x in TWINKLING_PHASES]

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
		return
		# for i in range(len(self.twinkling_timers)):
		# 	self.twinkling_timers[i] += dt
		# 	if self.twinkling_timers[i] >= TWINKLING_PHASES[i]:
		# 		self.twinkling_timers[i] = 0
		# 		self.shown_twinkling_phases[i] = not self.shown_twinkling_phases[i]

	def display(self, screen):
		for star in self._stars:
			if self.shown_twinkling_phases[star.twinkle_phase]:
				star.draw(screen)
