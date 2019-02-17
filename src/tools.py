
import os
import threading

import pygame

from . import constants as c
from . import setup
from .setup import CHAR_SIZE

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

def calc_stage_badges(stage_num):
    """
    Calculate how many of each stage badges there are for a given stage
    """
    if stage_num == 0:
        return {}
    else:
        w_stage = stage_num # temporary modification
        num_50 = w_stage // 50
        w_stage -= num_50 * 50
        num_30 = w_stage // 30
        w_stage -= num_30 * 30
        num_20 = w_stage // 20
        w_stage -= num_20 * 20
        num_10 = w_stage // 10
        w_stage -= num_10 * 10
        num_5 = w_stage // 5
        num_1 = w_stage - num_5 * 5
        return {1: num_1, 5: num_5, 10: num_10, 20: num_20,
                30: num_30, 50: num_50}

def map(value, istart, istop, ostart, ostop):
    """
    Map a value from an input range to an output range
    """
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def font_render(text, color, bg_color=None):
    """
    Create a pygame image with the text rendered on it
    """
    surf = pygame.Surface((len(text) * CHAR_SIZE, CHAR_SIZE))
    surf = surf.convert(setup.GFX['sheet'])
    for i, char in enumerate(text):
        # get font location for the char, default to unknown symbol
        font_data = setup.FONT.get(char.lower())
        if not font_data:
            font_data = setup.FONT.get(None)
        # grab the image at location
        glyph = sheet_grab(font_data[0], font_data[1], CHAR_SIZE)
        surf.blit(glyph, (i * CHAR_SIZE, 0))
    # replace palette color
    if bg_color:
        surf.set_palette_at(setup.BLACK_INDEX, bg_color)
    surf.set_palette_at(setup.WHITE_INDEX, (color.r, color.g, color.b))
    return surf

def grab(surf, x, y, w, h=None):
    '''
    Get a pixel rectangle from an image resource
    '''
    # allow square assumption (w = h)
    if h is None:
        h = w
    return surf.subsurface(x, y, w, h)

# shortcut
def sheet_grab(x, y, w, h=None):
    return grab(setup.Q_GFX['sheet'], x, y, w, h)

def grab_cells(surf, x, y, w=1, h=1, cell_w=16, cell_h=16, x_off=0,
               y_off=0, x_gap=0, y_gap=0):
    xx = x * (cell_w + x_gap) + x_off
    yy = y * (cell_h + y_gap) + y_off
    ww = w * cell_w
    hh = h * cell_h
    return grab(surf, xx, yy, ww, hh)

# shortcut
def sheet_grab_cells(x, y, w=1, h=1, cell_w=16, cell_h=16, x_off=0,
                     y_off = 0, x_gap = 0, y_gap=0):
    return grab_cells(setup.Q_GFX['sheet'], x, y, w, h, cell_w, cell_h,
                      x_off, y_off, x_gap, y_gap)
