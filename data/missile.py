from data import tools
from data.galaga_sprite import GalagaSprite


class Missile(GalagaSprite):
    ENEMY_MISSILE = 246, 51, 3, 8
    PLAYER_MISSILE = 246, 67, 3, 8

    def __init__(self, x, y, vel, is_enemy):
        super(Missile, self).__init__(x, y, 2, 10)
        self.vel = vel
        self.is_enemy = is_enemy

        if self.is_enemy:
            img_slice = self.ENEMY_MISSILE
        else:
            img_slice = self.PLAYER_MISSILE
        ix, iy, w, h = img_slice
        self.image = tools.grab_sheet(ix, iy, w, h)

    def update(self, delta_time: int, flash_flag: bool):
        vel = self.vel * delta_time
        self.x += round(vel.x)
        self.y += round(vel.y)
