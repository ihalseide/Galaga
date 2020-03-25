import pygame

from .state import State


class Demo(State):
    # TODO: implement

    def update(self, delta_time: int, keys):
        pass

    def display(self, surface: pygame.Surface, delta_time: float):
        pass

    def get_event(self, event: pygame.event.Event):
        pass
