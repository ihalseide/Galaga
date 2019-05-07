
import pygame

from .. import tools
from .. import setup
from .. import constants as c

BOUNDS = pygame.Rect(0, 0, c.WIDTH, c.HEIGHT)
PLAYER_SPEED = 350
ENEMY_SPEED = 300
ENEMY_TYPE = tools.grab(setup.GFX.get('sheet'), 246, 51, 3, 8)
PLAYER_TYPE = tools.grab(setup.GFX.get('sheet'), 246, 67, 3, 8)

class Missile(pygame.sprite.Sprite):
    def __init__(self, loc, vel, enemy):
        pygame.sprite.Sprite.__init__(self)

        self.vel = vel
        self.enemy = enemy

        self.rect = pygame.Rect(0, 0, 2, 10)
        self.rect.center = loc

        if self.enemy:
            self.image = ENEMY_TYPE
        else:
            self.image = PLAYER_TYPE

    def update(self, dt):
        if self.enemy:
            vel = self.vel * ENEMY_SPEED * dt
        else:
            vel = self.vel * PLAYER_SPEED * dt
        self.rect.x += round(vel.x)
        self.rect.y += round(vel.y)
        if not BOUNDS.contains(self.rect):
            self.kill()
