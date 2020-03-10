import os
from string import ascii_lowercase
from typing import Tuple, Union

import pygame

from . import constants as c

# font spritesheet coordinates and stuff
FONT_ALPHABET_Y = 224
FONT_CHAR_SIZE = 8

# Setup pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
SCREEN = pygame.display.set_mode([c.SCREEN_WIDTH, c.SCREEN_HEIGHT])
pygame.display.set_caption(c.TITLE)

# Pygame key constants
START_KEYS = [pygame.K_SPACE, pygame.K_RETURN]


def load_all_gfx(directory, accept=('.png', '.bmp', '.gif'), color_key=pygame.Color('black')) -> dict:
	graphics = {}
	for filename in os.listdir(directory):
		name, ext = os.path.splitext(filename)
		if ext.lower() in accept:
			img = pygame.image.load(os.path.join(directory, filename))
			if img.get_alpha():
				img = img.convert_alpha()
			else:
				img = img.convert()
				img.set_colorkey(color_key)
			graphics[name] = img
	return graphics


def load_all_sfx(directory, accept=(".ogg", ".wav")) -> dict:
	accept_all = len(accept) == 0
	effects = {}
	for filename in os.listdir(directory):
		name, ext = os.path.splitext(filename)
		if accept_all or ext.lower() in accept:
			effects[name] = pygame.mixer.Sound(os.path.join(directory, filename))
	return effects


def load_font() -> dict:
	"""
	Create the coordinate map for the font image
	"""
	font = dict()
	# add alphabet
	for i, char in enumerate(ascii_lowercase):
		font[char] = (i * FONT_CHAR_SIZE, FONT_ALPHABET_Y)
	# add digits
	for i in range(10):
		font[str(i)] = (i * FONT_CHAR_SIZE, FONT_ALPHABET_Y + FONT_CHAR_SIZE)
	font['-'] = (10 * FONT_CHAR_SIZE, FONT_ALPHABET_Y + FONT_CHAR_SIZE)
	font[' '] = (11 * FONT_CHAR_SIZE, FONT_ALPHABET_Y + FONT_CHAR_SIZE)
	font[None] = (12 * FONT_CHAR_SIZE, FONT_ALPHABET_Y + FONT_CHAR_SIZE)
	return font


# load all the resources
_FONT: dict = load_font()
_SFX: dict = load_all_sfx(os.path.join(c.RESOURCES, "audio"), (".ogg",))
_GFX: dict = load_all_gfx(os.path.join(c.RESOURCES, "graphics"), ('.png', ".bmp"))


def get_sfx(sound_name: str) -> Union[pygame.mixer.Sound, None]:
	return _SFX.get(sound_name)


def has_sfx(sound_name: str) -> bool:
	return get_sfx(sound_name) is not None


def get_image(image_name: str) -> Union[pygame.Surface, None]:
	return _GFX.get(image_name)


def has_image(image_name: str) -> bool:
	return get_image(image_name) is not None


def get_from_font(character: Union[str, None]) -> Union[Tuple[int, int], None]:
	return _FONT.get(character)


def has_char_in_font(character: str) -> bool:
	return get_from_font(character) is not None
