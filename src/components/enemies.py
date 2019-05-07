
import pygame
from pygame import Vector2

from .. import tools

class Enemy(pygame.sprite.Sprite):
    ANIMATION_TIME = 0.75 # seconds per frame
    DEATH_TIME = 0.2
    # states
    ASSEMBLING = "Assembling"
    TO_FORMATION = "Going to formation"
    FORMATION = "Formation"
    DIVE_BOMB = "Dive bomb run"
    TRACTOR_BEAM = "Tractor beam"
    DYING = "Dying"

    TIME_BT_POINTS = 0.7 # time between points in the paths

    EXPLOSION = [
        tools.sheet_grab_cells(8, 3),
        tools.sheet_grab_cells(9, 3),
        tools.sheet_grab_cells(10, 3),
        tools.sheet_grab_cells(11, 3, 2, 2),
        tools.sheet_grab_cells(13, 3, 2, 2),
    ]

    def __init__(self, loc, path, formation_spot=None, img_row=2, frames=8):
        pygame.sprite.Sprite.__init__(self)

        self.path = path
        self.state = self.ASSEMBLING
        self.path_index = 0
        self.path_time = 0
        self.formation_spot = [16 * s for s in formation_spot]
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = loc.x, loc.y
        self.death_timer = self.DEATH_TIME
        self.setup_images(img_row, frames)

    def setup_images(self, img_row, frames):
        self.images = [
            tools.sheet_grab_cells(x, img_row) for x in range(frames)]
        self.animation_index = 0
        self.image = self.images[self.animation_index]

    def animate(self, dt):
        if self.state == self.ASSEMBLING:
            pass
        if self.state == self.FORMATION:
            if self.animation_index == 7:
                self.animation_index = 6
            else:
                self.animation_index = 7
        elif self.state == self.DYING:
            pass
        self.image = self.images[self.animation_index]

    def switch_state(self, state):
        self.state = state
        if self.state == self.TO_FORMATION:
            self.path_index = None
        elif self.state == self.FORMATION:
            self.rect.center = self.formation_spot

    def lerp_to(self, dt, point, duration):
        self.path_time += dt
        if self.path_time >= duration:
            self.path_time = 0
            return True
        else:
            goal = Vector2(point)
            percent = self.path_time / duration
            current = Vector2(self.rect.center)
            move_to = current.lerp(goal, percent)
            self.rect.center = move_to

    def update(self, dt):
        if self.state == self.ASSEMBLING:
            complete = self.lerp_to(dt, self.path[self.path_index],
                                    self.TIME_BT_POINTS)
            if complete:
                self.path_index += 1
                if self.path_index == len(self.path):
                    self.switch_state(self.TO_FORMATION)
        elif self.state == self.TO_FORMATION:
            complete = self.lerp_to(dt, self.formation_spot, self.TIME_BT_POINTS)
            if complete:
                self.switch_state(self.FORMATION)
        elif self.state == self.DYING:
            if self.death_timer >= 0:
                self.death_timer -= dt
            else:
                self.kill()

    def hit(self):
        setup.SFX["enemy hit 1"].play()
        self.switch_state(self.DYING)



class Bee(Enemy):
    def __init__(self, loc, path, formation_spot):
        Enemy.__init__(self, loc, path, formation_spot, img_row=5)

class Butterfly(Enemy):
        def __init__(self, loc, path, formation_spot):
            Enemy.__init__(self, loc, path, formation_spot, img_row=4)

class Boss(Enemy):
        def __init__(self, loc, path, formation_spot):
            Enemy.__init__(self, loc, path, formation_spot, img_row=2)
            self.hp = 2

        def hit(self):
            self.hp -= 1
            if self.hp == 0:
                super(Boss, self).hit()
            else:
                self.setup_images(3, 8)
