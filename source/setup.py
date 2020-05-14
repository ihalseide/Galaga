import os
from string import ascii_lowercase

import pygame

from . import constants as c

# font spritesheet coordinates and stuff
FONT_ALPHABET_Y = 224
FONT_CHAR_SIZE = 8

# Pygame key constants
START_KEYS = [pygame.K_SPACE, pygame.K_RETURN]

# Setup pygame
SCREEN = FONT = SOUNDS = GRAPHICS = None


def setup_game():
    global SCREEN, FONT, SOUNDS, GRAPHICS

    # Center the window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    SCREEN = pygame.display.set_mode(c.DEFAULT_SCREEN_SIZE)
    pygame.display.set_caption(c.TITLE)

    # Load these
    FONT = load_font()
    SOUNDS = load_all_sfx(os.path.join(c.RESOURCE_DIR, "audio"), (".ogg",))
    GRAPHICS = load_all_gfx(os.path.join(c.RESOURCE_DIR, "graphics"), ('.png', ".bmp"))


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
    row_2_y = FONT_ALPHABET_Y + FONT_CHAR_SIZE
    font = dict()
    # add alphabet
    for i, char in enumerate(ascii_lowercase):
        font[char] = (i * FONT_CHAR_SIZE, FONT_ALPHABET_Y)
    # add digits
    for i in range(10):
        font[str(i)] = (i * FONT_CHAR_SIZE, row_2_y)
    font['-'] = (10 * FONT_CHAR_SIZE, row_2_y)
    font[' '] = (11 * FONT_CHAR_SIZE, row_2_y)
    font[None] = (12 * FONT_CHAR_SIZE, row_2_y)
    font[':'] = (13 * FONT_CHAR_SIZE, row_2_y)
    font['!'] = (14 * FONT_CHAR_SIZE, row_2_y)
    font[','] = (15 * FONT_CHAR_SIZE, row_2_y)
    font['©'] = (16 * FONT_CHAR_SIZE, row_2_y)
    font['.'] = (17 * FONT_CHAR_SIZE, row_2_y)
    font['%'] = (18 * FONT_CHAR_SIZE, row_2_y)
    return font


def get_sfx(sound_name: str) -> pygame.mixer.Sound:
    return SOUNDS.get(sound_name)


def has_sfx(sound_name: str) -> bool:
    return get_sfx(sound_name) is not None


def get_image(image_name: str) -> pygame.Surface:
    return GRAPHICS.get(image_name)


def has_image(image_name: str) -> bool:
    return get_image(image_name) is not None


def get_from_font(character) -> tuple:
    return FONT.get(character)


def has_char_in_font(character: str) -> bool:
    return get_from_font(character) is not None


def play_sound(sound_name):
    SOUNDS.get(sound_name).play()


def stop_sounds():
    pygame.mixer.stop()


# load all the resources
setup_game()
