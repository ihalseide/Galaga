import sys, pygame, math, os, time, random
from collections import namedtuple
from pygame.math import Vector2
from collections import namedtuple
from dataclasses import dataclass
from math import sin
from string import ascii_lowercase
from functools import wraps

# Named tuples for convenient member access

# Class for persistent data shared between states
Persist = namedtuple("Persist", "stars scores current_score one_up_score high_score num_shots num_hits stage_num")

# Point tuple
Point = namedtuple("Point", "x y")

# Rectangle tuple
Rectangle = namedtuple("Rectangle", "x y width height")

# Area tuple
Area = namedtuple("Area", "width height")

StageBadges = namedtuple("StageBadges", "stage_1 stage_5 stage_10 stage_20 stage_30 stage_50")

# Game state keys
TITLE_STATE = 'title state'
PLAY_STATE = 'play state'
SCORE_ENTRY_STATE = 'score entry state'
GAME_OVER_STATE = 'game over state'
DEMO_STATE = 'demo state'

# String constants for in-game
TITLE = 'Galaga'  # title for the game window
TITLE_FOOTER_TEXT = 'GALAGA © 1981'  # shown at the bottom of the screen on the menu
START_TEXT = 'START'  # Start message in play state
HI_SCORE_MESSAGE = 'HI-SCORE'  # HUD high score label
ONE_UP = '1UP'  # HUD 1up label
ONE_UP_NUM_FORMAT = '{: =6}'  # number format string for 1up score
HI_SCORE_NUM_FORMAT = '{: =6}'  # number format string for high score
STAGE_FORMAT_STR = 'STAGE {: =3}'  # number format string for the stage number
READY = 'READY'  # ready message in play state
GAME_OVER_TEXT = 'GAME OVER'

# Sting messages for game over
RESULT_TEXT = "- Result -"  # text is red
SHOTS_FIRED_TEXT = 'Shots fired {: >12}'  # text is light blue
NUM_HITS_TEXT = 'Number of hits {: >9}'  # text is white
HIT_MISS_RATIO = 'Hit-miss ratio {: >10.1%}'  # text is yellow

# Resources and other file paths
RESOURCE_DIR = "resources"
SCORE_FILE = "scores.txt"

# Game space
GAME_SIZE = Area(224, 288)
GAME_CENTER = Point(GAME_SIZE.width // 2, GAME_SIZE.height // 2)
DEFAULT_SCREEN_SIZE = GAME_SIZE
STAGE_TOP_Y = 30  # Y-coord. for the top of the stage
STAGE_BOTTOM_Y = GAME_SIZE.height - 20  # Y-coord. for the bottom of the stage
BADGE_Y = GAME_SIZE.height - 19  # Y-coord for the top of the stage badges

# Timing and frequencies:
FPS = 30  # Frames per second
ENEMY_ANIMATION_FREQ = 800  # milliseconds
TEXT_FLASH_FREQ = 300  # "

# Scoring
NUM_TRACKED_SCORES = 5

# Used colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
LIGHT_GREEN = (144, 238, 144)

# Player
PLAYER_FIRE_COOLDOWN = 400
PLAYER_SPEED = 0.085

# Stage enemies formation
FORMATION_OFFSET_Y = 20
FORMATION_MIN_SPREAD = 4
FORMATION_MAX_SPREAD = 8
FORMATION_MAX_X = 16
FORMATION_CYCLE_TIME = 8000 # millis

# Play state timings
STAGE_DURATION = 1600
READY_DURATION = 1600
INTRO_MUSIC_DURATION = 6600
START_NOISE_WAIT = 0
START_DURATION = START_NOISE_WAIT + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 200
FIRE_COOLDOWN = 200
GAME_OVER_DURATION = 3000

# game area boundary
STAGE_BOUNDS = pygame.Rect(0, c.STAGE_TOP_Y, c.GAME_SIZE.width, c.STAGE_BOTTOM_Y - c.STAGE_TOP_Y)

# For displaying the text in the middle for the play state
LINE_TEXT_HEIGHT = 16

# Title settings
LIGHT_TITLE = setup.get_image('light_title')
GREEN_TITLE = setup.get_image('green_title')
WHITE_TITLE = setup.get_image('white_title')
SCORE_Y = 10
TITLE_X = c.GAME_CENTER.x - LIGHT_TITLE.get_rect().width // 2
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60
MENU_SPEED = 3
TITLE_FLASH_TIME = 150  # millis.
TITLE_FLASH_NUM = 12

# How many milliseconds to show the game over screen
GAME_OVER_STATE_DURATION = 14500
#!/usr/bin/env python3


if __name__ == '__main__':
    main.main()
    pygame.quit()
    sys.exit()

# font spritesheet coordinates and stuff
FONT_ALPHABET_Y = 224
FONT_CHAR_SIZE = 8

# Pygame key constants
START_KEYS = [pygame.K_SPACE, pygame.K_RETURN]

# Setup pygame
SCREEN = FONT = SOUNDS = GRAPHICS = None


def setup_game():
    global SCREEN, FONT, SOUNDS, GRAPHICS

    # Center the window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    SCREEN = pygame.display.set_mode(c.DEFAULT_SCREEN_SIZE)
    pygame.display.set_caption(c.TITLE)

    # Load these
    FONT = load_font()
    SOUNDS = load_all_sfx(os.path.join(c.RESOURCE_DIR, "audio"), (".ogg",))
    GRAPHICS = load_all_gfx(os.path.join(c.RESOURCE_DIR, "graphics"), ('.png', ".bmp"))


def load_all_gfx(directory, accept=('.png', '.bmp', '.gif'), color_key=pygame.Color('black')) -> dict:
    graphics = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, filename))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color_key)
            graphics[name] = img
    return graphics


