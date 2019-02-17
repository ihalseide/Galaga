
import pygame

from . import constants as c

class Control(object):
    """
    Main class for running the game states and window
    """

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.paused = False
        self.fps = c.FPS
        self.screen = pygame.display.get_surface()

        self.state_dict = None
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup({})

    def flip_state(self):
        persist = self.state.cleanup()
        prev, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup(persist)

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
            keys = self.events()
            if not self.paused:
                self.state.update(dt, keys)

            if self.state.done:
                self.flip_state()
            elif self.state.quit:
                self.running = False

            self.state.display(self.screen, dt)
            pygame.display.update()
