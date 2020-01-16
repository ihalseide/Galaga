#!/usr/bin/env python3

# hud.py


"""
Code for the shared HUD drawing between the menu state and the play state
"""


import math

import pygame

from .. import constants as c
from ..tools import font_render


BLINK_1UP = 0.45 # seconds


class Hud:
	def __init__(self):
		self._timer_1up = ToggleTicker(BLINK_1UP)  # TODO: fix the blinking without a complicated class to do it
		self._blinking_1up = False

	def set_blinking_1up(self, value):
		self._blinking_1up = bool(value)

	@staticmethod
	def clear_top(screen):
		pygame.draw.rect(screen, pygame.Color('black'), (0, 0, c.GAME_WIDTH, 20))

	def display_scores(self, screen, dt, score, highscore, offset_y=0):
		self._timer_1up.update(dt)
		if not self._blinking_1up or self._timer_1up.on:
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
