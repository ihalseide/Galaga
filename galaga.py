#!/usr/bin/env python3

import sys, pygame, math, os, time, random, traceback
from dataclasses import dataclass
from collections import namedtuple
from pygame.math import Vector2
from pygame.rect import Rect
from math import sin
from string import ascii_lowercase

# Directories
SOUNDS_DIR = os.path.join('resources', 'audio')
GRAPHICS_DIR = os.path.join('resources','graphics')

# Game state keys
STATE_TITLE = 'title state'
STATE_DEMO = 'demo state'
STATE_PLAY = 'play state'
STATE_SCORE_ENTRY = 'score entry state'
STATE_GAME_OVER = 'game over state'

# String constants for in-game
TITLE = 'Galaga'  # title for the game window
TITLE_FOOTER_TEXT = 'GALAGA © 1981'  # shown at the bottom of the screen on the menu
START_TEXT = 'START'  # Start message in play state
HI_SCORE_MESSAGE = 'HI-SCORE'  # HUD high score label
ONE_UP = '1UP'  # HUD 1up label
ONE_UP_NUM_FORMAT = '{: =6}'  # number format string for 1up score
HI_SCORE_NUM_FORMAT = '{: =6}'  # number format string for high score
STAGE_FORMAT_STR = 'STAGE {: =3}'  # number format string for the stage number
READY = 'READY'  # ready message in play state
GAME_OVER_TEXT = 'GAME OVER'

# Sting messages for game over
RESULT_TEXT = "- Result -"  # text is red
SHOTS_FIRED_TEXT = 'Shots fired {: >12}'  # text is light blue
NUM_HITS_TEXT = 'Number of hits {: >9}'  # text is white
HIT_MISS_RATIO = 'Hit-miss ratio {: >10.1%}'  # text is yellow

# Resources and other file paths
RESOURCE_DIR = "resources"
SCORE_FILE = "scores.txt"

# Game space
GAME_WIDTH, GAME_HEIGHT = 224, 288
GAME_CENTER_X, GAME_CENTER_Y = GAME_WIDTH // 2, GAME_HEIGHT // 2
STAGE_TOP_Y = 30  # Y-coord. for the top of the stage
STAGE_BOTTOM_Y = GAME_HEIGHT - 20  # Y-coord. for the bottom of the stage
BADGE_Y = GAME_HEIGHT - 19  # Y-coord for the top of the stage badges
STAGE_BOUNDS = pygame.Rect(0, STAGE_TOP_Y, GAME_WIDTH, STAGE_BOTTOM_Y - STAGE_TOP_Y)

# Timing and frequencies in milliseconds unless otherwise noted
EXPLOSION_PLAYER_FRAME = 140
EXPLOSION_ENEMY_FRAME = 120
FPS = 30 # frames per second
TEXT_FLASH_FREQ = 300
PLAYER_FIRE_COOLDOWN = 400
PLAYER_SPEED = 0.085
STAGE_DURATION = 1600
READY_DURATION = 1600
INTRO_MUSIC_DURATION = 6600
START_NOISE_WAIT = 0
START_DURATION = START_NOISE_WAIT + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 200
FIRE_COOLDOWN = 200
GAME_OVER_DURATION = 3000
LINE_TEXT_HEIGHT = 16
GAME_OVER_STATE_DURATION = 14500
BLINK_1UP = 450

# Used colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
LIGHT_GREEN = (144, 238, 144)

# Title settings
SCORE_Y = 10
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60
MENU_SPEED = 3
TITLE_FLASH_TIME = 150  # millis.
TITLE_FLASH_NUM = 12

# font spritesheet coordinates and stuff
FONT_ALPHABET_Y = 224
FONT_CHAR_SIZE = 8

# Number of stars in the star field background
STAR_COUNT = 64

class GalagaSprite (pygame.sprite.Sprite):
    # A Galaga Sprite is different because it aligns the hitbox rect to its sprite rect center.

    def __init__ (self, hitbox, sprite, offset_x=0, offset_y=0, *groups: pygame.sprite.Group):
        super(GalagaSprite, self).__init__(groups)
        # Rect is the hitbox in the world, and it must be named "rect" for pygame
        self.rect = hitbox
        # Sprite is the rectangle selection in the sprite sheet
        self.sprite = None
        # Offset between the sprite image and the hitbox
        self.offset_x = offset_x
        self.offset_y = offset_y

    def display(self, surface, flip_horizontal=False, flip_vertical=False):
        if self.sprite is not None:
            img = grab_sheet(self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height)
            img = pygame.transform.flip(img, flip_horizontal, flip_vertical)
            # Center the image
            x = self.rect.x - sprite.width // 2 + self.offset_x
            y = self.rect.y - sprite.height // 2 + self.offset_y
            surface.blit(img, (x, y))

Star = namedtuple('Star', 'x y color layer_num time_on time_off')

def get_sfx(sound_name: str) -> pygame.mixer.Sound:
    return SOUNDS.get(sound_name)

def has_sfx(sound_name: str) -> bool:
    return get_sfx(sound_name) is not None

def get_image(image_name: str) -> pygame.Surface:
    return game.graphics.get(image_name)

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

def linear_interpolation(start: float, stop: float, percent: float) -> float:
    """
    Linear interpolation function
    :param start: starting value for interpolation
    :param stop: ending value for interpolation
    :param percent: proportion of the way through interpolation (0.0 -> 1.0)
    :return: the interpolated value
    """
    return (1 - percent) * start + percent * stop

