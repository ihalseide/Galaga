# main_menu.py


import pygame

from .. import timing
from .. import setup
from .. import constants as c
from .. import scoring
from ..components import stars, hud
from ..tools import font_render

from .state import _State


## A few constants for the menu
LIGHT_TITLE = setup.GFX.get('light title')
GREEN_TITLE = setup.GFX.get('green title')
WHITE_TITLE = setup.GFX.get('white title')

SCORE_Y = 10
TITLE_X = c.CENTER_X - LIGHT_TITLE.get_rect().width/2
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60

# Only used by scroll menu
MENU_SPEED = 2

# Only used by still menu
TITLE_FLASH_TIME = 0.15 # seconds
TITLE_FLASH_NUM = 15


def display_stars_bg(screen):
    # draw background
    screen.fill((0,0,0))
    stars.display(screen)


def display_menu_hud(screen, dt, offset_y=0):
    score_1up = scoring.get_1up_score()
    highscore = scoring.get_highscore()
    # draw 1up and high score hud
    hud.display_scores(screen, dt, score_1up, highscore, SCORE_Y)
    # draw start text
    txt = font_render('Start', pygame.Color('white'))
    w = txt.get_rect().width
    screen.blit(txt, (c.CENTER_X - w//2, offset_y + START_Y))
    # draw copyright?
    txt = font_render('-Copyright or whatever-', pygame.Color('white'))
    w = txt.get_rect().width
    screen.blit(txt, (c.CENTER_X - w//2, offset_y + COPY_Y))


class MenuScroll(_State):

    def __init__(self, persist={}):
        _State.__init__(self, persist)
        # init hud
        hud.init()
        # scrolling menu up
        self.offset_y = c.HEIGHT
        # initialize the stars
        stars.create_stars()
        # always this
        self.next = c.MENU_STILL


    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in setup.START_KEYS:
                # go to menu
                self.done = True


    def update(self, dt, keys):
        # stars
        stars.update(dt)
        # scroll menu
        if self.offset_y > 0:
            self.offset_y -= MENU_SPEED
        else:
            self.done = True            


    def display(self, screen, dt):
        # draw background
        display_stars_bg(screen)
        # title normal
        screen.blit(LIGHT_TITLE, (TITLE_X, TITLE_Y + self.offset_y))
        # hud
        display_menu_hud(screen, dt, self.offset_y)

                    
class Menu(_State):

    def __init__(self, persist={}):
        _State.__init__(self, persist)
        self.timer = timing.ToggleTicker(TITLE_FLASH_TIME)
        self.flash_num = 0
        self.flashing = True


    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in setup.START_KEYS:
                # start the game
                self.next = c.PLAY_NORMAL
                self.done = True


    def update(self, dt, keys):
        # stars
        stars.update(dt)
        # flash timer
        self.flashing = self.flash_num < TITLE_FLASH_NUM * 2
        if self.flashing:
            changed = self.timer.update(dt)
            if changed:
                self.flash_num += 1
                
				
    def display(self, screen, dt):
        # bg
        display_stars_bg(screen)
        # draw title sprite
        if not self.flashing:
            surf = LIGHT_TITLE
        elif self.timer.on:
            surf = WHITE_TITLE
        else:
            surf = GREEN_TITLE
        screen.blit(surf, (TITLE_X, TITLE_Y))
        # hud
        display_menu_hud(screen, dt)
        

