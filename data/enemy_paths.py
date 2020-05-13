# enemy_paths.py
# Author: Izak Halseide

from math import cos, sin
from .tools import distance, linear_interpolation, arc_length


class PathStep:

    def __init__(self):
        self.is_done = False

    def update(self, step_timer, x, y, angle):
        raise NotImplementedError()


class Wait(PathStep):

    def __init__(self, wait_time):
        super().__init__()
        self.wait_time = wait_time

    def update(self, step_timer, x, y, angle):
        if step_timer >= self.wait_time:
            self.is_done = True
        return x, y, angle


class TeleportTo(PathStep):

    def __init__(self, x, y, angle=None):
        super(TeleportTo, self).__init__()
        self.x = x
        self.y = y
        self.angle = angle

    def update(self, step_timer, x, y, angle):
        self.is_done = True
        return self.x, self.y, (self.angle or angle)


class MoveTowards(PathStep):

    def __init__(self, end_x, end_y, speed):
        super(MoveTowards, self).__init__()
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed
        assert self.speed != 0
        # To be calculated after the first update...
        self.start_x = None
        self.start_y = None
        self.duration = None

    def update(self, step_timer, x, y, angle):
        # This happens when the step is updated for the first time
        if self.start_x is None:
            self.start_x = x
            self.start_y = y
            dist = distance(self.start_x, self.start_y, self.end_x, self.end_y)
            self.duration = dist / self.speed
            return x, y, angle
        progress = step_timer / self.duration
        x = linear_interpolation(self.start_x, self.end_x, progress)
        y = linear_interpolation(self.start_y, self.end_y, progress)
        return x, y, angle


class MoveOnCircle(PathStep):

    def __init__(self, center_x, center_y, radius, start_angle, end_angle, speed):
        super(MoveOnCircle, self).__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.speed = speed
        assert self.speed != 0
        dist = arc_length(self.start_angle, self.end_angle, self.radius)
        self.duration = dist / self.speed

    def update(self, step_timer, x, y, angle):
        progress = step_timer / self.duration
        angle_from_center = linear_interpolation(self.start_angle, self.end_angle, progress)
        x = self.center_x + self.radius * cos(angle_from_center)
        y = self.center_y + self.radius * sin(angle_from_center)
        return x, y, angle


class EnemyPath:

    def __init__(self, *steps: PathStep):
        self.steps = steps
        self.step_iter = iter(self.steps)
        self.current_step: PathStep = next(self.step_iter)
        self.step_timer = 0
        self.is_done = False
        if not len(self.steps):
            self.is_done = True

    def update(self, delta_time, x, y, angle):
        """
        Given current x, y, angle, output the goal x, y, and angle.
        """
        if self.is_done or self.current_step is None:
            return x, y, angle

        self.step_timer += delta_time

        x, y, angle = self.current_step.update(self.step_timer, x, y, angle)
        step_is_done = self.current_step.is_done

        if step_is_done:
            try:
                self.current_step = next(self.step_iter)
            except StopIteration:
                self.is_done = True
                self.current_step = None
            self.step_timer = 0

        return x, y, angle
