
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
