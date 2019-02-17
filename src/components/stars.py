
import random

import pygame

from .. import constants as c

NUM = 90
COLORS = (pygame.Color("red"), pygame.Color("blue"),
                   pygame.Color("blue"), pygame.Color("lightgreen"),
                   pygame.Color("white"))
LAYERS = 2
PHASES = [0, 0.25, 0.1]

# Whether the stars are moving:
# 1 = down, 0 = not moving, -1 = up
_moving = 1
_stars = []

def create_stars():
    global _stars
    _stars = []
    for i in range(NUM):
        x = random.randint(0, c.WIDTH)
        y = random.randint(0, c.HEIGHT)
        col = random.choice(COLORS)
        z = random.randint(0, LAYERS-1)
        t = random.choice(PHASES)
        b = True #bool(random.randint(0,1))
        s = Star((x,y), color=col, z=z, twinkles=b, time_offset=t)
        _stars.append(s)
    
def update(dt):
    for s in _stars:
        s.update(dt, _moving)

def set_moving(value):
    global _moving
    if value == False or value == 0:
        _moving = 0
    elif value < 0:
        _moving = -1
    elif value > 0:
        _moving = 1
    else:
        # error, but default to 0
        _moving = 0

def display(screen):
    for s in _stars:
        s.draw(screen)

class Star(object):
    """
    Graphical object for the background
    """
    speeds = 30, 65
    show_time = 0.4 # seconds
    hide_time = 0.2

    def __init__(self, loc, color, z, twinkles=False, time_offset=0):
        self.loc = tuple(loc)
        self.color = color
        self.z = z
        self.show = True
        self.twinkles = twinkles
        self.timer = time_offset

    def update(self, dt, move=1):
        if move:
            new_y = self.loc[1] + round(self.speeds[self.z] * dt * move)
            if new_y > c.HEIGHT:
                new_y = 0 
            elif new_y < 0:
                new_y = c.HEIGHT
            self.loc = self.loc[0], new_y
        if self.twinkles:
            if self.show and self.timer >= self.show_time:
                self.show = False
                self.timer = 0
            elif not self.show and self.timer >= self.hide_time:
                self.show = True
                self.timer = 0
            self.timer += dt

    def draw(self, screen):
        if self.show:
            r_loc = [round(a) for a in self.loc]
            screen.set_at(r_loc, self.color)
