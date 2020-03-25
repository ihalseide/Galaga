import pygame


class State(object):

    def __init__(self, persist=None):
        if persist is None:
            persist = dict()
        self.persist = persist
        self.next = None  # Next state
        self.done = False  # Ready to switch to next state
        self.quit = False  # Wants to quit the program

    def cleanup(self) -> dict:
        return self.persist

    def get_event(self, event: pygame.event.Event):
        raise NotImplementedError()

    def update(self, delta_time: int, keys):
        raise NotImplementedError()

    def display(self, surface: pygame.Surface, delta_time: float):
        raise NotImplementedError()
