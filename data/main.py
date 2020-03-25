__author__ = "Izak Halseide"

import pygame

from data import constants as c, statistics, demo, play_state, main_menu, new_high_score
from data.state import State


class Control(object):
    """
    Main class for running the game states and window
    """

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = c.FPS
        self.paused = False
        self.running = True
        self.screen = pygame.display.get_surface()

        # state variables
        self.state_dict = {}
        self.state_name = ''
        self.state: State = State()

    def setup_states(self, state_dict: dict, start_state: State):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]({})

    def flip_state(self):
        persist = self.state.cleanup()
        prev, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name](persist)

    def events(self):
        for event in pygame.event.get():
            t = event.type
            if t == pygame.QUIT:
                self.running = False
            self.state.get_event(event)
        return pygame.key.get_pressed()

    def main(self):
        while self.running:
            # TODO: fix huge delta times when the window gets unfocused or something
            delta_time = self.clock.tick(self.fps)

            # Poll events and get the pressed keys from pygame
            pressed_keys = self.events()

            self.state.update(delta_time, pressed_keys)

            if self.state.done:
                self.flip_state()
            elif self.state.quit:
                self.running = False

            self.state.display(self.screen, delta_time)
            pygame.display.update()


def main():
    the_app = Control()
    state_dict = {
        c.MENU_STATE: main_menu.Menu,
        c.PLAY_STATE: play_state.Play,
        c.NEW_SCORE_STATE: new_high_score.HighScore,
        c.PLAY_STATS: statistics.Stats,
        c.MENU_DEMO: demo.Demo
    }
    the_app.setup_states(state_dict, c.MENU_STATE)
    the_app.main()
