"""
Galaga clone

Dependencies:
    - Python 3
    - pygame
    - elvector

Hardware
    - screen
    - input
    - raspberry pi
    - sound
    - sound

Input (min)
    - 4 directions
    - fire button

TODO
    - main menu
            - show scores
            - title
            - font
    - play
            - stages
            - enemy programming
            - player abduction
              - double ship
              - captured ship
              - tractor beam
            - shooting
            - show stats on game over
    - high score entry
            - interface
"""

import sys
import json

import pygame

from constants import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))

import states
import play_state
import game_objects as gobs

class Control(object):
    def __init__(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.running = True
        self.clock = pygame.time.Clock()
        self.paused = False
        self.fps = FPS
        self.out_screen = pygame.display.get_surface()
        self.screen = pygame.Surface((WIDTH,
                                      HEIGHT)).convert(self.out_screen)
        self.time = 0

        self.state.startup(self.time, {})

    def flip_state(self):
        persist = self.state.cleanup()
        prev, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def events(self):
        for event in pygame.event.get():
            t = event.type
            if t == pygame.QUIT:
                self.running = False
            elif t == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_ESCAPE:
                    self.running = False
            self.state.get_event(event)
        return pygame.key.get_pressed()

    def main(self):
        while self.running:
            # millis --> seconds
            dt = self.clock.tick(self.fps) / 1000
            self.time += dt

            keys = self.events()
            if not self.paused:
                self.state.update(dt, keys)

            if self.state.done:
                self.flip_state(self)
            elif self.state.quit:
                self.running = False

            self.state.display(self.screen, dt)
            # scale up to output
            pygame.transform.scale(self.screen, (WIDTH*2, HEIGHT*2),
                                   self.out_screen)
            pygame.display.update()

def main():
    state_dict = {
        START_STATE: states.StartState(),
        PLAY_STATE: play_state.PlayState(),
        SCORED_STATE: states.ScoreState()
    }
    con = Control(state_dict, PLAY_STATE)
    con.main()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