def load_all_sfx(directory, accept=(".ogg", ".wav")) -> dict:
    accept_all = len(accept) == 0
    effects = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if accept_all or ext.lower() in accept:
            effects[name] = pygame.mixer.Sound(os.path.join(directory, filename))
    return effects


def load_font() -> dict:
    """
    Create the coordinate map for the font image
    """
    row_2_y = FONT_ALPHABET_Y + FONT_CHAR_SIZE
    font = dict()
    # add alphabet
    for i, char in enumerate(ascii_lowercase):
        font[char] = (i * FONT_CHAR_SIZE, FONT_ALPHABET_Y)
    # add digits
    for i in range(10):
        font[str(i)] = (i * FONT_CHAR_SIZE, row_2_y)
    font['-'] = (10 * FONT_CHAR_SIZE, row_2_y)
    font[' '] = (11 * FONT_CHAR_SIZE, row_2_y)
    font[None] = (12 * FONT_CHAR_SIZE, row_2_y)
    font[':'] = (13 * FONT_CHAR_SIZE, row_2_y)
    font['!'] = (14 * FONT_CHAR_SIZE, row_2_y)
    font[','] = (15 * FONT_CHAR_SIZE, row_2_y)
    font['©'] = (16 * FONT_CHAR_SIZE, row_2_y)
    font['.'] = (17 * FONT_CHAR_SIZE, row_2_y)
    font['%'] = (18 * FONT_CHAR_SIZE, row_2_y)
    return font


def get_sfx(sound_name: str) -> pygame.mixer.Sound:
    return SOUNDS.get(sound_name)


def has_sfx(sound_name: str) -> bool:
    return get_sfx(sound_name) is not None


def get_image(image_name: str) -> pygame.Surface:
    return GRAPHICS.get(image_name)


def has_image(image_name: str) -> bool:
    return get_image(image_name) is not None


def get_from_font(character) -> tuple:
    return FONT.get(character)


def has_char_in_font(character: str) -> bool:
    return get_from_font(character) is not None


def play_sound(sound_name):
    SOUNDS.get(sound_name).play()


def stop_sounds():
    pygame.mixer.stop()


# load all the resources
setup_game()

def linear_interpolation(start: float, stop: float, percent: float) -> float:
    """
    Linear interpolation function
    :param start: starting value for interpolation
    :param stop: ending value for interpolation
    :param percent: proportion of the way through interpolation (0.0 -> 1.0)
    :return: the interpolated value
    """
    return (1 - percent) * start + percent * stop

def map_value(value, in_start, in_stop, out_start, out_stop):
    """
    Map a value from an input range to an output range
    :param value:
    :param in_start:
    :param in_stop:
    :param out_start:
    :param out_stop:
    :return:
    """
    return out_start + (out_stop - out_start) * ((value - in_start) / (in_stop - in_start))

def _font_render(text: str, color: pygame.Color, bg_color=None):
    """
    Create a pygame image with the text rendered on it using the custom bitmap font
    :param text:
    :param color:
    :param bg_color:
    :return:
    """
    surf = pygame.Surface((len(text) * setup.FONT_CHAR_SIZE, setup.FONT_CHAR_SIZE))
    if bg_color is None:
        surf.set_colorkey(pygame.Color('black'))
    for i, char in enumerate(text):
        # get font location for the char, default to unknown symbol
        font_data = setup.get_from_font(char.lower())
        if not font_data:
            font_data = setup.get_from_font(None)
        # grab the image at location
        glyph = grab_sheet(font_data[0], font_data[1], setup.FONT_CHAR_SIZE, setup.FONT_CHAR_SIZE)
        surf.blit(glyph, (i * setup.FONT_CHAR_SIZE, 0), )
    # replace colors
    pixels = pygame.PixelArray(surf)
    if bg_color:
        pixels.replace(pygame.Color('black'), bg_color)
    pixels.replace(pygame.Color('white'), color)
    pixels.close()
    return surf

