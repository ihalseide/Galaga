
import pygame

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