def map_value(value, in_start, in_stop, out_start, out_stop):
    """
    Map a value from an input range to an output range
    :param value:
    :param in_start:
    :param in_stop:
    :param out_start:
    :param out_stop:
    :return:
    """
    return out_start + (out_stop - out_start) * ((value - in_start) / (in_stop - in_start))

def _font_render(text: str, color: pygame.Color, bg_color=None):
    """
    Create a pygame image with the text rendered on it using the custom bitmap font
    :param text:
    :param color:
    :param bg_color:
    :return:
    """
    surf = pygame.Surface((len(text) * FONT_CHAR_SIZE, FONT_CHAR_SIZE))
    if bg_color is None:
        surf.set_colorkey(pygame.Color('black'))
    for i, char in enumerate(text):
        # get font location for the char, default to unknown symbol
        font_data = get_from_font(char.lower())
        if not font_data:
            font_data = get_from_font(None)
        # grab the image at location
        glyph = grab_sheet(font_data[0], font_data[1], FONT_CHAR_SIZE, FONT_CHAR_SIZE)
        surf.blit(glyph, (i * FONT_CHAR_SIZE, 0), )
    # replace colors
    pixels = pygame.PixelArray(surf)
    if bg_color:
        pixels.replace(pygame.Color('black'), bg_color)
    pixels.replace(pygame.Color('white'), color)
    pixels.close()
    return surf

def draw_text(surface, text, position, color, background_color=None, center_x=False, center_y=False):
    text_surface = _font_render(str(text), color, background_color)
    x, y = position
    width, height = text_surface.get_size()
    if center_x:
        x -= width // 2
    if center_y:
        y -= height // 2
    if surface is None:
        return text_surface
    else:
        return surface.blit(text_surface, (x, y))

def grab_sheet(x: int, y: int, width: int, height: int) -> pygame.Surface:
    """
    Get a pixel rectangle from an the spritesheet resource
    """
    return get_image('sheet').subsurface((x, y, width, height))

def calc_stage_badges(stage_num):
    # Calculate how many of each stage badges there are for a given stage
    assert stage_num in range(256)
    w_stage = stage_num  # temp. var
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
    return StageBadges(num_1, num_5, num_10, num_20, num_30, num_50)

def random_star () -> Star:
    x = random.randint(0, GAME_WIDTH)
    y = random.randint(0, GAME_HEIGHT)
    time_on, time_off = random.choice([(150, 140), (210, 200), (310, 300), (410, 300), (510, 300)])
    layer = random.randint(0, 1)
    if layer == 0:
        # speed = 0.050
        color = random.choice(RED, LIGHT_GREEN)
    elif layer == 1:
        # speed = 0.075
        color = random.choice(YELLOW, BLUE, WHITE)
    return Star(x, y, color, layer, time_on, time_off, speed)

def stars_init ():
    game.stars_direction = 1
    game.stars = [random_star() for _ in range(STAR_COUNT)]

def stars_update(delta_time: int):
    self.current_time += delta_time
    # update each timer
    for timer in self.twinkling_timers:
        timer.current_time += delta_time
        if timer.is_shown and timer.current_time >= timer.on_time:
            timer.current_time = 0
            timer.is_shown = False
        elif not timer.is_shown and timer.current_time >= timer.off_time:
            timer.current_time = 0
            timer.is_shown = True

def show_star_p (star_layer, star_on, star_off):
    return True

def star_calc_y (star_y, star_layer):
    pass

def star_display (star):
    if show_star_p(star.layer, star.time_on, star.time_off):
        y = star_calc_y(star.y, star.layer)
        game.screen.set_at((star.x, y), star.color)

def stars_display ():
    for star in game.stars:
        star_display(star)

def poll_events ():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #game.running = False
            cleanup()
            return
        give_event(event)
    return pygame.key.get_pressed()

def load_graphics () -> dict:
    graphics = {}
    color_key = BLACK
    for filename in os.listdir(GRAPHICS_DIR):
        name, ext = os.path.splitext(filename)
        if ext.lower() == '.png':
            img = pygame.image.load(os.path.join(GRAPHICS_DIR, filename))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color_key)
            graphics[name] = img
    game.graphics = graphics
    return graphics

def load_sounds () -> dict:
    effects = {}
    accept=(".ogg", ".wav")
    for filename in os.listdir(SOUNDS_DIR):
        name, ext = os.path.splitext(filename)
        if ext.lower() in accept:
            effects[name] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, filename))
    game.sounds = effects
    return effects

def create_font () -> dict:
    y = FONT_ALPHABET_Y + FONT_CHAR_SIZE
    font = dict()
    # Add alphabet
    for i, char in enumerate(ascii_lowercase):
        font[char] = (i * FONT_CHAR_SIZE, FONT_ALPHABET_Y)
    # Add digits
    for i in range(10):
        font[str(i)] = (i * FONT_CHAR_SIZE, y)
    # Add other symbols
    font['-']  = (10 * FONT_CHAR_SIZE, y)
    font[' ']  = (11 * FONT_CHAR_SIZE, y)
    font[None] = (12 * FONT_CHAR_SIZE, y)
    font[':']  = (13 * FONT_CHAR_SIZE, y)
    font['!']  = (14 * FONT_CHAR_SIZE, y)
    font[',']  = (15 * FONT_CHAR_SIZE, y)
    font['©']  = (16 * FONT_CHAR_SIZE, y)
    font['.']  = (17 * FONT_CHAR_SIZE, y)
    font['%']  = (18 * FONT_CHAR_SIZE, y)
    return font

def set_video_centered ():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def main ():
    pass

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

