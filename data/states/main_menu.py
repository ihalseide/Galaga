#!/usr/bin/env python3
#
# main_menu.py


import pygame

from .. import setup
from .. import constants as c
from .. import scoring
from ..components import stars, hud
from ..tools import font_render
from .state import _State


# A few constants for the menu
LIGHT_TITLE = setup.GFX.get('light title')
GREEN_TITLE = setup.GFX.get('green title')
WHITE_TITLE = setup.GFX.get('white title')
# Positioning on screen
SCORE_Y = 10
TITLE_X = c.GAME_CENTER_X - LIGHT_TITLE.get_rect().width/2
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60
# Timing and speeds
MENU_SPEED = 2
TITLE_FLASH_TIME = 0.15 # seconds
TITLE_FLASH_NUM = 15


class Menu(_State):
	def __init__(self, persist={}):
		_State.__init__(self, persist)
		# init hud
		self.hud = hud.Hud()
		# initialize the stars
		stars.create_stars()
		# next state
		self.next = c.PLAY_STATE
		# whether it is in a scrolling state
		self.is_scrolling = True
		self.timer = 0
		# times the title has flashed
		self.flash_num = 0
		# title is flashing now?
		self.is_flashing = False
		self.is_title_white = False
		self.ready = False
		# scrolling menu up
		self.offset_y = c.GAME_HEIGHT

	def set_ready(self):
		self.ready = True
		self.offset_y = 0
		self.is_flashing = True
		self.flash_num = 0

	def cleanup(self) -> dict:
		self.persist[c.HUD] = self.hud
		return self.persist

	def get_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in setup.START_KEYS:
				if self.ready:
					# start the game
					self.next = c.PLAY_STATE
					self.done = True
				else:
					self.set_ready()

	def update(self, dt, keys):
		# stars
		stars.update(dt)
		# hud
		self.hud.update(dt)
		# scroll menu
		if self.ready:
			# flash timer
			self.is_flashing = self.flash_num < TITLE_FLASH_NUM * 2
			if self.is_flashing:
				self.timer += dt
				if self.timer >= TITLE_FLASH_TIME:
					self.timer = 0
					self.flash_num += 1
					self.is_title_white = not self.is_title_white
			else:
				pass # TODO: make it flash later or invoke demo?
		elif self.offset_y > 0:
			self.offset_y -= MENU_SPEED
			if self.offset_y <= 0:
				self.set_ready()

	def display(self, screen, dt):
		# draw background
		self.hud.display(screen)
		screen.fill((0, 0, 0))
		stars.display(screen)
		# title normal
		if not self.is_flashing:
			surf = LIGHT_TITLE
		elif self.is_title_white:
			surf = WHITE_TITLE
		else:
			surf = GREEN_TITLE
		screen.blit(surf, (TITLE_X, TITLE_Y + self.offset_y))
		# hud
		score_1up = 20210  # TODO: use scoring.get_1up_score()
		highscore = 1000 # TODO: use scoring.get_high_score()
		# draw 1up and high score hud
		self.hud.display_scores(screen, dt, score_1up, highscore, SCORE_Y)
		# draw start text
		txt = font_render('Start', pygame.Color('white'))
		w = txt.get_rect().width
		screen.blit(txt, (c.GAME_CENTER_X - w // 2, self.offset_y + START_Y))
		# draw copyright?
		txt = font_render('-Copyright or whatever-', pygame.Color('white'))
		w = txt.get_rect().width
		screen.blit(txt, (c.GAME_CENTER_X - w // 2, self.offset_y + COPY_Y))
