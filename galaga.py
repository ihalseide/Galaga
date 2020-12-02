#!/usr/bin/env python3

import sys, pygame, math, os, time, random, traceback
from dataclasses import dataclass
from collections import namedtuple
from pygame.math import Vector2
from pygame.rect import Rect
from math import sin
from string import ascii_lowercase, digits, ascii_letters

from constants import *

# Globals
the_stars = None 
the_stars_direction = None
the_screen = None
the_sprites = None
the_spritesheet = None

Star = namedtuple('Star', 'x y color layer time_on time_off')

class GalagaSprite (pygame.sprite.Sprite):
    # A Galaga Sprite is different because it aligns the hitbox rect to its sprite rect center.

    def __init__ (self, x, y, width, height, sprite=None, offset_x=0, offset_y=0):
        super(GalagaSprite, self).__init__()
        # Rect is the hitbox in the world, and it must be named "rect" for pygame
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Sprite is the rectangle selection in the sprite sheet
        self.sprite = sprite
        # Offset between the sprite image and the hitbox
        self.offset_x = offset_x
        self.offset_y = offset_y
        # Replace color
        self.replace_white = None

    def display(self, flip_horizontal=False, flip_vertical=False):
        if self.sprite is not None:
            x, y, width, height = self.sprite
            img = sprite(x, y, width, height)
            img = pygame.transform.flip(img, flip_horizontal, flip_vertical)
            # For text sprite coloring
            if self.replace_white:
                img2 = img
                img = img2.copy()
                pygame.transform.threshold(img, img2, WHITE, set_color=self.replace_white, inverse_set=True)
            # Center the image
            x = self.x - width // 2 + self.offset_x
            y = self.y - height // 2 + self.offset_y
            the_screen.blit(img, (x, y))

def sprite(x: int, y: int, width: int, height: int) -> pygame.Surface:
    return the_spritesheet.subsurface((x, y, width, height))

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
    return ...

def random_star ():
    x = random.randint(0, GAME_WIDTH)
    y = random.randint(0, GAME_HEIGHT)
    time_on, time_off = random.choice([(150, 140), (210, 200), (310, 300), (410, 300), (510, 300)])
    layer = random.randint(0, 1)
    if layer == 0:
        color = random.choice((RED, LIGHT_GREEN))
    elif layer == 1:
        color = random.choice((YELLOW, BLUE, WHITE))
    return Star(x, y, color, layer, time_on, time_off)

def stars_init ():
    global the_stars, the_stars_direction
    random.seed(-404)
    the_stars_direction = 1
    the_stars = [random_star() for _ in range(STAR_COUNT)]

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

def show_star_p (star_on, star_off, time):
    # TODO: implement blinking stars
    return True

def layer_speed (star_layer):
    return [71, 83][star_layer]

def star_y (star_y, star_layer, time):
    change = (the_stars_direction * layer_speed(star_layer) * time // 1000) 
    return (star_y + change) % GAME_HEIGHT

def star_display (star, time):
    if show_star_p(star.time_on, star.time_off, time):
        y = star_y(star.y, star.layer, time)
        the_screen.set_at((star.x, y), star.color)

def stars_display ():
    time = pygame.time.get_ticks()
    for star in the_stars:
        star_display(star, time)

def poll_events ():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #game.running = False
            quit()
            return
        #give_event(event)
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

def char_to_sprite (char) -> Rect:
    # Note: this function relies on the specific details of the layout in the spritesheet!
    char = char.lower()
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789 -:!,.%©?'
    if char not in charset:
        char = '?'
    i = charset.index(char)
    x = 17 + i % 15
    y = 0 + i // 15
    return (x*8, y*8, 8, 8)

def text_sprite_create_char (char, x, y, color):
    global the_sprites
    sprite = GalagaSprite(x, y, FONT_CHAR_SIZE, FONT_CHAR_SIZE, 0, 0)
    sprite.sprite = char_to_sprite(char)
    sprite.replace_white = color
    the_sprites.append(sprite)

def text_sprite_create (text, x, y, color):
    x_offset = len(text) * FONT_CHAR_SIZE // 2
    for i, char in enumerate(text):
        text_sprite_create_char(char, x + i * FONT_CHAR_SIZE - x_offset, y, color)

def set_video_centered ():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def sprites_display ():
    for s in the_sprites:
        s.display()

def display ():
    the_screen.fill(BLACK)
    stars_display()
    sprites_display()
    pygame.display.update()

def display_init ():
    global the_screen
    set_video_centered()
    pygame.init()
    the_screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption('GALAGA (Python)')

def sprites_init ():
    global the_sprites
    the_sprites = [] 
    text_sprite_create('1UP', 30, 5, RED)
    title_init()

def spritesheet_init ():
    global the_spritesheet
    the_spritesheet = pygame.image.load('resources/spritesheet.png')

def title_init ():
    text_sprite_create('GALAGA © 1981', GAME_CENTER_X, 275, WHITE)
    text_sprite_create('START', GAME_CENTER_X, 180, WHITE)

def main ():
    display_init()
    spritesheet_init()
    stars_init()
    sprites_init()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        poll_events()
        display()

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

