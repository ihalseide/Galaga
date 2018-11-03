
import pygame

from .. import setup

class Missile(pygame.sprite.Sprite):
    PLAYER_SPEED = 350
    ENEMY_SPEED = 300

    def __init__(self, loc, vel, enemy):
        pygame.sprite.Sprite.__init__(self)

        self.vel = vel
        self.enemy = enemy

        self.rect = pygame.Rect(0, 0, 2, 10)
        self.rect.center = loc

        if self.enemy:
            self.image = setup.grab(118, 100, 3, 8)
        else:
            self.image = setup.grab(118, 178, 3, 8)

    def update(self, dt, bounds):
        if self.enemy:
            vel = self.vel * self.ENEMY_SPEED * dt
        else:
            vel = self.vel * self.PLAYER_SPEED * dt
        self.rect.x += round(vel.x)
        self.rect.y += round(vel.y)
        if not bounds.contains(self.rect):
            self.kill()
