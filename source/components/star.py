
import pygame

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

    def update(self, dt, bounds=None, move=True):
        if move:
            new_y = self.loc[1] + round(self.speeds[self.z] * dt)
            if bounds and new_y >= bounds.bottom:
                new_y = bounds.top
            self.loc = self.loc[0], new_y
        if self.twinkles:
            if self.show and self.timer >= self.show_time:
                self.show = False
                self.timer = 0
            elif not self.show and self.timer >= self.hide_time:
                self.show = True
                self.timer = 0
            self.timer += dt

    def display(self, screen):
        if self.show:
            r_loc = [round(a) for a in self.loc]
            screen.set_at(r_loc, self.color)
