import pygame


class GalagaSprite(pygame.sprite.Sprite):
	"""
	Base class for a general sprite in Galaga.
	Useful for sprites that can flip and rotate by 90 deg. increments, show/hide, and have their images offset from
	their centers, as well as having centered sprites.
	"""

	def __init__(self, x, y, width, height, image: pygame.Surface = None, *groups: pygame.sprite.Group):
		super(GalagaSprite, self).__init__(groups)

		# rectangle
		self.rect = pygame.Rect(0, 0, width, height)
		self.rect.center = (x, y)

		# display and image variables
		self.image: pygame.Surface = image
		self.image_offset_x: int = 0
		self.image_offset_y: int = 0
		self.is_visible: bool = True
		self.is_alive: bool = True
		self.flip_horizontal: bool = False
		self.flip_vertical: bool = False
		self._image_rotation: int = 0

	@property
	def image_rotation(self) -> int:
		return self._image_rotation

	@image_rotation.setter
	def image_rotation(self, value: int):
		self._image_rotation = int(value) % 4

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

	def flash_update(self):
		pass

	def update(self, *args):
		if hasattr(self, 'x') and hasattr(self, 'y'):
			self.rect.center = self.x, self.y

	def display(self, surface: pygame.Surface):
		if self.image is not None and self.is_visible:
			image = pygame.transform.flip(self.image, self.flip_horizontal, self.flip_vertical)
			if self.image_rotation:
				image = pygame.transform.rotate(image, -90 * self.image_rotation)
			img_width, img_height = image.get_size()
			x = self.x - img_width // 2 + self.image_offset_x
			y = self.y - img_height // 2 + self.image_offset_y
			surface.blit(image, (x, y))
