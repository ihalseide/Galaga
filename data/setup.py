#!/usr/bin/env python3
#
# setup.py


import os
from string import ascii_lowercase

import pygame

from . import constants as c
from .constants import RESOURCES

# font coords and stuff
ALPHA_Y = 224
CHAR_SIZE = 8

# Setup pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
SCREEN = pygame.display.set_mode([c.SCREEN_WIDTH, c.SCREEN_HEIGHT])
pygame.display.set_caption('Galaga')

# Pygame key constants
START_KEYS = [pygame.K_SPACE, pygame.K_RETURN]

# Resource loading functions:


def load_all_gfx(directory, accept=('.png', '.bmp', '.gif'), colorkey=pygame.Color('black')):
	graphics = {}
	for filename in os.listdir(directory):
		name, ext = os.path.splitext(filename)
		if ext.lower() in accept:
			img = pygame.image.load(os.path.join(directory, filename))
			if img.get_alpha():
				img = img.convert_alpha()
			else:
				img = img.convert()
				img.set_colorkey(colorkey)
			graphics[name] = img
	return graphics


def load_all_sfx(directory, accept=(".ogg", ".wav")):
	accept_all = len(accept) == 0
	effects = {}
	for filename in os.listdir(directory):
		name, ext = os.path.splitext(filename)
		if accept_all or ext.lower() in accept:
			effects[name] = pygame.mixer.Sound(os.path.join(directory, filename))
	return effects


def load_font():
	"""
	Create the coordinate map for the font image
	"""
	font = dict()
	# add alphabet
	for i, char in enumerate(ascii_lowercase):
		font[char] = (i * CHAR_SIZE, ALPHA_Y)
	# add digits
	for i in range(10):
		font[str(i)] = (i * CHAR_SIZE, ALPHA_Y + CHAR_SIZE)
	font['-'] = (10 * CHAR_SIZE, ALPHA_Y + CHAR_SIZE)
	font[' '] = (11 * CHAR_SIZE, ALPHA_Y + CHAR_SIZE)
	font[None] = (12 * CHAR_SIZE, ALPHA_Y + CHAR_SIZE)
	return font


FONT, SFX, GFX = None, None, None


def load():
	global FONT, SFX, GFX
	# load resources
	FONT = load_font()
	SFX = load_all_sfx(os.path.join(RESOURCES, "audio"), (".ogg",))
	GFX = load_all_gfx(os.path.join(RESOURCES, "graphics"), ('.png', ".bmp"))


load()
