
import os
import sys
import json
import threading

import pygame

from . import scoring
from . import constants as c

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return wrapper

def lerp(start, stop, percent):
    return (1 - percent) * start + percent * stop

def map(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def load_all_gfx(directory, color_key=(0,0,0), accept=(".png",".bmp",".gif")):
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

def load_all_sfx(directory, accept=(".ogg",".wav")):
    accept_all = len(accept) == 0
    effects = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if accept_all or ext.lower() in accept:
            effects[name] = pygame.mixer.Sound(os.path.join(directory, filename))
    return effects

def load_all_fonts(directory, accept=".ttf"):
    fonts = {}
    for f in os.listdir(directory):
        name,ext = os.path.splitext(f)
        if ext.lower() in accept:
            fonts[name] = os.path.join(directory, f)
    return fonts

class Control(object):
    """
    Main class for running the game states and window
    """

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.paused = False
        self.fps = c.FPS
        self.out_screen = pygame.display.get_surface()
        # mini screen
        self.screen = pygame.Surface(c.SCREEN_SIZE).convert()
        self.time = 0

        self.state_dict = None
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.time, {})

    def flip_state(self):
        persist = self.state.cleanup()
        prev, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def events(self):
        for event in pygame.event.get():
            t = event.type
            if t == pygame.QUIT:
                self.running = False
            elif t == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    self.running = False
            self.state.get_event(event)
        return pygame.key.get_pressed()

    def main(self):
        while self.running:
            # millis --> seconds
            dt = self.clock.tick(self.fps) / 1000
            self.time += dt

            keys = self.events()
            if not self.paused:
                self.state.update(dt, keys)

            if self.state.done:
                self.flip_state(self)
            elif self.state.quit:
                self.running = False

            self.state.display(self.screen, dt)
            # scale up to output
            pygame.transform.scale(self.screen, (c.WIDTH*2, c.HEIGHT*2),
                                   self.out_screen)
            pygame.display.update()
