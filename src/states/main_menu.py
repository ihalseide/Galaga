
import pygame

from .. import setup
from .. import constants as c
from .. import scoring
from ..components import stars, hud
from ..tools import font_render

from .state import _State

class Menu(_State):

    MENU_SPEED = 2
    SCORE_Y = 10
    TITLE = setup.GFX.get('title')
    print(setup.GFX)
    TITLE_X = c.CENTER_X - TITLE.get_rect().width/2
    TITLE_Y = SCORE_Y + 80
    START_Y = TITLE_Y + 110
    COPY_Y = START_Y + 60 

    def __init__(self):
        _State.__init__(self)

    def startup(self, persist={}):
        _State.startup(self, persist)
        # init hud
        hud.init()
        # scrolling menu up
        self.menu_y = c.HEIGHT
        # initialize the stars
        stars.create_stars()
        # get scores
        self.scores = scoring.get_scores()
        self.score = 0
        self.highscore = scoring.get_highscore()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.menu_y == 0:
                    # start the game
                    self.next = c.PLAY_STATE
                    self.done = True
                else:
                    # go to menu
                    self.menu_y = 0

    def update(self, dt, keys):
        # stars
        stars.update(dt)
        # scroll menu
        if self.menu_y > 0:
            self.menu_y -= self.MENU_SPEED
        elif self.menu_y < 0:
            self.menu_y = 0

    def display(self, screen, dt):
        # draw background
        screen.fill((0,0,0))
        stars.display(screen)
        # draw 1up and high score hud
        hud.display_scores(screen, dt, self.score, self.highscore, 
                            self.SCORE_Y + self.menu_y)
        # draw title sprite
        if self.menu_y == 0:
            # TODO: blink the title
            pass
        else:
            y = self.menu_y + self.TITLE_Y
            screen.blit(self.TITLE, (self.TITLE_X, y))
        # draw start
        txt = font_render('Start', pygame.Color('white'))
        w = txt.get_rect().width
        screen.blit(txt, (c.CENTER_X - w//2, self.menu_y + self.START_Y))
        # draw copyright?
        txt = font_render('Copyright? or whatever...',
                          pygame.Color('magenta'))
        w = txt.get_rect().width
        screen.blit(txt, (c.CENTER_X - w//2, self.menu_y + self.COPY_Y))

