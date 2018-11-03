
import os

import pygame

from . import tools
from . import constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
SCREEN = pygame.display.set_mode([2 * x for x in c.SCREEN_SIZE])

FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"), [".ttf"])
SFX = tools.load_all_sfx(os.path.join("resources", "audio"), [".ogg"])
GFX = tools.load_all_gfx(os.path.join("resources", "graphics"), (0,0,0), [".png"])

def grab(x, y, w, h, image="sheet"):
    sheet = GFX.get(image)
    if sheet:
        return sheet.subsurface(x, y, w, h)
    else:
        return None

def grab_cells(x, y, w=1, h=1, cell_w=16, cell_h=16, x_off=0, y_off=0, x_gap=0, y_gap=0,
              image="sheet"):
    xx = x * (cell_w + x_gap) + x_off
    yy = y * (cell_h + y_gap) + y_off
    ww = w * cell_w
    hh = h * cell_h
    return grab(xx, yy, ww, hh, image)
