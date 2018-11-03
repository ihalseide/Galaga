
import os

import pygame

from . import tools
from . import constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
SCREEN = pygame.display.set_mode([2 * x for x in c.SCREEN_SIZE])

FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"), [".ttf"])
SFX = tools.load_all_sfx(os.path.join("resources", "audio"), [".ogg"])
GFX = tools.load_all_gfx(os.path.join("resources", "graphics"), [".png"])

def grab(x, y, w, h, image="sheet"):
    sheet = GFX.get(image)
    if sheet:
        return sheet.subsurface(x, y, w, h)
    else:
        return None

def grab_cells(x, y, w=1, h=1, cell_w=16, cell_h=16, x_off=0, y_off=0, x_gap=0, y_gap=0,
              image="sheet"):
    xx = x_off + x * (w + x_gap)
    yy = y_off + y * (h + y_gap)
    return grab(xx, yy, w * cell_w, h * cell_h, image)

def grab_cell_1(x, y, w=1, h=1, image="sheet"):
    return grab_cells(x, y, w, h, x_off=1, y_off=1, x_gap=1, y_gap=1, image=image)
