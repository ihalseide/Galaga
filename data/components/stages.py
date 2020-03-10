from typing import Tuple, Optional

import pygame

from data import constants as c
from data.components.enemies import Butterfly, Bee, EnemyPath, PathPoint, Enemy

TOP_LEFT = 100, -20
TOP_RIGHT = c.GAME_WIDTH - 100, -20

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

    def get_new_enemies(self) -> Tuple[Enemy]:
        if self.waiting_enemies:
            return (self.waiting_enemies.pop(),)

    @property
    def enemy_group_reference(self):
        return self._enemy_group_reference

    @enemy_group_reference.setter
    def enemy_group_reference(self, enemy_group: pygame.sprite.Group):
        assert isinstance(enemy_group, pygame.sprite.Group)
        self._enemy_group_reference = enemy_group

    def has_enemy_group_reference(self):
        return self._enemy_group_reference is not None

    def add_enemy(self, enemy: Enemy):
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
        stage.add_enemy(Bee(50, 50, 0, 0, path=EnemyPath(PathPoint(100, 100, 1)), is_active=True))
        stage.add_enemy(Bee(80, 50, 0, 0, path=EnemyPath(PathPoint(100, 100, 1)), is_active=True))
        stage.add_enemy(Bee(110, 50, 0, 0, path=EnemyPath(PathPoint(100, 100, 1)), is_active=True))
    elif stage_num == 2:
        stage.is_bonus_stage = True
        stage.add_enemy(Bee(100, 100, 0, 0, None))

    return stage
