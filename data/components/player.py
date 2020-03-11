import pygame

from data import constants as c
from data import tools
from data.components import galaga_sprite

FIRE_COOLDOWN = 400
SPEED = 0.085


class Player(galaga_sprite.GalagaSprite):
    def __init__(self):
        galaga_sprite.GalagaSprite.__init__(self, c.GAME_WIDTH // 2, c.GAME_HEIGHT - 25, 13, 12,
                                            tools.grab_sheet(6 * 16, 0 * 16, 16))
        self.last_fire_time = 0
        self.image_offset_x = 1

    def update(self, dt, keys):
        s = round(SPEED * dt)
        if keys[pygame.K_RIGHT]:
            self.x += s
        elif keys[pygame.K_LEFT]:
            self.x -= s

    def can_fire(self, time):
        return time - self.last_fire_time >= FIRE_COOLDOWN