def draw_text(surface, text, position, color, background_color=None, center_x=False, center_y=False):
    text_surface = _font_render(str(text), color, background_color)
    x, y = position
    width, height = text_surface.get_size()
    if center_x:
        x -= width // 2
    if center_y:
        y -= height // 2
    if surface is None:
        return text_surface
    else:
        return surface.blit(text_surface, (x, y))

def grab_sheet(x: int, y: int, width: int, height: int) -> pygame.Surface:
    """
    Get a pixel rectangle from an the spritesheet resource
    """
    return setup.get_image('sheet').subsurface((x, y, width, height))

def create_center_rect(x: int, y: int, width: int, height: int) -> pygame.Rect:
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (x, y)
    return rect

def distance(x1: float, y1: float, x2: float, y2: float):
    """
    Return distance between two 2D points.
    """
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)

def angle_between(x1: float, y1: float, x2: float, y2: float):
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)

def close_to_2d(x1, y1, x2, y2, max_distance=0.001):
    """
    Give whether two points in 2d space are "close enough"
    """
    return distance(x1, y1, x2, y2) <= max_distance

def snap_angle(angle) -> int:
    """
    Return the nearest discrete 8-value angle to a continuous radian angle
    :param angle: input angle in radians
    :return:
    """
    # TODO: implement
    return angle // 8

def clamp_value(n, minimum, maximum):
    """
    Clamp a value between a min and max
    :param n:
    :param minimum:
    :param maximum:
    :return:
    """
    return max(minimum, min(n, maximum))

def range_2d(start_x, start_y, end_x, end_y):
    """
    A range across 2D indices in x and y
    :param start_x:
    :param start_y:
    :param end_x: exclusive
    :param end_y: exclusive
    :return:
    """
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            yield x, y

def irange_2d(start_x, start_y, end_x, end_y):
    """
    Be inclusive with the end_x and end_y
    :param start_x:
    :param start_y:
    :param end_x: inclusive
    :param end_y: inclusive
    :return:
    """
    for x, y in range_2d(start_x, start_y, end_x + 1, end_y + 1):
        yield x, y

def arc_length(start_angle, end_angle, radius):
    """
    Takes angles in radians
    :param start_angle:
    :param end_angle:
    :param radius:
    :return:
    """
    theta = abs(end_angle - start_angle)
    return theta * radius

def calc_stage_badges(stage_num):
    """
    Calculate how many of each stage badges there are for a given stage
    """
    assert stage_num in range(256)

    w_stage = stage_num  # temp. var

    num_50 = w_stage // 50
    w_stage -= num_50 * 50
    num_30 = w_stage // 30
    w_stage -= num_30 * 30
    num_20 = w_stage // 20
    w_stage -= num_20 * 20
    num_10 = w_stage // 10
    w_stage -= num_10 * 10
    num_5 = w_stage // 5
    num_1 = w_stage - num_5 * 5

    return c.StageBadges(num_1, num_5, num_10, num_20, num_30, num_50)

def update_wrapper_ms(func, argument_name="delta_time"):
    """
    Wrapper to make a function keep track of the time elapsed since it's last call.
    Time is tracked in milliseconds
    """
    last_call_time = None

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        nonlocal last_call_time

        now = time.perf_counter_ns()
        if last_call_time is None:
            elapsed = 0
        else:
            elapsed = now - last_call_time
        last_call_time = now
        elapsed_millis = elapsed // 1_000_000

        kwargs[argument_name] = elapsed_millis
        return func(*args, **kwargs)

    return func_wrapper

def calc_formation(time):
    # Time should be in millis

    mod_time = time % c.FORMATION_CYCLE_TIME
    norm_time = 2 * math.pi * mod_time / c.FORMATION_CYCLE_TIME

    middle_spread = (c.FORMATION_MAX_SPREAD + c.FORMATION_MIN_SPREAD) / 2
    spread_magnitude = c.FORMATION_MAX_SPREAD - c.FORMATION_MIN_SPREAD
    offset = sin(norm_time) * spread_magnitude
    spread = round(middle_spread + offset)

    center_x = 0 #c.GAME_CENTER.x
    offset = sin(2 * norm_time) * c.FORMATION_MAX_X
    x = round(center_x + offset)

    return spread, x, c.FORMATION_OFFSET_Y

def calc_formation_pos_from_time(formation_x, formation_y, time):
    spread, x_offset, y_offset = calc_formation(time)
    return calc_formation_pos(formation_x, formation_y, spread, x_offset, y_offset)

