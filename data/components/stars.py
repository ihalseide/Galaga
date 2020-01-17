#!/usr/bin/env python3
import random

import pygame

from .. import constants as c

# Constants for just the stars
NUM = 90
# blue is in the list twice so that it is selected more often
COLORS = (pygame.Color("red"), pygame.Color("blue"), pygame.Color("blue"), pygame.Color("lightgreen"), pygame.Color(
	"white"))
LAYERS = 2
PHASES = [0, 0.25, 0.1]


class _Star(object):
	"""
	Graphical object for the background
	"""
	speeds = 30, 65
	show_time = 0.4  # seconds
	hide_time = 0.2

	def __init__(self, loc, color, z, twinkles=False, time_offset=0):
		self.loc = tuple(loc)
		self.color = color
		self.z = z
		self.show = True
		self.twinkles = twinkles
		self.timer = time_offset

	def update(self, dt, move=1):
		if move:
			new_y = self.loc[1] + round(self.speeds[self.z] * dt * move)
			if new_y > c.GAME_HEIGHT:
				new_y = 0
			elif new_y < 0:
				new_y = c.GAME_HEIGHT
			self.loc = self.loc[0], new_y
		if self.twinkles:
			if self.show and self.timer >= self.show_time:
				self.show = False
				self.timer = 0
			elif not self.show and self.timer >= self.hide_time:
				self.show = True
				self.timer = 0
			self.timer += dt

	def draw(self, screen):
		if self.show:
			r_loc = [round(a) for a in self.loc]
			screen.set_at(r_loc, self.color)


def _random_star() -> _Star:
	x = random.randint(0, c.GAME_WIDTH)
	y = random.randint(0, c.GAME_HEIGHT)
	col = random.choice(COLORS)
	z = random.randint(0, LAYERS - 1)
	t = random.choice(PHASES)
	b = True  # bool(random.randint(0,1))
	return _Star((x, y), color=col, z=z, twinkles=b, time_offset=t)


class Stars(object):

	def __init__(self, num: int = NUM):
		self._num_stars = num
		self._moving = 1
		self._stars = [_random_star() for i in range(self._num_stars)]

	def update(self, dt):
		for s in self._stars:
			s.update(dt, self._moving)

	def set_moving(self, value: int):
		if value < 0:
			self._moving = -1
		elif value > 0:
			self._moving = 1
		else:
			# error, but default to 0
			self._moving = 0

	def display(self, screen):
		for s in self._stars:
			s.draw(screen)
