import math
from typing import Tuple, Union

import pygame

from data import setup


def lerp(start: float, stop: float, percent: float) -> float:
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


def _font_render(text: str, color: pygame.Color, bg_color: Union[pygame.Color, None] = None):
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
        glyph = grab_sheet(font_data[0], font_data[1], setup.FONT_CHAR_SIZE)
        surf.blit(glyph, (i * setup.FONT_CHAR_SIZE, 0), )
    # replace colors
    pixels = pygame.PixelArray(surf)
    if bg_color:
        pixels.replace(pygame.Color('black'), bg_color)
    pixels.replace(pygame.Color('white'), color)
    pixels.close()
    return surf


def draw_text(screen: pygame.Surface, text: str, position: Tuple[int, int], color: pygame.Color,
              bg_color: Union[pygame.Color, None] = None, centered_y: bool = False, centered_x: bool = False):
    surf = _font_render(text, color, bg_color)
    x, y = position
    width, height = surf.get_size()
    if centered_y:
        y -= height // 2
    if centered_x:
        x -= width // 2
    screen.blit(surf, (x, y))


def grab_sheet(x: int, y: int, width: int, height: Union[int, None] = None) -> pygame.Surface:
    """
    Get a pixel rectangle from an image resource
    """
    # allow square assumption (w = h)
    if height is None:
        height = width
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
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            yield x, y
