__author__ = "Izak Halseide"

import math

import pygame

from data import constants as c
from data import tools
from data.components import galaga_sprite


class PathStep:

    def __init__(self, max_time=-1):
        self.is_done = False
        self.max_time = max_time
        self.x = None
        self.y = None
        self.angle = None
        self.is_setup = False

    def setup_positions(self, x, y, angle=c.ANGLE_UP):
        self.x = x
        self.y = y
        self.angle = angle
        self.is_setup = True

    def update(self, delta_time, current_x, current_y, current_angle):
        raise ValueError("Not implemented.")


class WaitStep(PathStep):

    def __init__(self, wait_time):
        # The EnemyPath class will do the work of letting the step last as long as the wait_time
        super(WaitStep, self).__init__(max_time=wait_time)

    def update(self, delta_time, current_x, current_y, current_angle):
        self.x = current_x
        self.y = current_y
        self.angle = current_angle


class LinearMoveStep(PathStep):

    def __init__(self, goal_x, goal_y, travel_time):
        super(LinearMoveStep, self).__init__(max_time=travel_time)
        self.start_x = None
        self.start_y = None
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.travel_time = travel_time
        self.current_time = 0

    def setup_positions(self, x, y, angle=c.ANGLE_UP):
        super(LinearMoveStep, self).setup_positions(x, y, angle)
        self.start_x = x
        self.start_y = y

    def update(self, delta_time, current_x, current_y, current_angle):
        if self.is_done:
            self.x = self.goal_x
            self.y = self.goal_y
            return
        self.x = current_x
        self.y = current_y
        self.angle = current_angle
        self.current_time += delta_time
        progress = tools.clamp_value(self.current_time / self.travel_time, 0, 1)
        self.x = tools.lerp(self.start_x, self.goal_x, progress)
        self.y = tools.lerp(self.start_y, self.goal_y, progress)
        if tools.close_to_2d(self.x, self.y, self.goal_x, self.goal_y):
            self.is_done = True


class OrbitStep(PathStep):

    def __init__(self, orbit_center_x, orbit_center_y, orbit_radius, start_orbit_angle, end_orbit_angle, travel_time,
                 do_change_angle=True):
        super(OrbitStep, self).__init__(max_time=travel_time)
        self.orbit_center_x = orbit_center_x
        self.orbit_center_y = orbit_center_y
        self.orbit_radius = orbit_radius
        self.start_orbit_angle = start_orbit_angle
        self.end_orbit_angle = end_orbit_angle
        self.travel_time = travel_time
        self.do_change_angle = do_change_angle

    def calc_position(self):
        # TODO: finish
        x = self.orbit_center_x + math.cos(self.start_orbit_angle) * self.orbit_radius
        y = self.orbit_center_y + math.sin(self.start_orbit_angle) * self.orbit_radius
        if self.do_change_angle:
            self.angle = self.start_orbit_angle + (math.pi / 2.0)  # TODO: maybe (-) instead of (+)??
        return x, y


class EnemyPath:

    def __init__(self, *sequence: PathStep):
        self._sequence = sequence
        self._current_step_index = 0
        self._current_step: PathStep = self._sequence[self._current_step_index]
        self._step_timer = 0

        self.is_done = False

        # variables that the path "follows"
        self.x = None
        self.y = None
        self.angle = None
        self.is_setup = False

    def setup_positions(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.is_setup = True
        if not self._current_step.is_setup:
            self._current_step.setup_positions(x, y, angle)

    @property
    def current_step(self):
        return self._current_step

    def update(self, delta_time):
        if self.is_done or (not self.is_setup):
            return
        self._step_timer += delta_time
        if self.current_step.is_done:
            # last step = entire path is done
            if self._current_step_index >= len(self._sequence) - 1:
                self.is_done = True
                return
            # next
            self._current_step_index += 1
            self._current_step = self._sequence[self._current_step_index]
            self._current_step.setup_positions(self.x, self.y, self.angle)
            self._step_timer = 0
            return
        elif 0 <= self._current_step.max_time <= self._step_timer:
            self._current_step.is_done = True

        self._current_step.update(delta_time, self.x, self.y, self.angle)

        # save new values
        self.x = self._current_step.x
        self.y = self._current_step.y
        self.angle = self._current_step.angle


class Enemy(galaga_sprite.GalagaSprite):

    def __init__(self, x: int, y: int, angle: int = c.ANGLE_UP, path: EnemyPath = None, *groups):
        super().__init__(x, y, 16, 16, *groups)
        self.angle = angle
        self.is_alive = True
        self.frame_num = 0

        # Path to follow
        self._path: EnemyPath = path
        if self._path:
            self._path.setup_positions(self.x, self.y, self.angle)

    @property
    def path(self):
        return self._path

    def update(self, delta_time):
        if self._path:
            self._path.update(delta_time)
            self.x = self._path.x
            self.y = self._path.y
            self.angle = self._path.angle

    def display(self, surface: pygame.Surface):
        super(Enemy, self).display(surface)


class FormationEnemy(Enemy):
    formation_state = None
    formation_function = None

    @classmethod
    def go_to_formation_path(cls, formation_x, formation_y):
        assert cls.formation_state is not None
        assert cls.formation_function is not None
        x, y = cls.formation_function(formation_x, formation_y)
        return EnemyPath(LinearMoveStep(x, y, 600))

    @classmethod
    def set_formation_pos_function(cls, function, state):
        cls.formation_function = function
        cls.formation_state = state

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(FormationEnemy, self).__init__(x, y, path=path)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)
        self.formation_x = formation_x
        self.formation_y = formation_y
        self.is_in_formation = False

    def update(self, delta_time):
        super(FormationEnemy, self).update(delta_time)
        if self._path and self._path.is_done and not self.is_in_formation:
            self._path = self.go_to_formation_path(self.formation_x, self.formation_y)
            self._path.setup_positions(self.x, self.y, self.angle)
            self.is_in_formation = True


class Bee(FormationEnemy):
    """
    Normal enemy
    """

    FRAMES = [(128, 32, 16, 16), (144, 32, 16, 16), (160, 32, 16, 16), (176, 32, 16, 16),
              (192, 32, 16, 16), (208, 32, 16, 16), (224, 32, 16, 16), (240, 32, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Bee, self).__init__(x, y, formation_x, formation_y, path=path)
        self.image = tools.grab_sheet(224, 32, 16)
        self.rect = tools.create_center_rect(self.x, self.y, 16, 16)
        self.frame_num = 7

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
        super(Bee, self).display(surface)
        # tools.draw_text(surface, "Bee at: {}, {}".format(self.x, self.y), (40, 40), pygame.Color('yellow'))

    def update(self, delta_time):
        super(Bee, self).update(delta_time)


class Butterfly(FormationEnemy):
    """
    Normal enemy
    """


class Boss(Enemy):
    """
    The enemy that tries to capture the player's fighter
    """
    pass


class TrumpetBug(Enemy):
    """
    The enemy that spawns after a kill streak
    """
    pass