def calc_formation_pos(formation_x, formation_y, formation_spread, formation_x_offset, formation_y_offset):
    x = formation_x_offset + formation_x * (16 + formation_spread)
    y = formation_y_offset + formation_y * (16 + formation_spread)
    return x, y

def time_millis():
    return time.perf_counter_ns() // 1_000_000

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

NUM_OF_RANDOM_STARS = 64

StarLayer = namedtuple("StarLayer", "speed colors")


@dataclass
class TwinklingPhase:
    on_time: int
    off_time: int
    current_time: int = 0
    is_shown: bool = True


LAYERS = StarLayer(0.050, (c.RED, c.LIGHT_GREEN)), \
         StarLayer(0.075, (c.YELLOW, c.BLUE, c.WHITE))

TWINKLING_PHASES = TwinklingPhase(150, 140), TwinklingPhase(210, 200), TwinklingPhase(310, 300), \
                   TwinklingPhase(410, 300), TwinklingPhase(510, 300)


@dataclass
class Star:
    """
    A star particle, that has color, moves, and takes up a single pixel
    """
    start_x: int
    start_y: float
    color: tuple
    layer_num: int
    twinkle_phase: int
    speed: float
    show: bool = True


def random_star() -> Star:
    x = random.randint(0, c.GAME_SIZE.width)
    y = random.randint(0, c.GAME_SIZE.height)
    layer = random.randint(0, len(LAYERS) - 1)
    color = random.choice(LAYERS[layer].colors)
    phase = random.randint(0, len(TWINKLING_PHASES) - 1)
    return Star(x, y, color, layer, phase, speed=LAYERS[layer].speed)


class StarField:
    """
    Aesthetic stars for the background
    """

    def __init__(self):
        self._moving: int = 1
        self.stars = [random_star() for _ in range(NUM_OF_RANDOM_STARS)]
        self.twinkling_timers = [phase for phase in TWINKLING_PHASES]
        self.current_time = 0

    @property
    def moving(self) -> int:
        return self._moving

    @moving.setter
    def moving(self, direction: int):
        if direction < 0:
            self._moving = -1
        elif direction > 0:
            self._moving = 1
        else:
            self._moving = 0

    def update(self, delta_time: int):
        self.current_time += delta_time
        # update each timer
        for timer in self.twinkling_timers:
            timer.current_time += delta_time
            if timer.is_shown and timer.current_time >= timer.on_time:
                timer.current_time = 0
                timer.is_shown = False
            elif not timer.is_shown and timer.current_time >= timer.off_time:
                timer.current_time = 0
                timer.is_shown = True

    def display(self, screen):
        for star in self.stars:
            is_shown = self.twinkling_timers[star.twinkle_phase].is_shown
            if is_shown:
                y = round((star.start_y + (star.speed * self.current_time * self._moving)) % c.GAME_SIZE.height)
                screen.set_at((star.start_x, y), star.color)
def draw_mid_text(screen, text, color, line=1):
    x, y = c.GAME_CENTER.x, c.GAME_CENTER.y + LINE_TEXT_HEIGHT * (line - 1)
    tools.draw_text(screen, text, (x, y), color, center_y=True, center_x=True)

def play_init (persist):
    # Setup stars
    stars.moving = False

    # Score
    score = 0

    # init player
    is_player_alive = False
    player = None
    extra_lives = 3
    can_control_player = False
    last_fire_time = 0
    num_shots = 0
    num_hits = 0

    # init stage number and badge icons
    stage_num = 0
    num_badges = 0
    stage_badges = tools.calc_stage_badges(stage_num)
    is_animating_stage_badges = False
    stage_badge_animation_step = 0
    stage_badge_animation_timer = 0

    # missile sprites and such
    missiles = pygame.sprite.Group()
    enemy_missiles = pygame.sprite.Group()

    # Explosions sprites
    explosions = pygame.sprite.Group()

    # enemies and level
    formation_spread: int = 0
    formation_x_offset: int = 0
    formation_y_offset = c.STAGE_TOP_Y + 16
    the_stage: stages.Stage = stages.load_stage(1)  # pre-load stage 1
    enemies: pygame.sprite.Group = pygame.sprite.Group()
    enemies.add(the_stage.enemies)

    # timers:
    blocking_timer = 0  # this timer is for timing how long to show messages on screen
    flashing_text_timer = 0
    animation_beat_timer = 0
    animation_flag = False
    is_flashing_text = False
    show_1up_text = True

    # state
    is_starting = True
    has_started_intro_music = False
    should_show_ready = False
    should_show_stage = False
    should_spawn_enemies = False
    is_done_spawning_enemies = False
    is_ready = False
    should_reform_enemies = False
    should_show_game_over = False

