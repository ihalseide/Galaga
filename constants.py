# Directories
SOUNDS_DIR = 'audio'
RESOURCE_DIR = "resources"
SCORE_FILE = "scores.txt"

# Game state keys
STATE_TITLE = 'title state'
STATE_DEMO = 'demo state'
STATE_PLAY = 'play state'
STATE_SCORE_ENTRY = 'score entry state'
STATE_GAME_OVER = 'game over state'

# Sting messages for game over
RESULT_TEXT = "- Results -"  # text is red
SHOTS_FIRED_TEXT = 'Shots Fired {: >12}'  # text is light blue
NUM_HITS_TEXT = 'Number of Hits {: >9}'  # text is white
HIT_MISS_RATIO = 'Hit-Miss ratio {: >10.1%}'  # text is yellow

# Game space
GAME_WIDTH, GAME_HEIGHT = 224, 288
GAME_CENTER_X, GAME_CENTER_Y = GAME_WIDTH // 2, GAME_HEIGHT // 2
STAGE_TOP_Y = 30  # Y-coord. for the top of the stage
STAGE_BOTTOM_Y = GAME_HEIGHT - 20  # Y-coord. for the bottom of the stage
BADGE_Y = GAME_HEIGHT - 19  # Y-coord for the top of the stage badges

# Timing and frequencies in milliseconds unless otherwise noted
EXPLOSION_PLAYER_FRAME = 140
EXPLOSION_ENEMY_FRAME = 120
FPS = 30 # frames per second
TEXT_FLASH_FREQ = 300
PLAYER_FIRE_COOLDOWN = 400
PLAYER_SPEED = 0.085
STAGE_DURATION = 1600
READY_DURATION = 1600
INTRO_MUSIC_DURATION = 6600
START_NOISE_WAIT = 0
START_DURATION = START_NOISE_WAIT + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 200
FIRE_COOLDOWN = 200
GAME_OVER_DURATION = 3000
GAME_OVER_STATE_DURATION = 14500
BLINK_1UP = 450

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
LIGHT_GREEN = (144, 238, 144)

# Title settings
SCORE_Y = 10
TITLE_Y = SCORE_Y + 80
START_Y = TITLE_Y + 110
COPY_Y = START_Y + 60
MENU_SPEED = 3
TITLE_FLASH_TIME = 150  # millis.
TITLE_FLASH_NUM = 12

# Font spritesheet coordinates and stuff
FONT_ALPHABET_Y = 224
FONT_CHAR_SIZE = 8
LINE_TEXT_HEIGHT = 16

# Number of stars in the star field background
STAR_COUNT = 64
