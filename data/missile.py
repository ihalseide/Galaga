from data import tools, galaga_sprite

ENEMY_TYPE = tools.grab_sheet(246, 51, 3, 8)
PLAYER_TYPE = tools.grab_sheet(246, 67, 3, 8)


class Missile(galaga_sprite.GalagaSprite):
	def __init__(self, x, y, vel, is_enemy):
		super(Missile, self).__init__(x, y, 2, 10)
		self.vel = vel
		self.is_enemy = is_enemy

		if self.is_enemy:
			self.image = ENEMY_TYPE
		else:
			self.image = PLAYER_TYPE

	def update(self, dt):
		if self.is_enemy:
			vel = self.vel * dt
		else:
			vel = self.vel * dt
		self.x += round(vel.x)
		self.y += round(vel.y)
