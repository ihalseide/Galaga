import pygame

from .. import constants as c
from .. import tools


class Player(pygame.sprite.Sprite):
	fire_cooldown = 0.4
	speed = 85

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(0, 0, 15, 15)
		self.rect.center = (c.GAME_WIDTH // 2, c.GAME_HEIGHT - self.rect.height // 2 - 25)
		self.image = tools.grab_sheet(6*16, 0*16, 16)
		self.last_fire_time = 0

	def update(self, dt, keys):
		s = round(self.speed * dt)
		if keys[pygame.K_RIGHT]:
			self.rect.x += s
		elif keys[pygame.K_LEFT]:
			self.rect.x -= s

	def can_fire(self, time):
		return time - self.last_fire_time >= self.fire_cooldown

	def draw(self, screen):
		screen.blit(self.image, self.rect)
