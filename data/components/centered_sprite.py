import pygame


class CenteredSprite:
	def __init__(self):
		self.rect: pygame.Rect = None
		self.image: pygame.Surface = None
		self.image_offset_x: int = 0
		self.image_offset_y: int = 0

	def update(self, *args, **kwargs):
		pass

	def display(self, surface: pygame.Surface):
		if self.image:
			img_width, img_height = self.image.get_size()
			x = self.rect.centerx - img_width // 2 + self.image_offset_x
			y = self.rect.centery - img_height // 2 + self.image_offset_y
			surface.blit(self.image, (x, y))

	def kill(self):
		# TODO: implement, very important for performance!
		pass
