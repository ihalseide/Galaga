"""
Constants for the rest of the game - no importing from other game code allowed here!
"""

from collections import namedtuple

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