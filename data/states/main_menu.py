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


def display_stars_bg(screen):
	# draw background
	screen.fill((0,0,0))
	stars.display(screen)


def display_menu_hud(screen, dt, offset_y=0):
	score_1up = scoring.get_1up_score()
	highscore = scoring.get_highscore()
	# draw 1up and high score hud
	hud.display_scores(screen, dt, score_1up, highscore, SCORE_Y)
	# draw start text
	txt = font_render('Start', pygame.Color('white'))
	w = txt.get_rect().width
	screen.blit(txt, (c.GAME_CENTER_X - w//2, offset_y + START_Y))
	# draw copyright?
	txt = font_render('-Copyright or whatever-', pygame.Color('white'))
	w = txt.get_rect().width
	screen.blit(txt, (c.GAME_CENTER_X - w//2, offset_y + COPY_Y))


class Menu(_State):
	def __init__(self, persist={}):
		_State.__init__(self, persist)
		# init hud
		hud.init()
		# initialize the stars
		stars.create_stars()
		# scrolling menu up
		self.offset_y = c.GAME_HEIGHT
		self.next = c.PLAY_STATE
		self.is_scrolling = True
		self.timer = 0
		self.flash_num = 0
		self.is_flashing = False

	def get_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in setup.START_KEYS:
				if self.ready:
					# start the game
					self.next = c.PLAY_STATE
					self.done = True
				else:
					# go to menu
					self.ready = True

	def update(self, dt, keys):
		# stars
		stars.update(dt)
		# scroll menu
		if self.offset_y > 0:
			self.offset_y -= MENU_SPEED
		# flash timer
		if self.is_flashing:
			self.is_flashing = self.flash_num < TITLE_FLASH_NUM * 2
			if self.is_flashing:
				changed = self.timer.update(dt)
				if changed:
					self.flash_num += 1

	def display(self, screen, dt):
		# draw background
		display_stars_bg(screen)
		# title normal
		if not self.is_flashing:
			surf = LIGHT_TITLE
		elif self.timer.on:
			surf = WHITE_TITLE
		else:
			surf = GREEN_TITLE
		screen.blit(LIGHT_TITLE, (TITLE_X, TITLE_Y + self.offset_y))
		# hud
		display_menu_hud(screen, dt, self.offset_y)
