import pygame

from data import tools
from data.galaga_sprite import GalagaSprite


class Player(GalagaSprite):
    FIRE_COOLDOWN = 400
    SPEED = 0.085

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 13, 12)
        self.image = tools.grab_sheet(6 * 16, 0 * 16, 16, 16)
        self.last_fire_time = 0
        self.image_offset_x = 1

    def update(self, delta_time, keys):
        s = round(self.SPEED * delta_time)
        if keys[pygame.K_RIGHT]:
            self.x += s
        elif keys[pygame.K_LEFT]:
            self.x -= s

    def can_fire(self, time):
        return time - self.last_fire_time >= self.FIRE_COOLDOWN
