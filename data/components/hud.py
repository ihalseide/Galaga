#!/usr/bin/env python3

# hud.py


"""
Code for the shared HUD drawing between the menu state and the play state
"""


import math

import pygame

from .. import constants as c
from ..tools import font_render


BLINK_1UP = 0.45  # seconds


class Hud:
	def __init__(self):
		self._timer_1up = 0
		self._show_1up = True
		self._blinking_1up = False

	def set_blinking_1up(self, value):
		self._blinking_1up = bool(value)

	@staticmethod
	def clear_top(screen):
		pygame.draw.rect(screen, pygame.Color('black'), (0, 0, c.GAME_WIDTH, 20))

	def update(self, dt):
		if self._blinking_1up:
			self._timer_1up += dt
			if self._timer_1up >= BLINK_1UP:
				self._timer_1up = 0
				self._show_1up = not self._show_1up
		else:
			self._show_1up = True

	def display(self, screen):
		pass

	def display_scores(self, screen, dt, score, highscore, offset_y=0):
		if not self._blinking_1up or self._show_1up:
			t = font_render("1 UP", pygame.Color('red'))
			screen.blit(t, (22, 1 + offset_y))
		if score == 0:
			score = "00"
		else:
			score = str(score).zfill(round(math.log(score, 10)))
		t = font_render(score, pygame.Color('white'))
		w = t.get_rect().width
		screen.blit(t, (60-w, 10 + offset_y))
		t = font_render("HI-SCORE", pygame.Color('red'))
		size = t.get_rect().width
		screen.blit(t, ((c.GAME_WIDTH - size)//2, 1 + offset_y))
		score = str(highscore)
		t = font_render(score, pygame.Color('white'))
		size = t.get_rect().width
		screen.blit(t, ((c.GAME_WIDTH - size)//2, 10 + offset_y))
