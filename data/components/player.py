import pygame

from . import centered_sprite
from .. import constants as c
from .. import tools

FIRE_COOLDOWN = 0.4
SPEED = 85


class Player(centered_sprite.CenteredSprite):
	def __init__(self):
		centered_sprite.CenteredSprite.__init__(self)
		self.rect = pygame.Rect(0, 0, 13, 12)
		self.rect.center = (c.GAME_WIDTH // 2, c.GAME_HEIGHT - self.rect.height // 2 - 25)
		self.image = tools.grab_sheet(6*16, 0*16, 16)
		self.last_fire_time = 0
		self.image_offset_x = 1

	def update(self, dt, keys):
		s = round(SPEED * dt)
		if keys[pygame.K_RIGHT]:
			self.rect.x += s
		elif keys[pygame.K_LEFT]:
			self.rect.x -= s

	def can_fire(self, time):
		return time - self.last_fire_time >= FIRE_COOLDOWN

	# def display(self, screen):
	# 	centered_sprite.CenteredSprite.display(self, screen)
	# 	pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
