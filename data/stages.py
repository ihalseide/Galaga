__author__ = "Izak Halseide"

from collections import namedtuple

import pygame

from data import constants as c
from data.enemies import Butterfly, Bee, TractorEnemy
from data.enemy_paths import EnemyPath, Wait
from data.galaga_sprite import GalagaSprite
from data.tools import range_2d

Point = namedtuple("Point", "x y")

TOP_LEFT = Point(100, 0)
TOP_RIGHT = Point(c.GAME_WIDTH - 100, 0)
BOTTOM_LEFT = Point(0, 200)
BOTTOM_RIGHT = Point(c.GAME_WIDTH, 200)

MAX_ENEMY_ROWS = 12
MAX_ENEMY_COLUMNS = 12

# how long a squad waits to spawn the next enemy
SQUAD_INTERVAL = 0.5  # seconds
WAVE_INTERVAL = 0.6  # seconds


class Stage(object):

    def __init__(self, stage_num: int, is_bonus_stage: bool = False):
        self.is_bonus_stage = is_bonus_stage
        self.is_done_spawning = False
        self.stage_num = stage_num
        self.waiting_enemies = []
        self._enemy_group_reference = None

    def get_new_enemy(self) -> GalagaSprite:
        if self.waiting_enemies:
            return self.waiting_enemies.pop()

    @property
    def enemy_group_reference(self):
        return self._enemy_group_reference

    @enemy_group_reference.setter
    def enemy_group_reference(self, enemy_group: pygame.sprite.Group):
        assert isinstance(enemy_group, pygame.sprite.Group)
        self._enemy_group_reference = enemy_group

    def has_enemy_group_reference(self):
        return self._enemy_group_reference is not None

    def add_enemy(self, enemy: GalagaSprite):
        self.waiting_enemies.append(enemy)

    def update(self, dt: float):
        pass


def load_stage(stage_num: int) -> Stage:
    """
    Returns the requested stage for the stage number
    :param stage_num: Should be an int between 1 and 255
    :return: A Stage object, which needs to be given a sprite group reference to spawn enemies into later.
    """
    stage = Stage(stage_num)

    if stage_num == 1:
        wait_time = 0
        time_between_enemies = 200
        time_between_waves = 800

        # 4 bees come from the top right and 4 butterflies come from the top left
        for x, y in range_2d(start_x=4, start_y=3, end_x=6, end_y=5):
            stage.add_enemy(Bee(x=TOP_RIGHT.x, y=TOP_RIGHT.y, formation_x=x, formation_y=y,
                                path=EnemyPath(Wait(wait_time))))
            wait_time += time_between_enemies
        wait_time = 0
        for x, y in range_2d(start_x=4, start_y=1, end_x=6, end_y=3):
            stage.add_enemy(Butterfly(x=TOP_LEFT.x, y=TOP_LEFT.y, formation_x=x, formation_y=y,
                                      path=EnemyPath(Wait(wait_time))))
            wait_time += time_between_enemies

        # 4 bosses and 4 butterflies come in alternating order from the bottom left
        wait_time += time_between_waves
        this_wave_time = wait_time
        for x, y in range_2d(3, 0, 7, 1):
            stage.add_enemy(TractorEnemy(x=BOTTOM_LEFT.x, y=BOTTOM_LEFT.y, formation_x=x, formation_y=y,
                                         path=EnemyPath(Wait(wait_time))))
            wait_time += time_between_enemies
        wait_time = this_wave_time
        wait_time += time_between_enemies
        stage.add_enemy(Butterfly(x=BOTTOM_LEFT.x, y=BOTTOM_LEFT.y, formation_x=3, formation_y=1,
                                  path=EnemyPath(Wait(wait_time))))
        wait_time += time_between_enemies
        stage.add_enemy(Butterfly(x=BOTTOM_LEFT.x, y=BOTTOM_LEFT.y, formation_x=3, formation_y=2,
                                  path=EnemyPath(Wait(wait_time))))
        wait_time += time_between_enemies
        stage.add_enemy(Butterfly(x=BOTTOM_LEFT.x, y=BOTTOM_LEFT.y, formation_x=6, formation_y=1,
                                  path=EnemyPath(Wait(wait_time))))
        wait_time += time_between_enemies
        stage.add_enemy(Butterfly(x=BOTTOM_LEFT.x, y=BOTTOM_LEFT.y, formation_x=6, formation_y=2,
                                  path=EnemyPath(Wait(wait_time))))
        wait_time += time_between_enemies
        # 8 butterflies come from the bottom right
        # 8 bees come from the top right
        # 8 bees come from the top left
    elif stage_num == 2:
        stage.is_bonus_stage = True
        stage.add_enemy(Bee(100, 100, 0, 0, None))

    return stage
