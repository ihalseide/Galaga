#!/usr/bin/env python3

# hud.py


"""
Code for the shared HUD drawing between the menu state and the play state
"""

import pygame

from .. import constants as c
from .. import tools

BLINK_1UP = 0.45  # seconds


class Hud:
	def __init__(self, display_score: int, high_score: int):
		self._display_score = int(display_score)
		self._high_score = int(high_score)

	def set_display_score(self, score):
		self._display_score = score

	def set_display_high_score(self, score: int):
		self._high_score = score

	def update(self, dt: float):
		pass

	def display(self, screen, offset_y=0):
		# 1UP score
		score_string = "{: =6}".format(self._display_score)
		tools.draw_text(screen, "1UP", (20, 10 + offset_y), pygame.Color('red'))
		tools.draw_text(screen, score_string, (20, 20 + offset_y), pygame.Color('white'))
		# high score
		high_score_string = "{: =6}".format(self._high_score)
		tools.draw_text(screen, "HI-SCORE", (c.GAME_CENTER_X, 10 + offset_y), pygame.Color('red'), centered_x=True)
		tools.draw_text(screen, high_score_string, (83, 20 + offset_y), pygame.Color('white'))
