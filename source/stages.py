
from collections import namedtuple

from .constants import WIDTH, HEIGHT
from .components.enemies import *

LEFT, TOP, RIGHT = 0, 1, 2

EnemySpot = namedtuple("EnemySpot", ["enemy", "row", "col"])
Wave = namedtuple("Wave", ["enemies", "start_slot", "path"])
Point = namedtuple("Point", ["x", "y"])

# paths
P = Point
test_path = [P(WIDTH//2,0), P(WIDTH//2, HEIGHT//3), P(WIDTH//2, 2*HEIGHT//3), P(0,0)]

class Stage(object):
    def __init__(self, challenging:bool, wave_groups:list):
        self.wave_groups = wave_groups
        self.challenging = challenging
        self.stage_num = None

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
    return Point(x, y)

stages = [
    None,
    # 1
    Stage(challenging=False, wave_groups=[
        [Wave(enemies = fill_enemy(Bee, 1, 2, 4, 5),
              start_slot = get_slot(TOP, 6),
              path = test_path),
         Wave(enemies = fill_enemy(Butterfly, 3, 4, 4, 5),
              start_slot = get_slot(TOP, 6),
              path = test_path)],
        [Wave(enemies = [EnemySpot(Boss, 0, 4)],
              start_slot = get_slot(LEFT, 6),
              path = test_path)]
    ])
]
for i, s in enumerate(stages):
    if s is not None:
        s.stage_num = i
