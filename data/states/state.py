import pygame


class State(object):
	def __init__(self, persist=None):
		if persist is None:
			persist = dict()
		self.persist = persist
		self.next = None   # Next state
		self.done = False  # Ready to switch to next state
		self.quit = False  # Wants to quit the program

	def cleanup(self) -> dict:
		return self.persist

	def get_event(self, event: pygame.event.Event):
		pass

	def update(self, dt: float, keys):
		pass

	def display(self, surf: pygame.Surface, dt: float):
		pass