def play_get_event(event):
    if event.type == pygame.KEYDOWN:
        keypress = event.key
        if keypress == pygame.K_SPACE and is_player_alive and can_control_player:
            if current_time >= (last_fire_time + FIRE_COOLDOWN):
                fighter_shoots()
                last_fire_time = current_time

        elif keypress == pygame.K_ESCAPE:
            # TODO: (DEBUG) skip things when [ESC] is pressed
            if not is_ready:
                done_starting()
                done_with_ready()
                done_showing_stage()
                stop_sounds()

        elif keypress == pygame.K_r:
            # TODO: (DEBUG) reset the state when [R] is pressed
            __init__(persist)

        elif keypress == pygame.K_k:
            # TODO: (DEBUG) kill the player when [K] is pressed
            kill_player()

def fighter_shoots ():
    play_sound('fighter_fire')
    # v is multiplied by speed in the missile class
    v = Vector2(0, -0.350)
    x = player.rect.centerx
    y = player.rect.top + 10
    m = sprites.Missile(x, y, v, is_enemy=False)
    missiles.add(m)
    num_shots += 1

def play_intro_music(:
    # Make the game play the intro music and wait
    stop_sounds()
    setup.get_sfx("theme").play()
    has_started_intro_music = True

def animate_stage_badges( delta_time):
    if not is_animating_stage_badges:
        return

    if stage_badge_animation_step > num_badges:
        is_animating_stage_badges = False

    stage_badge_animation_timer += delta_time

    if (stage_badge_animation_timer >= STAGE_BADGE_DURATION) and (
            stage_badge_animation_step < num_badges):
        stage_badge_animation_step += 1
        stage_badge_animation_timer = 0
        play_sound('stage_award')

def update( delta_time, keys):
    # More important things to update
    update_timers(delta_time)
    update_player(delta_time, keys)
    update_enemies(delta_time)

    # Less important graphical things to update
    update_text_sprites(delta_time)
    update_explosions(delta_time)
    update_stars(delta_time)
    animate_stage_badges(delta_time)
    update_missiles(delta_time)

def update_enemies( delta_time):
    # update enemies
    if the_stage and enemies:
        enemies.update(delta_time, animation_flag)

def add_explosion( x, y, is_player_type=False):
    explosions.add(sprites.Explosion(x, y, is_player_type=is_player_type))

def update_missiles( delta_time):
    for a_missile in missiles.sprites():
        a_missile.update(delta_time, animation_flag)

        # Only work on the first enemy hit
        for enemy in enemies:
            if not enemy.is_visible:
                continue
            if enemy.rect.colliderect(a_missile.rect):
                enemy.kill()
                a_missile.kill()
                num_hits += 1
                add_explosion(enemy.x, enemy.y)
                play_sound("enemy_hit_1")
                points = 0
                if isinstance(enemy, sprites.Bee):
                    points = 400
                elif isinstance(enemy, sprites.Butterfly):
                    points = 400
                elif isinstance(enemy, sprites.Purple):
                    points = 800
                    sprites.ScoreText(enemy.x, enemy.y, points)
                score += points
                high_score = max(score, high_score)
                if not STAGE_BOUNDS.contains(a_missile.rect):
                    a_missile.kill()
                break

def kill_player(:
    if player is None or not is_player_alive:
        return
    play_sound("explosion")
    is_player_alive = False
    player.kill()
    add_explosion(player.x, player.y, is_player_type=True)
    reform_enemies()

def reform_enemies(:
    is_ready = False
    should_reform_enemies = True
    # TODO: fix
    done_reforming_enemies()

def done_reforming_enemies(:
    should_show_ready = True
    should_reform_enemies = False
    spawn_player()

def decrement_lives(:
    extra_lives -= 1

def update_timers( delta_time: float):
    # the "blocking" timer that blocks stuff
    if is_starting:
        blocking_timer += delta_time
        if not has_started_intro_music:
            if blocking_timer >= START_NOISE_WAIT:
                play_intro_music()
        if blocking_timer >= START_DURATION:
            done_starting()
    elif should_show_stage:
        blocking_timer += delta_time
        if blocking_timer >= STAGE_DURATION:
            done_showing_stage()
            show_ready()
    elif should_show_ready:
        blocking_timer += delta_time
        if blocking_timer >= READY_DURATION:
            done_with_ready()
    elif should_show_game_over:
        blocking_timer += delta_time
        if blocking_timer >= GAME_OVER_DURATION:
            done_showing_game_over()

    # The separate timer for synchronized animation of some things
    animation_beat_timer += delta_time
    if animation_beat_timer >= c.ENEMY_ANIMATION_FREQ:
        animation_beat_timer = 0
        animation_flag = not animation_flag

    # The separate timer for flashing the 1UP text
    if is_flashing_text:
        flashing_text_timer += delta_time
        if flashing_text_timer >= c.TEXT_FLASH_FREQ:
            flashing_text_timer = 0
            show_1up_text = not show_1up_text

def show_ready(:
    should_show_ready = True
    persist.stars.moving = 1

def done_showing_stage(:
    should_show_stage = False
    blocking_timer = 0

def done_with_ready(:
    should_show_ready = False
    can_control_player = True
    blocking_timer = 0
    is_ready = True

def done_starting(:
    is_starting = False
    blocking_timer = 0
    spawn_player()
    stage_num = 0
    next_stage()
    should_show_stage = True
    is_flashing_text = True

def next_stage(:
    stage_num += 1

    # This check is made because stage #1 is pre-loaded:
    if not the_stage.stage_num == stage_num:
        the_stage = stages.load_stage(stage_num)
        enemies.add(the_stage.enemies)

    update_stage_badges()
    start_animating_stage_badges()

def start_animating_stage_badges(:
    is_animating_stage_badges = True
    stage_badge_animation_step = 0

def update_stage_badges(:
    stage_badges = tools.calc_stage_badges(stage_num)
    num_badges = sum(stage_badges)

def spawn_player(:
    if extra_lives == 0:
        show_game_over()
        return
    decrement_lives()
    is_player_alive = True
    player = sprites.Player(x=c.GAME_SIZE.width // 2, y=c.STAGE_BOTTOM_Y - 16)

def show_game_over(:
    should_show_game_over = True

def done_showing_game_over(:
    should_show_game_over = False
    is_done = True
    next_state_name = c.GAME_OVER_STATE

def display( screen: pygame.Surface):
    # clear screen
    screen.fill(c.BLACK)
    # stars
    persist.stars.display(screen)
    if the_stage:
        # draw enemies
        for enemy in enemies:
            enemy.display(screen)
    # draw player
    if is_player_alive:
        player.display(screen)
    # draw bullets
    for m in missiles:
        m.display(screen)
    # draw explosions
    for x in explosions:
        x.display(screen)
    # display text sprites
    for ts in sprites.ScoreText.text_sprites:
        ts.display(screen)
    # draw HUD
    show_state(screen)
    hud.display(screen, one_up_score=persist.one_up_score, high_score=persist.high_score,
                offset_y=0, num_extra_lives=extra_lives, stage_badges=stage_badges,
                stage_badge_animation_step=stage_badge_animation_step, show_1up=show_1up_text)

def show_state( screen):
    if is_starting:
        draw_mid_text(screen, c.START_TEXT, c.RED)
    elif should_show_stage:
        # pad the number to 3 digits
        draw_mid_text(screen, c.STAGE_FORMAT_STR.format(stage_num), c.LIGHT_BLUE)
    elif should_show_ready:
        draw_mid_text(screen, c.READY, c.RED)
    elif should_show_game_over:
        draw_mid_text(screen, c.GAME_OVER_TEXT, c.RED)

def update_player( dt, keys):
    if player and is_player_alive:
        if can_control_player:
            player.update(dt, keys)

        if player.rect.left < STAGE_BOUNDS.left:
            player.rect.left = STAGE_BOUNDS.left
        elif player.rect.right > STAGE_BOUNDS.right:
            player.rect.right = STAGE_BOUNDS.right

def update_text_sprites( delta_time):
    # update score text things
    sprites.ScoreText.text_sprites.update(delta_time, animation_flag)

def update_stars( delta_time):
    persist.stars.update(delta_time)

def update_explosions( delta_time):
    explosions.update(delta_time, animation_flag)


class Title:
def __init__( persist):
    # initialize the persistent data because it is the initial state
    if persist is None:
        scores = scoring.load_scores()
        high_score = max(scores, key=lambda record: record.score).score
        persist = c.Persist(stars=StarField(),
                            scores=scores,
                            current_score=0,
                            one_up_score=0,
                            high_score=high_score,
                            num_shots=0,
                            num_hits=0,
                            stage_num=0)
    State.__init__( persist)

    # whether it is in a scrolling state
    is_scrolling = True
    timer = 0

    # times the title has flashed
    flash_num = 0
    is_flashing = False
    is_title_white = False
    ready = False

    # scrolling menu up
    offset_y = c.GAME_SIZE.height

def set_ready(:
    ready = True
    offset_y = 0
    is_flashing = True
    flash_num = 0

def get_event( event):
    if event.type == pygame.KEYDOWN:
        if event.key in setup.START_KEYS:
            if ready:
                # start the game
                next_state_name = c.PLAY_STATE
                is_done = True
            else:
                set_ready()

def update( delta_time, keys):
    # stars
    persist.stars.update(delta_time)
    # scroll menu
    if ready:
        # flash timer
        is_flashing = flash_num < TITLE_FLASH_NUM * 2
        if is_flashing:
            timer += delta_time
            if timer >= TITLE_FLASH_TIME:
                timer = 0
                flash_num += 1
                is_title_white = not is_title_white
        else:
            pass  # TODO: make it flash later or invoke demo?
    elif offset_y > 0:
        offset_y -= MENU_SPEED
        if offset_y <= 0:
            set_ready()

def display( screen):
    # draw background
    screen.fill(c.BLACK)
    persist.stars.display(screen)
    # title normal
    if not is_flashing:
        surf = LIGHT_TITLE
    elif is_title_white:
        surf = WHITE_TITLE
    else:
        surf = GREEN_TITLE
    screen.blit(surf, (TITLE_X, TITLE_Y + offset_y))
    # draw 1up and high score hud
    hud.display(screen, one_up_score=0, high_score=0, offset_y=offset_y)
    # draw start text
    tools.draw_text(screen, c.START_TEXT, (c.GAME_CENTER.x, offset_y + START_Y), c.WHITE, center_x=True)
    # draw footer on bottom
    tools.draw_text(screen, c.TITLE_FOOTER_TEXT, (c.GAME_CENTER.x, offset_y + COPY_Y), c.WHITE, center_x=True)




def play_over_init ():
    play_sound("game_over")
    start_time = pygame.time.get_ticks()

    persist.stars.moving = 1

    stage_badges = calc_stage_badges(persist.stage_num)

    # Just render the surface once
    if num_shots == 0:
        ratio = 0
    else:
        ratio = num_hits / num_shots

def play_over_update (delta_time: int, keys: list):
    persist.stars.update(delta_time)
    if current_time > start_time + GAME_OVER_STATE_DURATION:
        is_done = True
        next_state_name = c.TITLE_STATE
        stop_sounds()

def play_over_display (screen: pygame.Surface):
    screen.fill(c.BLACK)
    persist.stars.display(screen)

    x, y = c.GAME_CENTER.x, 100

    draw_text(surface=screen, text=c.RESULT_TEXT,
              position=(x, y), color=c.RED, center_x=True)

    x = c.GAME_CENTER.x - 100
    draw_text(surface=screen, text=c.SHOTS_FIRED_TEXT.format(persist.num_shots),
              position=(x, y + 16), color=c.LIGHT_BLUE)

    draw_text(surface=screen, text=c.NUM_HITS_TEXT.format(persist.num_hits),
              position=(x, y + 32), color=c.WHITE)

    draw_text(surface=screen, text=c.HIT_MISS_RATIO.format(ratio),
              position=(x, y + 48), color=c.YELLOW)

    hud.display(screen, one_up_score=persist.one_up_score, high_score=persist.high_score,
                stage_badges=stage_badges, stage_badge_animation_step=sum(stage_badges))

GuiTuple = namedtuple("GuiTuple", "life stage_1 stage_5 stage_10 stage_20 stage_30 stage_50")

BLINK_1UP = 450  # milliseconds

# sprite resources for HUD
ICONS = GuiTuple(grab_sheet(96, 0, 16, 16), grab_sheet(208, 48, 7, 16), grab_sheet(192, 48, 7, 16),
                 grab_sheet(176, 48, 14, 16), grab_sheet(160, 48, 15, 16), grab_sheet(144, 48, 16, 16),
                 grab_sheet(128, 48, 16, 16))


def draw_lives(screen, num_extra_lives):
    # lives
    for i in range(num_extra_lives):
        screen.blit(ICONS.life, (3 + i * 16, c.STAGE_BOTTOM_Y + 1, 16, 16))


def draw_stage_badges(screen, stage_badges, stage_badge_animation_step):
    # draw the stage level badges
    draw_x = c.GAME_SIZE.width
    h = c.BADGE_Y
    number_to_draw = stage_badge_animation_step

    for n in range(stage_badges.stage_1):
        if number_to_draw > 0:
            draw_x -= 8
            screen.blit(ICONS.stage_1, (draw_x, h, 7, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_5):
        if number_to_draw > 0:
            draw_x -= 8
            screen.blit(ICONS.stage_5, (draw_x, h, 7, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_10):
        if number_to_draw > 0:
            draw_x -= 14
            screen.blit(ICONS.stage_10, (draw_x, h, 14, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_20):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_20, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_30):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_30, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return

    for n in range(stage_badges.stage_50):
        if number_to_draw > 0:
            draw_x -= 16
            screen.blit(ICONS.stage_50, (draw_x, h, 16, 16))
            number_to_draw -= 1
        else:
            return


def display(screen: pygame.Surface, one_up_score: int, high_score: int, offset_y: int = 0, num_extra_lives=0,
            stage_badges=None, stage_badge_animation_step=None, show_1up=True):
    # clear the top and bottom for the hud when in play state
    screen.fill(pygame.Color('black'), (0, 0, c.GAME_SIZE.width, c.STAGE_TOP_Y))
    screen.fill(pygame.Color('black'), (0, c.STAGE_BOTTOM_Y, c.GAME_SIZE.width,
                                        c.GAME_SIZE.height - c.STAGE_BOTTOM_Y))

    # 1UP score
    if show_1up:
        draw_text(screen, c.ONE_UP, Point(20, 10 + offset_y), c.RED)
    score_string = c.HI_SCORE_NUM_FORMAT.format(one_up_score)
    draw_text(screen, score_string, Point(20, 20 + offset_y), c.WHITE)

    # high score
    high_score_string = c.HI_SCORE_NUM_FORMAT.format(high_score)
    draw_text(screen, c.HI_SCORE_MESSAGE, Point(c.GAME_CENTER.x, 10 + offset_y), c.RED, center_x=True)
    draw_text(screen, high_score_string, Point(83, 20 + offset_y), c.WHITE)

    if num_extra_lives:
        draw_lives(screen, num_extra_lives=num_extra_lives)

    if stage_badges is not None:
        draw_stage_badges(screen, stage_badges, stage_badge_animation_step)

ScoreRecord = namedtuple('Score', 'name score')

NUM_TRACKED_SCORES = c.NUM_TRACKED_SCORES


def load_scores() -> list:
    scores = []
    with open(c.SCORE_FILE) as file:
        # Read a max of NUM_TRACKED_SCORES lines
        for line, _ in zip(file, range(NUM_TRACKED_SCORES)):
            try:
                name, score = line.split(' ')
                name = name[:3]  # Limit name length to 3
                score = int(score)  # The score is an int.
                record = ScoreRecord(name, score)
                scores.append(record)
            except ValueError as e:
                print("[Warning]: ValueError caught in loading scores -", e)
    if not scores:
        return [ScoreRecord('AAA', 30_000),
                ScoreRecord('BBB', 20_000),
                ScoreRecord('CCC', 10_000),
                ScoreRecord('DDD', 9_000),
                ScoreRecord('EEE', 8_000)]
    return scores


def save_scores(scores):
    sorted_scores = sorted(scores)
    lines = ["{} {}".format(record.name, record.score) for record in sorted_scores[:NUM_TRACKED_SCORES]]
    with open(c.SCORE_FILE) as file:
        file.writelines(lines)

class Control(object):
    """
    Main class for running the game states and window
    """

    def __init__(self, state_dict: dict, initial_state_name: str, persist=None):
        # Init
        self.state_dict = state_dict
        self.state_name = initial_state_name

        self.clock = pygame.time.Clock()
        self.fps: int = c.FPS
        self.paused = False
        self.running = True
        self.screen: pygame.Surface = pygame.display.get_surface()
        state_class: State.__class__ = self.state_dict[self.state_name]
        self.state: State = state_class(persist=persist)

    def flip_state(self):
        persist = self.state.cleanup()
        self.state_name = self.state.next_state_name
        state_class = self.state_dict[self.state_name]
        self.state = state_class(persist)
        self.state.state_start_time = pygame.time.get_ticks()

    def poll_events(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                self.running = False
                self.state.cleanup()
                return
            self.state.get_event(event)
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys

    def main_loop(self):
        while self.running:
            # TODO: fix huge delta times when the window gets unfocused or something (if possible?)
            delta_time = self.clock.tick(self.fps)

            # Poll events and get the pressed keys from pygame
            pressed_keys = self.poll_events()
            if not self.running:
                break

            self.state.current_time = pygame.time.get_ticks()  # update the state's time for it
            self.state.update(delta_time, pressed_keys)

            if self.state.is_done:
                self.flip_state()
            elif self.state.is_quit:
                self.running = False

            self.state.display(self.screen)
            pygame.display.update()


def main():
    # This function begins the main game loop inside the CONTROL class
    initial_state = c.TITLE_STATE
    state_dict = {c.TITLE_STATE: Title,
                  c.PLAY_STATE: Play,
                  c.SCORE_ENTRY_STATE: ScoreEntry,
                  c.GAME_OVER_STATE: GameOver,
                  c.DEMO_STATE: Demo}
    # persist = c.Persist(stars=Stars(), scores=[], current_score=16000, one_up_score=0, high_score=100000, \
    # num_shots=132, num_hits=257)
    persist = None
    the_galaga = Control(state_dict=state_dict, initial_state_name=initial_state, persist=persist)
    the_galaga.main_loop()
