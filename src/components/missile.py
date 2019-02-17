
import pygame

from .. import tools
from .. import setup

class Missile(pygame.sprite.Sprite):
    PLAYER_SPEED = 350
    ENEMY_SPEED = 300
    ENEMY_TYPE = tools.grab(setup.Q_GFX.get('sheet'), 246, 51, 3, 8)
    PLAYER_TYPE = tools.grab(setup.Q_GFX.get('sheet'), 246, 67, 3, 8)

    def __init__(self, loc, vel, enemy):
        pygame.sprite.Sprite.__init__(self)

        self.vel = vel
        self.enemy = enemy

        self.rect = pygame.Rect(0, 0, 2, 10)
        self.rect.center = loc

        if self.enemy:
            self.image = self.ENEMY_TYPE
        else:
            self.image = self.PLAYER_TYPE

    def update(self, dt, bounds):
        if self.enemy:
            vel = self.vel * self.ENEMY_SPEED * dt
        else:
            vel = self.vel * self.PLAYER_SPEED * dt
        self.rect.x += round(vel.x)
        self.rect.y += round(vel.y)
        if not bounds.contains(self.rect):
            self.kill()
