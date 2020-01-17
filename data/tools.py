#!/usr/bin/env python3
#
# tools.py


import threading
from typing import Tuple

import pygame

from . import setup
from .setup import CHAR_SIZE, GFX


def threaded(fn):
	"""
	Wrapper to make a function run on a thread
	"""

	def wrapper(*args, **kwargs):
		thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
		thread.start()
		return thread

	return wrapper


def lerp(start, stop, percent):
	return (1 - percent) * start + percent * stop


def map_value(value, in_start, in_stop, out_start, out_stop):
	"""
	Map a value from an input range to an output range
	"""
	return out_start + (out_stop - out_start) * ((value - in_start) / (in_stop - in_start))


def _font_render(text, color, bg_color=None):
	"""
	Create a pygame image with the text rendered on it
	"""
	surf = pygame.Surface((len(text) * CHAR_SIZE, CHAR_SIZE))
	for i, char in enumerate(text):
		# get font location for the char, default to unknown symbol
		font_data = setup.FONT.get(char.lower())
		if not font_data:
			font_data = setup.FONT.get(None)
		# grab the image at location
		glyph = grab_sheet(font_data[0], font_data[1], CHAR_SIZE)
		surf.blit(glyph, (i * CHAR_SIZE, 0))
	# replace colors
	pixels = pygame.PixelArray(surf)
	if bg_color:
		pixels.replace(pygame.Color('black'), bg_color)
	pixels.replace(pygame.Color('white'), color)
	pixels.close()
	return surf


def draw_text(screen: pygame.Surface, text: str, position: Tuple[int, int], color, bg_color=None, centered_y=False,
			  centered_x=False):
	surf = _font_render(text, color, bg_color)
	x, y = position
	width, height = surf.get_size()
	if centered_y:
		y -= height // 2
	if centered_x:
		x -= width // 2
	screen.blit(surf, (x, y))


def grab_sheet(x, y, width, height=None):
	"""
	Get a pixel rectangle from an image resource
	"""
	# allow square assumption (w = h)
	if height is None:
		height = width
	return GFX['sheet'].subsurface(x, y, width, height)