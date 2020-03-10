import math
from typing import Tuple

import pygame

from data import tools
from data.components import galaga_sprite


def move_on_line(start_pos, end_pos, progress) -> Tuple[float, float]:
    x = tools.lerp(start_pos[0], end_pos[0], progress)
    y = tools.lerp(start_pos[1], end_pos[1], progress)
    return x, y


def move_on_circle(circle_center: Tuple[float, float], circle_radius: float, start_angle: float, progress: float) -> \
        Tuple[float, float]:
    """
    Return the x,y position for moving along a circle using linear interpolation
    :param circle_center:
    :param circle_radius:
    :param start_angle: starting angle to the circle in degrees
    :param progress:
    :return:
    """
    # LERP the angle and get x,y out of that
    angle = math.radians(tools.lerp(start_angle, start_angle + 360, progress))
    x = circle_radius * math.cos(angle) + circle_center[0]
    y = circle_radius * math.sin(angle) + circle_center[1]
    return x, y

class PathStep:

    def __init__(self):
        self.progress = 0


class EnemyPath(object):

    def __init__(self, *sequence: PathStep):
        self.sequence = list(sequence)

    def append_node(self, node: PathStep):
        self.sequence.append(node)
        return self


class PathWait(PathStep):

    def __init__(self, wait_time):
        super(PathWait, self).__init__()
        self.wait_time = wait_time


class PathCircle(PathStep):

    def __init__(self, center_x, center_y, radius, start_angle, stop_angle, speed):
        super(PathCircle, self).__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.speed = speed


class PathPoint(PathStep):

    def __init__(self, point_x, point_y, travel_to_speed):
        super(PathPoint, self).__init__()
        self.point_x = point_x
        self.point_y = point_y


class Enemy(galaga_sprite.GalagaSprite):

    # TODO: add path following and circling around, etc.

    def __init__(self, x: int = 0, y: int = 0, is_active = False, path = None, *groups):
        super().__init__(pygame.Rect(x - 8, y - 8, 16, 16), *groups)
        self.x = x
        self.y = y
        self.rotation: float = 0
        self.is_alive = True
        self.is_active: bool = is_active
        self.path: EnemyPath = path

    def kill(self):
        super(Enemy, self).kill()

    def update(self, dt):
        if self.path:
            pass

    def display(self, surface: pygame.Surface):
        super(Enemy, self).display(surface)


class SquadEnemy(Enemy):

    def __init__(self, x, y, formation_x, formation_y, path):
        super(SquadEnemy, self).__init__(x, y, path = path)
        self.formation_x: int = formation_x
        self.formation_y: int = formation_y


class Bee(SquadEnemy):

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None, is_active=False):
        super(Bee, self).__init__(x, y, formation_x, formation_y, path)
        self.is_active = is_active
        self.image = tools.grab_sheet(224, 32, 16)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)


class Butterfly(SquadEnemy):

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Butterfly, self).__init__(x, y, formation_x, formation_y, path)
        self.image = tools.grab_sheet(96, 32, 16)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)


# The enemy that tries to capture the player's fighter
class Boss(SquadEnemy):

    def __init__(self, x: int = 0, y: int = 0, formation_x: int = 0, formation_y: int = 0):
        super(Boss, self).__init__(x, y, formation_x, formation_y)
        self.image = tools.grab_sheet(224, 16, 16)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)
        self.health = 2


# The enemy that spawns after a kill streak
class TrumpetBug(Enemy):

    def __init__(self, x: int, y: int):
        super(TrumpetBug, self).__init__(x, y)
