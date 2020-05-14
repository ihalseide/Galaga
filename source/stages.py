# stages.py
# Author: Izak Halseide

from . import constants as c
from .constants import Point
from .enemy_paths import EnemyPath, Wait
from .sprites import Enemy, Bee, Butterfly, Purple, GalagaSprite

# Some set enemy spawning locations
TOP_LEFT = Point(100, 0)
TOP_RIGHT = Point(c.GAME_SIZE.width - 100, 0)
BOTTOM_LEFT = Point(0, 200)
BOTTOM_RIGHT = Point(c.GAME_SIZE.width, 200)

MAX_ENEMY_ROWS = 12
MAX_ENEMY_COLUMNS = 12

# Times in milliseconds
TIME_BETWEEN_ENEMIES = 500  # 200


class Stage(object):
    """
    Mutable stage object that represents a single stage in Galaga.
    It is mutable for when the representation of the stage is being built.
    """

    def __init__(self, stage_num: int):
        # Initial settings
        self.stage_num = stage_num
        self.is_bonus_stage = False

        # Variables that are stepped when the stage is being defined
        self.enemies = []
        self.wave_0_defined = False
        self.num_of_waves = 0
        self.defining_wave_num = 0
        self.defining_enemy_num = 0
        self.wave_wait_time = 0
        self.current_enemy_origin = None

    def get_new_enemy(self) -> GalagaSprite:
        if self.enemies:
            return self.enemies.pop()

    def queue_enemy(self, enemy_class: Enemy.__class__, formation_x, formation_y, *path_steps):
        if self.current_enemy_origin is None:
            raise ValueError("Current enemy origin is not set!")
        origin_x, origin_y = self.current_enemy_origin
        path = EnemyPath(Wait(self.wave_wait_time), *path_steps)
        enemy = enemy_class(x=origin_x, y=origin_y, formation_x=formation_x, formation_y=formation_y, path=path)
        enemy.number_in_wave = self.defining_enemy_num
        enemy.wave_number = self.defining_wave_num
        self.wave_wait_time += TIME_BETWEEN_ENEMIES
        self.defining_enemy_num += 1
        self.enemies.append(enemy)

    def define_enemy_origin(self, enemy_origin: Point):
        self.current_enemy_origin = enemy_origin

    def roll_to_start_of_wave(self):
        self.defining_enemy_num = 0
        self.wave_wait_time = 0

    def define_next_wave(self, enemy_origin: Point = None):
        if enemy_origin is not None:
            self.define_enemy_origin(enemy_origin)

        self.num_of_waves += 1
        if self.wave_0_defined:
            self.defining_wave_num += 1
        else:
            self.wave_0_defined = True

        self.roll_to_start_of_wave()

    def define_another_squad(self, enemy_origin: Point = None):
        if enemy_origin is not None:
            self.define_enemy_origin(enemy_origin)
        self.roll_to_start_of_wave()


def load_stage(stage_num: int) -> Stage:
    """
    Returns the requested stage for the stage number
    :param stage_num: Should be an int between 1 and 255
    :return: A Stage object, which needs to be given a sprite group reference to spawn enemies into later.
    """

    assert stage_num in range(1, 256)

    stage = Stage(stage_num)

    if stage_num == 1:
        # 4 bees come from the top right and 4 butterflies come from the top left
        stage.define_next_wave(TOP_RIGHT)
        stage.queue_enemy(Bee, formation_x=4, formation_y=3)
        stage.queue_enemy(Bee, formation_x=4, formation_y=4)
        stage.queue_enemy(Bee, formation_x=5, formation_y=3)
        stage.queue_enemy(Bee, formation_x=5, formation_y=4)

        stage.define_another_squad(TOP_LEFT)
        stage.queue_enemy(Butterfly, formation_x=4, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=5, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=4, formation_y=2)
        stage.queue_enemy(Butterfly, formation_x=5, formation_y=2)

        # 4 bosses and 4 butterflies come in alternating order from the bottom left
        stage.define_next_wave(BOTTOM_LEFT)
        stage.queue_enemy(Purple, formation_x=3, formation_y=0)
        stage.queue_enemy(Butterfly, formation_x=3, formation_y=1)
        stage.queue_enemy(Purple, formation_x=4, formation_y=0)
        stage.queue_enemy(Butterfly, formation_x=3, formation_y=2)
        stage.queue_enemy(Purple, formation_x=5, formation_y=0)
        stage.queue_enemy(Butterfly, formation_x=6, formation_y=1)
        stage.queue_enemy(Purple, formation_x=6, formation_y=0)
        stage.queue_enemy(Butterfly, formation_x=6, formation_y=2)

        # 8 butterflies come from the bottom right
        stage.define_next_wave(BOTTOM_RIGHT)
        stage.queue_enemy(Butterfly, formation_x=1, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=1, formation_y=2)
        stage.queue_enemy(Butterfly, formation_x=2, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=2, formation_y=2)
        stage.queue_enemy(Butterfly, formation_x=7, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=7, formation_y=2)
        stage.queue_enemy(Butterfly, formation_x=8, formation_y=1)
        stage.queue_enemy(Butterfly, formation_x=8, formation_y=2)

        # 8 bees come from the top right
        stage.define_next_wave(TOP_RIGHT)
        stage.queue_enemy(Bee, formation_x=2, formation_y=3)
        stage.queue_enemy(Bee, formation_x=2, formation_y=4)
        stage.queue_enemy(Bee, formation_x=3, formation_y=3)
        stage.queue_enemy(Bee, formation_x=3, formation_y=4)
        stage.queue_enemy(Bee, formation_x=6, formation_y=3)
        stage.queue_enemy(Bee, formation_x=6, formation_y=4)
        stage.queue_enemy(Bee, formation_x=7, formation_y=3)
        stage.queue_enemy(Bee, formation_x=7, formation_y=4)

        # 8 bees come from the top left
        stage.define_next_wave(TOP_LEFT)
        stage.queue_enemy(Bee, formation_x=0, formation_y=3)
        stage.queue_enemy(Bee, formation_x=0, formation_y=4)
        stage.queue_enemy(Bee, formation_x=1, formation_y=3)
        stage.queue_enemy(Bee, formation_x=1, formation_y=4)
        stage.queue_enemy(Bee, formation_x=8, formation_y=3)
        stage.queue_enemy(Bee, formation_x=8, formation_y=4)
        stage.queue_enemy(Bee, formation_x=9, formation_y=3)
        stage.queue_enemy(Bee, formation_x=9, formation_y=4)

    elif stage_num == 2:

        pass

    elif stage_num == 3:

        stage.is_bonus_stage = True

    return stage
