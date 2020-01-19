from data import tools
from data.components import centered_sprite


class _Enemy(centered_sprite.CenteredSprite):

	def __init__(self, x: int, y: int, formation_x: int, formation_y: int, can_be_in_formation: bool = True, *groups):
		super().__init__(*groups)
		self.x: int = x
		self.y: int = y
		self.formation_x: int = formation_x
		self.formation_y: int = formation_y
		self.can_be_in_formation = can_be_in_formation
		self.rotation = 0


class Bee(_Enemy):

	def __init__(self, x: int, y: int, formation_x: int, formation_y: int):
		super(Bee, self).__init__(x, y, formation_x, formation_y, can_be_in_formation=True)
		self.image = tools.grab_sheet(224, 32, 16)
		self.rect = tools.create_center_rect(self.x, self.y, 16, 16)


class Butterfly(_Enemy):

	def __init__(self, x: int, y: int, formation_x: int, formation_y: int):
		super(Butterfly, self).__init__(x, y, formation_x, formation_y, can_be_in_formation=True)
		self.image = tools.grab_sheet(96, 32, 16)
		self.rect = tools.create_center_rect(self.x, self.y, 16, 16)


# The enemy that tries to capture the player's fighter
class Boss(_Enemy):

	def __init__(self, x: int, y: int, formation_x: int, formation_y: int):
		super(Boss, self).__init__(x, y, formation_x, formation_y, can_be_in_formation=True)
		self.image = tools.grab_sheet(224, 16, 16)
		self.rect = tools.create_center_rect(self.x, self.y, 16, 16)


# The enemy that spawns after a kill streak
class TrumpetBug(_Enemy):
	
	def __init__(self, x: int, y: int):
		super(TrumpetBug, self).__init__(x, y, -1, -1, can_be_in_formation=False)
