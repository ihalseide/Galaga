# sprites.py
# Author: Izak Halseide

from .tools import time_millis
import pygame
from . import constants as c, tools
from .constants import Rectangle
from .enemy_paths import EnemyPath
from .tools import grab_sheet


class GalagaSprite(pygame.sprite.Sprite):
    """
    Base class for a general sprite in Galaga.
    Useful for sprites that can flip their images, show/hide, and have their images offset from
    their centers, as well as having centered sprites.
    """

    def __init__(self, x, y, width, height, *groups: pygame.sprite.Group):
        super(GalagaSprite, self).__init__(groups)

        # Rectangle and position
        self.rect = pygame.Rect(0, 0, width, height)
        self.x = x
        self.y = y

        # Display and image variables
        self.image = None
        self.image_offset_x: int = 0
        self.image_offset_y: int = 0
        self.is_visible: bool = True
        self.flip_horizontal: bool = False
        self.flip_vertical: bool = False

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

    def update(self, delta_time: int, flash_flag: bool):
        pass

    def display(self, surface: pygame.Surface):
        if self.image is not None and self.is_visible:
            image = pygame.transform.flip(self.image, self.flip_horizontal, self.flip_vertical)
            img_width, img_height = image.get_size()
            # Center the image
            x = self.x - img_width // 2 + self.image_offset_x
            y = self.y - img_height // 2 + self.image_offset_y
            surface.blit(image, (x, y))


class Player(GalagaSprite):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 13, 12)
        self.image = grab_sheet(6 * 16, 0 * 16, 16, 16)
        self.image_offset_x = 1

    def update(self, delta_time, keys):
        s = round(c.PLAYER_SPEED * delta_time)
        if keys[pygame.K_RIGHT]:
            self.x += s
        elif keys[pygame.K_LEFT]:
            self.x -= s


class Enemy(GalagaSprite):

    def __init__(self, x, y, width, height, can_be_in_formation, formation_x=None, formation_y=None, path=None,
                 wave_number=None, number_in_wave=None, is_visible=False):
        super(Enemy, self).__init__(x, y, width, height)
        self.can_be_in_formation = can_be_in_formation
        self.is_in_formation = True#False
        self.formation_x = formation_x
        self.formation_y = formation_y
        self.wave_number = wave_number
        self.number_in_wave = number_in_wave
        self.path = path
        self.is_visible = is_visible

    def display(self, surface: pygame.Surface):
        super(Enemy, self).display(surface)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

    def update(self, delta_time: int, flash_flag: bool):
        if self.is_in_formation:
            self.go_to_formation()

    def go_to_formation(self):
        if self.formation_x is None or self.formation_y is None:
            return
        self.x, self.y = tools.calc_formation_pos_from_time(self.formation_x, self.formation_y, time_millis())


