
from collections import namedtuple

from constants import *
from game_objects import *

LEFT, TOP, RIGHT = 0, 1, 2

EnemySpot = namedtuple("EnemySpot", ["enemy", "row", "col"])
Wave = namedtuple("Wave", ["enemies", "path"])
SpaceTime = namedtuple("SpaceTime", ["x", "y", "t"]) # time relative to wave
Stage = namedtuple("Stage", ["challenging", "wave_groups"])

def ChallengeEnemy(enemy):
    return EnemySpot(enemy, None, None)

def span(start, stop=None, step=1):
    return range(start, stop+1, step)

def fill_enemy(enemy_type, start_row, start_col, end_row, end_col):
    return [EnemySpot(enemy_type, r, c) for r in span(start_row, end_row)
            for c in span(start_col, end_col)]

def get_slot(side, index):
    """
    Returns a spacetime for an enemy to start at
    """
    s = index * 16
    if side == TOP:
        y = 0
        x = s
    elif side == LEFT:
        x = 0
        y = s
    elif side == RIGHT:
        x = WIDTH
        y = s
    return SpaceTime(x, y, 0)

stages = [
    # 1
    Stage(challenging=False, wave_groups=[
        [Wave(enemies = fill_enemy(Bee, 1, 2, 4, 5),
              path = [get_slot(TOP, 6), # center to the right
                      SpaceTime(WIDTH * 1/4, HEIGHT * 3/4, 0.5)]),
         Wave(enemies = fill_enemy(Butterfly, 3, 4, 4, 5),
              path = [get_slot(TOP, 6), # center to the right
                      SpaceTime(WIDTH * 3/4, HEIGHT * 3/4, 0.5)])],
        [Wave(enemies = [EnemySpot(Boss, 0, 4)],
              path = [get_slot(LEFT, 6)])]
    ]),

    # 2
    Stage(challenging=False, wave_groups=[

    ]),

    # 3
    Stage(challenging=True, wave_groups=[

    ])
]
