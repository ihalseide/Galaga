from data import tools
from data.components import galaga_sprite

import pygame

FRAME_DURATION = 0.1 # milliseconds


class Explosion(galaga_sprite.GalagaSprite):

	def __init__(self, x: int, y: int):
		super(Explosion, self).__init__(rect=pygame.Rect(0, 0, 16, 16))
		self.x = x
		self.y = y
		self.frame = 0
		self.frame_timer = 0
		self.image = tools.grab_sheet(224, 80, 16, 16)

	def update(self, dt):
		if not self.is_alive:
			return
		self.frame_timer += dt
		if self.frame_timer >= FRAME_DURATION:
			self.frame += 1
			self.frame_timer = 0
		if self.frame == 1:
			self.image = tools.grab_sheet(240, 80, 16, 16)
		elif self.frame == 2:
			self.image = tools.grab_sheet(224, 96, 16, 16)
		elif self.frame == 3:
			self.image = tools.grab_sheet(0, 112, 32, 32)
		elif self.frame == 4:
			self.image = tools.grab_sheet(32, 112, 32, 32)
		elif self.frame != 0:
			self.is_alive = False
			self.kill()
			
	def display(self, surface: pygame.Surface):
		if not self.is_alive:
			return
		super(Explosion, self).display(surface)
