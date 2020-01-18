import pygame

from . import centered_sprite
from .. import tools

PLAYER_SPEED = 350
ENEMY_SPEED = 300
ENEMY_TYPE = tools.grab_sheet(246, 51, 3, 8)
PLAYER_TYPE = tools.grab_sheet(246, 67, 3, 8)


class Missile(centered_sprite.CenteredSprite):
	def __init__(self, loc, vel, is_enemy):
		super(Missile, self).__init__()

		self.vel = vel
		self.is_enemy = is_enemy

		self.rect = pygame.Rect(0, 0, 2, 10)
		self.rect.center = loc

		if self.is_enemy:
			self.image = ENEMY_TYPE
		else:
			self.image = PLAYER_TYPE

	def update(self, dt, bounds):
		# TODO: move detecting bounds to the play_state class
		if self.is_enemy:
			vel = self.vel * ENEMY_SPEED * dt
		else:
			vel = self.vel * PLAYER_SPEED * dt

		self.rect.x += round(vel.x)
		self.rect.y += round(vel.y)

		if not bounds.contains(self.rect):
			self.kill()
