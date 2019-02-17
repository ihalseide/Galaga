"""
Code for the shared HUD drawing between the menu state and the play state
"""
import pygame

from .. import constants as c
from .. import setup
from .. import timing
from ..tools import font_render

BLINK_1UP = 0.45 # seconds

def init():
    global _timer_1up, _blinking_1up
    _timer_1up = timing.ToggleTicker(BLINK_1UP)
    _blinking_1up = False

def set_blinking_1up(value):
    global _blinking_1up
    _blinking_1up = bool(value)

# play state drawing
def draw_for_play(screen, dt, score, highscore):
    clear_top(screen)
    display_scores(screen, dt, score, highscore)

def clear_top(screen):
    pygame.draw.rect(screen, pygame.Color('black'), (0, 0, c.WIDTH, 20))

def display_scores(screen, dt, score, highscore, offset_y=0):
    _timer_1up.update(dt)
    if not _blinking_1up or _timer_1up.on:
        t = font_render("1 UP", pygame.Color('red'))
        screen.blit(t, (22, 1 + offset_y))
    if score == 0:
        score = "00"
    else:
        score = str(self.score).zfill(round(math.log(self.score, 10)))
    t = font_render(score, pygame.Color('white'))
    w = t.get_rect().width
    screen.blit(t, (60-w, 10 + offset_y))
    t = font_render("HI-SCORE", pygame.Color('red'))
    size = t.get_rect().width
    screen.blit(t, ((c.WIDTH - size)//2, 1 + offset_y))
    score = str(highscore)
    t = font_render(score, pygame.Color('white'))
    size = t.get_rect().width
    screen.blit(t, ((c.WIDTH - size)//2, 10 + offset_y))
