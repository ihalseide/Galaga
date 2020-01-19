from typing import Union

import pygame


class CenteredSprite(pygame.sprite.Sprite):
	def __init__(self, *groups):
		super(CenteredSprite, self).__init__(groups)
		self.rect: Union[pygame.Rect, None] = None
		self.image: Union[pygame.Surface, None] = None
		self.image_offset_x: int = 0
		self.image_offset_y: int = 0

	def display(self, surface: pygame.Surface):
		if self.image:
			img_width, img_height = self.image.get_size()
			x = self.rect.centerx - img_width // 2 + self.image_offset_x
			y = self.rect.centery - img_height // 2 + self.image_offset_y
			surface.blit(self.image, (x, y))
