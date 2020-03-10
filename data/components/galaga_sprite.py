from typing import Optional

import pygame


class GalagaSprite(pygame.sprite.Sprite):

	def __init__(self, rect: pygame.Rect = None, image: pygame.Surface = None, *groups: pygame.sprite.Group):
		super(GalagaSprite, self).__init__(groups)
		self.rect: pygame.Rect = rect
		self.image: pygame.Surface = image
		self.image_offset_x: int = 0
		self.image_offset_y: int = 0
		self.is_visible: bool = True
		self.is_alive: bool = True

	@property
	def x(self):
		return self.rect.centerx

	@x.setter
	def x(self, value: int):
		self.rect.centerx = value

	@property
	def y(self):
		return self.rect.centery

	@y.setter
	def y(self, value: int):
		self.rect.centery = value

	def update(self, *args):
		if hasattr(self, 'x') and hasattr(self, 'y'):
			self.rect.center = self.x, self.y

	def display(self, surface: pygame.Surface):
		if self.image is not None and self.is_visible:
			img_width, img_height = self.image.get_size()
			x = self.x - img_width // 2 + self.image_offset_x
			y = self.y - img_height // 2 + self.image_offset_y
			surface.blit(self.image, (x, y))
