
import pygame

import ..setup as r

class Missile(pygame.sprite.Sprite):
    player_speed = 350
    enemy_speed = 300

    def __init__(self, loc, vel, enemy):
        pygame.sprite.Sprite.__init__(self)

        self.vel = vel
        self.enemy = enemy

        self.rect = pygame.Rect(0, 0, 2, 10)
        self.rect.center = loc

        if self.enemy:
            self.image = r.GFX.subsurface((125,105,3,8))
        else:
            self.image = r.GFX.subsurface((125,190,3,8))

    def update(self, dt, bounds):
        if self.enemy:
            vel = self.vel * self.enemy_speed * dt
        else:
            vel = self.vel * self.player_speed * dt
        self.rect.x += round(vel.x)
        self.rect.y += round(vel.y)
        if not bounds.contains(self.rect):
            self.kill()