class Bee(Enemy):
    """
    Normal enemy
    """

    FRAMES = [Rectangle(128, 32, 16, 16), Rectangle(144, 32, 16, 16), Rectangle(160, 32, 16, 16),
              Rectangle(176, 32, 16, 16), Rectangle(192, 32, 16, 16), Rectangle(208, 32, 16, 16),
              Rectangle(224, 32, 16, 16), Rectangle(240, 32, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Bee, self).__init__(x, y, 16, 16,
                                  can_be_in_formation=True, formation_x=formation_x, formation_y=formation_y, path=path)
        self.image = grab_sheet(224, 32, 16, 16)
        self.frame_num = 7
        self.angle = 0
        self.is_visible = True

    def display(self, surface: pygame.Surface):
        x, y, w, h = self.FRAMES[self.frame_num]
        self.image = grab_sheet(x, y, w, h)
        super(Bee, self).display(surface)

    def update(self, delta_time: int, flash_flag: bool):
        x, y, angle = self.path.update(delta_time, self.x, self.y, self.angle)
        self.x, self.y, self.angle = x, y, angle

        if flash_flag:
            self.frame_num = 6
        else:
            self.frame_num = 7
        if self.path is not None:
            # Not using the angle right now
            self.x, self.y, _ = self.path.update(delta_time, self.x, self.y, self.angle)


class Butterfly(Enemy):
    """
    Normal enemy
    """

    FRAMES = [Rectangle(0, 32, 16, 16), Rectangle(16, 32, 16, 16), Rectangle(32, 32, 16, 16), Rectangle(48, 32, 16, 16),
              Rectangle(64, 32, 16, 16), Rectangle(80, 32, 16, 16), Rectangle(96, 32, 16, 16),
              Rectangle(112, 32, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Butterfly, self).__init__(x, y, 16, 16,
                                        can_be_in_formation=True,
                                        formation_x=formation_x, formation_y=formation_y, path=path)
        self.image = grab_sheet(224, 32, 16, 16)
        self.frame_num = 7

    def update(self, delta_time: int, flash_flag: bool):
        super(Butterfly, self).update(delta_time, flash_flag)
        if flash_flag:
            self.frame_num = 6
        else:
            self.frame_num = 7
        self.image = grab_sheet(*self.FRAMES[self.frame_num])


class Purple(Enemy):
    """
    The enemy that tries to capture the player's fighter
    """

    FRAMES = [Rectangle(224, 16, 16, 16), Rectangle(240, 16, 16, 16)]

    def __init__(self, x: int, y: int, formation_x: int, formation_y: int, path: EnemyPath = None):
        super(Purple, self).__init__(x, y, 16, 16,
                                     can_be_in_formation=True,
                                     formation_x=formation_x, formation_y=formation_y, path=path)
        self.image = grab_sheet(128, 16, 16, 16)
        self.frame_num = 0

    def update(self, delta_time: int, flash_flag: bool):
        super(Purple, self).update(delta_time, flash_flag)
        if flash_flag:
            self.frame_num = 0
        else:
            self.frame_num = 1
        rect = self.FRAMES[self.frame_num]
        self.image = grab_sheet(x=rect.x, y=rect.y, width=rect.width, height=rect.height)


class Trumpet(Enemy):
    """
    The enemy that spawns after a kill streak
    """

    def __init__(self, x: int, y: int, path: EnemyPath = None):
        super(Trumpet, self).__init__(x, y, 16, 16, can_be_in_formation=False, path=path, is_visible=True)
        self.image = grab_sheet(0, 64, 16, 16)


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
        self.image = grab_sheet(ix, iy, w, h)

    def update(self, delta_time: int, flash_flag: bool):
        vel = self.vel * delta_time
        self.x += round(vel.x)
        self.y += round(vel.y)


class Explosion(GalagaSprite):
    PLAYER_FRAME_DURATION = 140
    OTHER_FRAME_DURATION = 120

    PLAYER_FRAMES = [Rectangle(64, 112, 32, 32), Rectangle(96, 112, 32, 32), Rectangle(128, 112, 32, 32),
                     Rectangle(160, 112, 32, 32)]

    OTHER_FRAMES = [Rectangle(224, 80, 16, 16), Rectangle(240, 80, 16, 16), Rectangle(224, 96, 16, 16),
                    Rectangle(0, 112, 32, 32), Rectangle(32, 112, 32, 32)]

    def __init__(self, x: int, y: int, is_player_type=False):
        super(Explosion, self).__init__(x, y, 16, 16)
        self.is_player_type = is_player_type

        self.frame_timer = 0

        if self.is_player_type:
            self.image = grab_sheet(64, 112, 32, 32)
            self.frames = iter(self.PLAYER_FRAMES)
            self.frame_duration = self.PLAYER_FRAME_DURATION
        else:
            self.image = grab_sheet
            self.frames = iter(self.OTHER_FRAMES)
            self.frame_duration = self.OTHER_FRAME_DURATION

        self.frame = None
        self.next_frame()

    def next_frame(self):
        self.frame = next(self.frames)
        x, y, w, h = self.frame
        self.image = grab_sheet(x, y, w, h)
        self.frame_timer = 0

    def update(self, delta_time: int, flash_flag: bool):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            try:
                self.next_frame()
            except StopIteration:
                self.kill()
                return

    def display(self, surface: pygame.Surface):
        super(Explosion, self).display(surface)


def create_score_surface(number):
    sheet_y = 240
    char_width = 5
    char_height = 8
    sheet_char_width = 4

    number = int(number)
    str_num = str(number)
    length = len(str_num)

    # Create the surface to add to
    # noinspection PyArgumentList
    surface = pygame.Surface((char_width * length, char_height)).convert_alpha()

    # choose color based on the number
    color = None
    if number in (800, 1000):
        color = c.BLUE
    else:
        color = c.YELLOW

    # blit each individual char
    for i, character in enumerate(str_num):
        value = int(character)
        sheet_x = value * sheet_char_width
        number_sprite = grab_sheet(sheet_x, sheet_y, 4, 8)
        surface.blit(number_sprite, (i * char_width, 0))

    # replace white with color
    pixels = pygame.PixelArray(surface)
    pixels.replace((255, 255, 255), color)
    pixels.close()

    return surface


class ScoreText(GalagaSprite):
    # The class keeps track of the text sprites
    text_sprites = pygame.sprite.Group()

    def __init__(self, x, y, number, lifetime=950):
        super(ScoreText, self).__init__(x, y, 1, 1, self.text_sprites)  # BB size doesn't matter here
        self.number = number
        self.image = create_score_surface(self.number)
        self.lifetime = lifetime

    def update(self, delta_time: int, flash_flag: bool):
        # Wait to die
        if self.lifetime < 0:
            self.kill()
            return
        self.lifetime -= delta_time
