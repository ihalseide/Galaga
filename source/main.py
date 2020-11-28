import pygame
from . import constants as c
from .states import GameOver, Demo, Play, Title, ScoreEntry, State


class Control(object):
    """
    Main class for running the game states and window
    """

    def __init__(self, state_dict: dict, initial_state_name: str, persist=None):
        # Init
        self.state_dict = state_dict
        self.state_name = initial_state_name

        self.clock = pygame.time.Clock()
        self.fps: int = c.FPS
        self.paused = False
        self.running = True
        self.screen: pygame.Surface = pygame.display.get_surface()
        state_class: State.__class__ = self.state_dict[self.state_name]
        self.state: State = state_class(persist=persist)

    def flip_state(self):
        persist = self.state.cleanup()
        self.state_name = self.state.next_state_name
        state_class = self.state_dict[self.state_name]
        self.state = state_class(persist)
        self.state.state_start_time = pygame.time.get_ticks()

    def poll_events(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                self.running = False
                self.state.cleanup()
                return
            self.state.get_event(event)
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys

    def main_loop(self):
        while self.running:
            # TODO: fix huge delta times when the window gets unfocused or something (if possible?)
            delta_time = self.clock.tick(self.fps)

            # Poll events and get the pressed keys from pygame
            pressed_keys = self.poll_events()
            if not self.running:
                break

            self.state.current_time = pygame.time.get_ticks()  # update the state's time for it
            self.state.update(delta_time, pressed_keys)

            if self.state.is_done:
                self.flip_state()
            elif self.state.is_quit:
                self.running = False

            self.state.display(self.screen)
            pygame.display.update()


def main():
    # This function begins the main game loop inside the CONTROL class
    initial_state = c.TITLE_STATE
    state_dict = {c.TITLE_STATE: Title,
                  c.PLAY_STATE: Play,
                  c.SCORE_ENTRY_STATE: ScoreEntry,
                  c.GAME_OVER_STATE: GameOver,
                  c.DEMO_STATE: Demo}
    # persist = c.Persist(stars=Stars(), scores=[], current_score=16000, one_up_score=0, high_score=100000, \
    # num_shots=132, num_hits=257)
    persist = None
    the_galaga = Control(state_dict=state_dict, initial_state_name=initial_state, persist=persist)
    the_galaga.main_loop()
