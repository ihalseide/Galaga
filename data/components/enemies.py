from . import centered_sprite
from .. import tools


ANIMATION_TIME = 0.75 # seconds per frame
DEATH_TIME = 0.2
# states
ASSEMBLING = "Assembling"
TO_FORMATION = "Going to formation"
FORMATION = "Formation"
DIVE_BOMB = "Dive bomb run"
TRACTOR_BEAM = "Tractor beam"
DYING = "Dying"

TIME_BT_POINTS = 0.7  # time between points in the paths

EXPLOSION = [
	tools.grab_sheet(8*16, 3*16, 16),
	tools.grab_sheet(9*16, 3*16, 16),
	tools.grab_sheet(10*16, 3*16, 16),
	tools.grab_sheet(11*16, 3*16, 32),
	tools.grab_sheet(13*16, 3*16, 32),
]


class Enemy(centered_sprite.CenteredSprite):
	pass


class Bee(Enemy):
	pass


class Butterfly(Enemy):
	pass


class Boss(Enemy):
	pass
