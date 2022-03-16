# states.py

import pygame
from pygame.math import Vector2
from . import constants as c, tools, setup, hud, scoring, sprites
from .setup import play_sound, stop_sounds
from .stars import StarField
from .tools import calc_stage_badges, draw_text

GAME_OVER_DURATION = 3000

# For displaying the text in the middle for the play state
LINE_TEXT_HEIGHT = 16

# Title settings
LIGHT_TITLE = setup.get_image('light_title')
GREEN_TITLE = setup.get_image('green_title')
WHITE_TITLE = setup.get_image('white_title')
SCORE_Y = 10
TITLE_X = c.GAME_CENTER.x - LIGHT_TITLE.get_rect().width // 2
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60
MENU_SPEED = 3
TITLE_FLASH_TIME = 150  # millis.
TITLE_FLASH_NUM = 12

# How many milliseconds to show the game over screen
GAME_OVER_STATE_DURATION = 14500


def draw_mid_text(screen, text, color, line=1):
    x, y = c.GAME_CENTER.x, c.GAME_CENTER.y + LINE_TEXT_HEIGHT * (line - 1)
    tools.draw_text(screen, text, (x, y), color, center_y=True, center_x=True)


class State:
    """
    Base class for game states.
    """

    def __init__(self, persist):
        self.persist: c.Persist = persist
        self.next_state_name = None  # Next state
        self.is_done = False  # Ready to switch to next state
        self.is_quit = False  # Wants to quit the program
        self.current_time = 0  # Current time since the beginning of the pygame ticks
        self.start_time = 0  # When the state started

    def cleanup(self):
        return self.persist

    def get_event(self, event: pygame.event.Event):
        raise NotImplementedError()

    def update(self, delta_time: int, keys: list):
        raise NotImplementedError()

    def display(self, surface: pygame.Surface):
        raise NotImplementedError()


class Title(State):

    def __init__(self, persist):
        # initialize the persistent data because it is the initial state
        if persist is None:
            scores = scoring.load_scores()
            high_score = max(scores, key=lambda record: record.score).score
            persist = c.Persist(stars=StarField(),
                                scores=scores,
                                current_score=0,
                                one_up_score=0,
                                high_score=high_score,
                                num_shots=0,
                                num_hits=0,
                                stage_num=0)
        State.__init__(self, persist)

        # whether it is in a scrolling state
        self.is_scrolling = True
        self.timer = 0

        # times the title has flashed
        self.flash_num = 0
        self.is_flashing = False
        self.is_title_white = False
        self.ready = False

        # scrolling menu up
        self.offset_y = c.GAME_SIZE.height

    def set_ready(self):
        self.ready = True
        self.offset_y = 0
        self.is_flashing = True
        self.flash_num = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in setup.START_KEYS:
                if self.ready:
                    # start the game
                    self.next_state_name = c.PLAY_STATE
                    self.is_done = True
                else:
                    self.set_ready()

    def update(self, delta_time, keys):
        # stars
        self.persist.stars.update(delta_time)
        # scroll menu
        if self.ready:
            # flash timer
            self.is_flashing = self.flash_num < TITLE_FLASH_NUM * 2
            if self.is_flashing:
                self.timer += delta_time
                if self.timer >= TITLE_FLASH_TIME:
                    self.timer = 0
                    self.flash_num += 1
                    self.is_title_white = not self.is_title_white
            else:
                pass  # TODO: make it flash later or invoke demo?
        elif self.offset_y > 0:
            self.offset_y -= MENU_SPEED
            if self.offset_y <= 0:
                self.set_ready()

    def display(self, screen):
        # draw background
        screen.fill(c.BLACK)
        self.persist.stars.display(screen)
        # title normal
        if not self.is_flashing:
            surf = LIGHT_TITLE
        elif self.is_title_white:
            surf = WHITE_TITLE
        else:
            surf = GREEN_TITLE
        screen.blit(surf, (TITLE_X, TITLE_Y + self.offset_y))
        # draw 1up and high score hud
        hud.display(screen, one_up_score=0, high_score=0, offset_y=self.offset_y)
        # draw start text
        tools.draw_text(screen, c.START_TEXT, (c.GAME_CENTER.x, self.offset_y + START_Y), c.WHITE, center_x=True)
        # draw footer on bottom
        tools.draw_text(screen, c.TITLE_FOOTER_TEXT, (c.GAME_CENTER.x, self.offset_y + COPY_Y), c.WHITE, center_x=True)


class GameOver(State):

    def __init__(self, persist):
        super(GameOver, self).__init__(persist)
        play_sound("game_over")
        self.start_time = pygame.time.get_ticks()

        self.persist.stars.moving = 1

        self.stage_badges = calc_stage_badges(self.persist.stage_num)

        # Just render the surface once
        if self.persist.num_shots == 0:
            self.ratio = 0
        else:
            self.ratio = self.persist.num_hits / self.persist.num_shots

    def get_event(self, event: pygame.event.Event):
        pass

    def update(self, delta_time: int, keys: list):
        self.persist.stars.update(delta_time)
        if self.current_time > self.start_time + GAME_OVER_STATE_DURATION:
            self.is_done = True
            self.next_state_name = c.TITLE_STATE
            stop_sounds()

    def display(self, screen: pygame.Surface):
        screen.fill(c.BLACK)
        self.persist.stars.display(screen)

        x, y = c.GAME_CENTER.x, 100

        draw_text(surface=screen, text=c.RESULT_TEXT,
                  position=(x, y), color=c.RED, center_x=True)

        x = c.GAME_CENTER.x - 100
        draw_text(surface=screen, text=c.SHOTS_FIRED_TEXT.format(self.persist.num_shots),
                  position=(x, y + 16), color=c.LIGHT_BLUE)

        draw_text(surface=screen, text=c.NUM_HITS_TEXT.format(self.persist.num_hits),
                  position=(x, y + 32), color=c.WHITE)

        draw_text(surface=screen, text=c.HIT_MISS_RATIO.format(self.ratio),
                  position=(x, y + 48), color=c.YELLOW)

        hud.display(screen, one_up_score=self.persist.one_up_score, high_score=self.persist.high_score,
                    stage_badges=self.stage_badges, stage_badge_animation_step=sum(self.stage_badges))


class Demo(State):
    # TODO: implement

    def update(self, delta_time: int, keys):
        pass

    def display(self, surface: pygame.Surface):
        pass

    def get_event(self, event: pygame.event.Event):
        pass


class ScoreEntry(State):

    def __init__(self, persist):
        super(ScoreEntry, self).__init__(persist)

    def get_event(self, event: pygame.event.Event):
        pass

    def update(self, delta_time: int, keys: list):
        pass

    def display(self, surface: pygame.Surface):
        pass
