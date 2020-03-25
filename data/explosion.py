import pygame

from data import tools
from data.galaga_sprite import GalagaSprite


class Explosion(GalagaSprite):
    FRAME_DURATION = 120

    def __init__(self, x: int, y: int):
        super(Explosion, self).__init__(x, y, 16, 16)
        self.frame = 0
        self.frame_timer = 0
        self.image = tools.grab_sheet(224, 80, 16, 16)

    def update(self, delta_time: int, flash_flag: bool):
        self.frame_timer += delta_time
        if self.frame_timer >= self.FRAME_DURATION:
            self.frame += 1
            self.frame_timer = 0
        if self.frame == 1:
            self.image = tools.grab_sheet(240, 80, 16, 16)
        elif self.frame == 2:
            self.image = tools.grab_sheet(224, 96, 16, 16)
        elif self.frame == 3:
            self.image = tools.grab_sheet(0, 112, 32, 32)
        elif self.frame == 4:
            self.image = tools.grab_sheet(32, 112, 32, 32)
        elif self.frame != 0:
            self.kill()

    def display(self, surface: pygame.Surface):
        super(Explosion, self).display(surface)
