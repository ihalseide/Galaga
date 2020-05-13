# tools.py
# Author: Izak Halseide

import math
import time
import pygame
from functools import wraps
from . import constants as c
from . import setup
from math import sin


def linear_interpolation(start: float, stop: float, percent: float) -> float:
    """
    Linear interpolation function
    :param start: starting value for interpolation
    :param stop: ending value for interpolation
    :param percent: proportion of the way through interpolation (0.0 -> 1.0)
    :return: the interpolated value
    """
    return (1 - percent) * start + percent * stop


def map_value(value, in_start, in_stop, out_start, out_stop):
    """
    Map a value from an input range to an output range
    :param value:
    :param in_start:
    :param in_stop:
    :param out_start:
    :param out_stop:
    :return:
    """
    return out_start + (out_stop - out_start) * ((value - in_start) / (in_stop - in_start))


def _font_render(text: str, color: pygame.Color, bg_color=None):
    """
    Create a pygame image with the text rendered on it using the custom bitmap font
    :param text:
    :param color:
    :param bg_color:
    :return:
    """
    surf = pygame.Surface((len(text) * setup.FONT_CHAR_SIZE, setup.FONT_CHAR_SIZE))
    if bg_color is None:
        surf.set_colorkey(pygame.Color('black'))
    for i, char in enumerate(text):
        # get font location for the char, default to unknown symbol
        font_data = setup.get_from_font(char.lower())
        if not font_data:
            font_data = setup.get_from_font(None)
        # grab the image at location
        glyph = grab_sheet(font_data[0], font_data[1], setup.FONT_CHAR_SIZE, setup.FONT_CHAR_SIZE)
        surf.blit(glyph, (i * setup.FONT_CHAR_SIZE, 0), )
    # replace colors
    pixels = pygame.PixelArray(surf)
    if bg_color:
        pixels.replace(pygame.Color('black'), bg_color)
    pixels.replace(pygame.Color('white'), color)
    pixels.close()
    return surf


def draw_text(surface, text, position, color, background_color=None, center_x=False, center_y=False):
    text_surface = _font_render(str(text), color, background_color)
    x, y = position
    width, height = text_surface.get_size()
    if center_x:
        x -= width // 2
    if center_y:
        y -= height // 2
    if surface is None:
        return text_surface
    else:
        return surface.blit(text_surface, (x, y))


def grab_sheet(x: int, y: int, width: int, height: int) -> pygame.Surface:
    """
    Get a pixel rectangle from an the spritesheet resource
    """
    return setup.get_image('sheet').subsurface((x, y, width, height))


def create_center_rect(x: int, y: int, width: int, height: int) -> pygame.Rect:
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (x, y)
    return rect


def distance(x1: float, y1: float, x2: float, y2: float):
    """
    Return distance between two 2D points.
    """
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def angle_between(x1: float, y1: float, x2: float, y2: float):
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)


def close_to_2d(x1, y1, x2, y2, max_distance=0.001):
    """
    Give whether two points in 2d space are "close enough"
    """
    return distance(x1, y1, x2, y2) <= max_distance


def snap_angle(angle) -> int:
    """
    Return the nearest discrete 8-value angle to a continuous radian angle
    :param angle: input angle in radians
    :return:
    """
    # TODO: implement
    return angle // 8


def clamp_value(n, minimum, maximum):
    """
    Clamp a value between a min and max
    :param n:
    :param minimum:
    :param maximum:
    :return:
    """
    return max(minimum, min(n, maximum))


def range_2d(start_x, start_y, end_x, end_y):
    """
    A range across 2D indices in x and y
    :param start_x:
    :param start_y:
    :param end_x: exclusive
    :param end_y: exclusive
    :return:
    """
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            yield x, y


def irange_2d(start_x, start_y, end_x, end_y):
    """
    Be inclusive with the end_x and end_y
    :param start_x:
    :param start_y:
    :param end_x: inclusive
    :param end_y: inclusive
    :return:
    """
    for x, y in range_2d(start_x, start_y, end_x + 1, end_y + 1):
        yield x, y


def arc_length(start_angle, end_angle, radius):
    """
    Takes angles in radians
    :param start_angle:
    :param end_angle:
    :param radius:
    :return:
    """
    theta = abs(end_angle - start_angle)
    return theta * radius


def calc_stage_badges(stage_num):
    """
    Calculate how many of each stage badges there are for a given stage
    """

    assert stage_num in range(256)

    w_stage = stage_num  # temp. var

    num_50 = w_stage // 50
    w_stage -= num_50 * 50
    num_30 = w_stage // 30
    w_stage -= num_30 * 30
    num_20 = w_stage // 20
    w_stage -= num_20 * 20
    num_10 = w_stage // 10
    w_stage -= num_10 * 10
    num_5 = w_stage // 5
    num_1 = w_stage - num_5 * 5

    return c.StageBadges(num_1, num_5, num_10, num_20, num_30, num_50)


def update_wrapper_ms(func, argument_name="delta_time"):
    """
    Wrapper to make a function keep track of the time elapsed since it's last call.
    Time is tracked in milliseconds
    """

    last_call_time = None

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        nonlocal last_call_time

        now = time.perf_counter_ns()
        if last_call_time is None:
            elapsed = 0
        else:
            elapsed = now - last_call_time
        last_call_time = now
        elapsed_millis = elapsed // 1_000_000

        kwargs[argument_name] = elapsed_millis
        return func(*args, **kwargs)

    return func_wrapper


def calc_formation(time):
    # Time should be in millis

    mod_time = time % c.FORMATION_CYCLE_TIME
    norm_time = 2 * math.pi * mod_time / c.FORMATION_CYCLE_TIME

    middle_spread = (c.FORMATION_MAX_SPREAD + c.FORMATION_MIN_SPREAD) / 2
    spread_magnitude = c.FORMATION_MAX_SPREAD - c.FORMATION_MIN_SPREAD
    offset = sin(norm_time) * spread_magnitude
    spread = round(middle_spread + offset)

    center_x = 0 #c.GAME_CENTER.x
    offset = sin(2 * norm_time) * c.FORMATION_MAX_X
    x = round(center_x + offset)

    return spread, x, c.FORMATION_OFFSET_Y


def calc_formation_pos_from_time(formation_x, formation_y, time):
    spread, x_offset, y_offset = calc_formation(time)
    return calc_formation_pos(formation_x, formation_y, spread, x_offset, y_offset)


def calc_formation_pos(formation_x, formation_y, formation_spread, formation_x_offset, formation_y_offset):
    x = formation_x_offset + formation_x * (16 + formation_spread)
    y = formation_y_offset + formation_y * (16 + formation_spread)
    return x, y


def time_millis():
    return time.perf_counter_ns() // 1_000_000