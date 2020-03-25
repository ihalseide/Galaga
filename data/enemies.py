__author__ = "Izak Halseide"

import pygame

from data import tools
from data.enemy_paths import EnemyPath
from data.galaga_sprite import GalagaSprite


class Enemy(GalagaSprite):
    pass


class Bee(Enemy):
    """
    Normal enemy
    """

    FRAMES = [(128, 32, 16, 16), (144, 32, 16, 16), (160, 32, 16, 16), (176, 32, 16, 16),
              (192, 32, 16, 16), (208, 32, 16, 16), (224, 32, 16, 16), (240, 32, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Bee, self).__init__(x, y, 16, 16)
        self.image = tools.grab_sheet(224, 32, 16, 16)
        self.frame_num = 7
        self.is_in_formation = False
        self.formation_x = formation_x
        self.formation_y = formation_y
        self.path = path
        self.angle = 0

    def display(self, surface: pygame.Surface):
        x, y, w, h = self.FRAMES[self.frame_num]
        self.image = tools.grab_sheet(x, y, w, h)
        super(Bee, self).display(surface)

    def update(self, delta_time: int, flash_flag: bool):
        if self.is_in_formation:
            if flash_flag:
                self.frame_num = 6
            else:
                self.frame_num = 7
        elif self.path is not None:
            # Not using the angle right now
            self.x, self.y, _ = self.path.update(delta_time, self.x, self.y, self.angle)


class Butterfly(Enemy):
    """
    Normal enemy
    """

    FRAMES = [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16), (48, 32, 16, 16),
              (64, 32, 16, 16), (80, 32, 16, 16), (96, 32, 16, 16), (112, 32, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Butterfly, self).__init__(x, y, 16, 16)
        self.image = tools.grab_sheet(224, 32, 16, 16)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)
        self.frame_num = 7
        self.is_in_formation = False

    def flash_update(self):
        if self.is_in_formation:
            if self.frame_num == 7:
                self.frame_num = 6
            elif self.frame_num == 6:
                self.frame_num = 7

    def choose_image(self):
        self.image = tools.grab_sheet(*self.FRAMES[self.frame_num])

    def display(self, surface: pygame.Surface):
        self.choose_image()
        super(Butterfly, self).display(surface)
        # tools.draw_text(surface, "Bee at: {}, {}".format(self.x, self.y), (40, 40), pygame.Color('yellow'))

    def update(self, delta_time: int, flash_flag: bool):
        pass


class TractorEnemy(Enemy):
    """
    The enemy that tries to capture the player's fighter
    """

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(TractorEnemy, self).__init__(x, y, 16, 16)
        self.image = tools.grab_sheet(128, 16, 16, 16)


class TrumpetBug(Enemy):
    """
    The enemy that spawns after a kill streak
    """
    pass
