
import random

import pygame
from pygame.math import Vector2

import resources as r
from constants import *

class Star(object):
    speeds = 30, 65
    show_time = 0.4 # seconds
    hide_time = 0.2

    def __init__(self, loc, color, z, twinkles=False, time_offset=0):
        self.loc = Vector2(loc)
        self.color = color
        self.z = z
        self.show = True
        self.twinkles = twinkles
        self.timer = time_offset

    def update(self, dt, bounds=None, move=True):
        if move:
            self.loc.y += round(self.speeds[self.z] * dt)
            if bounds and self.loc.y >= bounds.bottom:
                self.loc.y = bounds.top
        if self.twinkles:
            if self.show and self.timer >= self.show_time:
                self.show = False
                self.timer = 0
            elif not self.show and self.timer >= self.hide_time:
                self.show = True
                self.timer = 0
            self.timer += dt

    def display(self, screen):
        # clear then draw
        x, y = (round(a) for a in self.loc)
        if self.show:
            screen.set_at((x,y), self.color)

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

class Player(pygame.sprite.Sprite):
    fire_cooldown = 0.4
    speed = 85

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.controllable = True

        self.rect = pygame.Rect(0, 0, 15, 15)
        self.rect.center = (WIDTH/2, HEIGHT-self.rect.height//2-25)

        self.image = r.GFX.subsurface((102, 1, 16, 16))

        self.last_fire_time = 0

    def update(self, dt, keys):
        s = round(self.speed * dt)
        if keys[pygame.K_RIGHT]:
            self.rect.x += s
        elif keys[pygame.K_LEFT]:
            self.rect.x -= s

    def can_fire(self, time):
        return time - self.last_fire_time >= self.fire_cooldown

class Enemy(pygame.sprite.Sprite):
    def __init__(self, time, path, formation_spot):
        pygame.sprite.Sprite.__init__(self)
        self.start_time = time
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = path[0].x, path[0].y
        self.in_formation = False
        self.path = path
        self.formation_spot = formation_spot

    def update(self, dt, animate=False):
        self.rect.center = (16*f for f in self.formation_spot)

class Bee(Enemy):
    def __init__(self, time, path, formation_spot):
        Enemy.__init__(self, time, path, formation_spot)

        self.images = [r.grab(1+x*17,69,16,16) for x in range(8)]
        self.animation_index = 0
        self.image = self.images[self.animation_index]

class Butterfly(Enemy):
        def __init__(self, time, path, formation_spot):
            Enemy.__init__(self, time, path, formation_spot)

            self.path = path
            self.rect = pygame.Rect(0, 0, 10, 10)
            self.rect.center = loc

class Boss(Enemy):
        def __init__(self, time, path, formation_spot):
            Enemy.__init__(self, time, path, formation_spot)

            self.path = path
            self.rect = pygame.Rect(0, 0, 10, 10)
            self.rect.center = loc
