import pygame

from data import constants as c, hud, stars
from data import scoring
from data import setup
from data import tools
from data.state import State


class Menu(State):
    # A few constants for the menu
    LIGHT_TITLE = setup.get_image('light title')
    GREEN_TITLE = setup.get_image('green title')
    WHITE_TITLE = setup.get_image('white title')
    # Positioning on screen
    SCORE_Y = 10
    TITLE_X = c.GAME_CENTER_X - LIGHT_TITLE.get_rect().width / 2
    TITLE_Y = SCORE_Y + 80
    START_Y = TITLE_Y + 110
    COPY_Y = START_Y + 60
    # Timing and speeds
    MENU_SPEED = 2
    TITLE_FLASH_TIME = 150  # milliseconds
    TITLE_FLASH_NUM = 12

    def __init__(self, persist=None):
        State.__init__(self, persist)
        # init hud
        self.hud = hud.Hud(scoring.get_1up_score(), scoring.get_high_score())
        # initialize the stars
        self.stars = stars.Stars()
        # next state
        self.next = c.PLAY_STATE
        # whether it is in a scrolling state
        self.is_scrolling = True
        self.timer = 0
        # times the title has flashed
        self.flash_num = 0
        # title is flashing now?
        self.is_flashing = False
        self.is_title_white = False
        self.ready = False
        # scrolling menu up
        self.offset_y = c.GAME_HEIGHT

    def set_ready(self):
        self.ready = True
        self.offset_y = 0
        self.is_flashing = True
        self.flash_num = 0

    def cleanup(self) -> dict:
        self.persist[c.HUD] = self.hud
        self.persist[c.STARS] = self.stars
        return self.persist

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in setup.START_KEYS:
                if self.ready:
                    # start the game
                    self.next = c.PLAY_STATE
                    self.done = True
                    self.play_start_noise()
                else:
                    self.set_ready()

    @staticmethod
    def play_start_noise():
        setup.get_sfx('start_noise').play()

    def update(self, delta_time, keys):
        # stars
        self.stars.update(delta_time)
        # hud
        self.hud.update(delta_time)
        # scroll menu
        if self.ready:
            # flash timer
            self.is_flashing = self.flash_num < self.TITLE_FLASH_NUM * 2
            if self.is_flashing:
                self.timer += delta_time
                if self.timer >= self.TITLE_FLASH_TIME:
                    self.timer = 0
                    self.flash_num += 1
                    self.is_title_white = not self.is_title_white
            else:
                pass  # TODO: make it flash later or invoke demo?
        elif self.offset_y > 0:
            self.offset_y -= self.MENU_SPEED
            if self.offset_y <= 0:
                self.set_ready()

    def display(self, screen, delta_time):
        # draw background
        self.hud.display(screen)
        screen.fill(pygame.Color('black'))
        self.stars.display(screen)
        # title normal
        if not self.is_flashing:
            surf = self.LIGHT_TITLE
        elif self.is_title_white:
            surf = self.WHITE_TITLE
        else:
            surf = self.GREEN_TITLE
        screen.blit(surf, (self.TITLE_X, self.TITLE_Y + self.offset_y))
        # hud
        score_1up = 20210  # TODO: use scoring.get_1up_score()
        highscore = 1000  # TODO: use scoring.get_high_score()
        # draw 1up and high score hud
        self.hud.display(screen, self.offset_y)
        # draw start text
        tools.draw_text(screen, c.START, (c.GAME_CENTER_X, self.offset_y + self.START_Y), pygame.Color('white'),
                        centered_x=True)
        # draw copyright on bottom
        tools.draw_text(screen, c.MENU_MESSAGE, (c.GAME_CENTER_X, self.offset_y + self.COPY_Y), pygame.Color('white'),
                        centered_x=True)
