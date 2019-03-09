
import time

import pygame

from .. import tools
from .. import constants as c

SPEED = 85

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 15, 15)
        self.rect.center = (c.WIDTH/2, c.HEIGHT-self.rect.height//2-25)
        self.image = tools.sheet_grab_cells(6, 0)
        self.speed = SPEED

    def update(self, dt, keys):
        s = round(self.speed * dt)
        if keys[pygame.K_RIGHT]:
            if self.rect.right + s < c.WIDTH:
                self.rect.x += s
        elif keys[pygame.K_LEFT]:
            if self.rect.x - s > 0:
                self.rect.x -= s
