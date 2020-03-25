import pygame

from data import constants as c
from data.tools import draw_text


class Hud:
    BLINK_1UP = 450  # milliseconds

    def __init__(self, display_score: int, high_score: int):
        self._display_score = int(display_score)
        self._high_score = int(high_score)

    def set_display_score(self, score):
        self._display_score = score

    def set_display_high_score(self, score: int):
        self._high_score = score

    def update(self, dt: float):
        pass

    def display(self, screen, offset_y=0):
        # 1UP score
        score_string = c.HI_SCORE_NUM.format(self._display_score)
        draw_text(screen, c.ONE_UP, (20, 10 + offset_y), pygame.Color('red'))
        draw_text(screen, score_string, (20, 20 + offset_y), pygame.Color('white'))
        # high score
        high_score_string = c.HI_SCORE_NUM.format(self._high_score)
        draw_text(screen, c.HI_SCORE, (c.GAME_CENTER_X, 10 + offset_y), pygame.Color('red'), centered_x=True)
        draw_text(screen, high_score_string, (83, 20 + offset_y), pygame.Color('white'))
