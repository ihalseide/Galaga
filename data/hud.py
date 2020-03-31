from collections import namedtuple

import pygame

from . import constants as c
from .constants import Point
from .tools import draw_text, grab_sheet

GuiTuple = namedtuple("GuiTuple", "life stage_1 stage_5 stage_10 stage_20 stage_30 stage_50")

BLINK_1UP = 450  # milliseconds

# sprite resources for HUD
ICONS = GuiTuple(grab_sheet(96, 0, 16, 16), grab_sheet(208, 48, 7, 16), grab_sheet(192, 48, 7, 16),
                 grab_sheet(176, 48, 14, 16), grab_sheet(160, 48, 15, 16), grab_sheet(144, 48, 16, 16),
                 grab_sheet(128, 48, 16, 16))


def draw_lives(screen, num_extra_lives):
    # lives
    for i in range(num_extra_lives):
        screen.blit(ICONS.life, (3 + i * 16, c.STAGE_BOTTOM_Y + 1, 16, 16))


def draw_stage_badges(screen, stage_badges, stage_badge_animation_step):
    # draw the stage level badges
    draw_x = c.GAME_SIZE.width
    h = c.BADGE_Y
    number_to_draw = stage_badge_animation_step

    for n in range(stage_badges.stage_1):
        if number_to_draw > 0:
            draw_x -= 8
            screen.blit(ICONS.stage_1, (draw_x, h, 7, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_5):
        if number_to_draw > 0:
            draw_x -= 8
            screen.blit(ICONS.stage_5, (draw_x, h, 7, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_10):
        if number_to_draw > 0:
            draw_x -= 14
            screen.blit(ICONS.stage_10, (draw_x, h, 14, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_20):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_20, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_30):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_30, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_50):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_50, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return


def display(screen: pygame.Surface, one_up_score: int, high_score: int, offset_y: int = 0, num_extra_lives=0,
            stage_badges=None, stage_badge_animation_step=None, show_1up=True):
    # clear the top and bottom for the hud when in play state
    screen.fill(pygame.Color('black'), (0, 0, c.GAME_SIZE.width, c.STAGE_TOP_Y))
    screen.fill(pygame.Color('black'), (0, c.STAGE_BOTTOM_Y, c.GAME_SIZE.width,
                                        c.GAME_SIZE.height - c.STAGE_BOTTOM_Y))

    # 1UP score
    if show_1up:
        draw_text(screen, c.ONE_UP, Point(20, 10 + offset_y), c.RED)
    score_string = c.HI_SCORE_NUM_FORMAT.format(one_up_score)
    draw_text(screen, score_string, Point(20, 20 + offset_y), c.WHITE)

    # high score
    high_score_string = c.HI_SCORE_NUM_FORMAT.format(high_score)
    draw_text(screen, c.HI_SCORE_MESSAGE, Point(c.GAME_CENTER.x, 10 + offset_y), c.RED, center_x=True)
    draw_text(screen, high_score_string, Point(83, 20 + offset_y), c.WHITE)

    if num_extra_lives:
        draw_lives(screen, num_extra_lives=num_extra_lives)

    if stage_badges is not None:
        draw_stage_badges(screen, stage_badges, stage_badge_animation_step)
