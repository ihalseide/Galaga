"""
Constants for the rest of the game - no importing from other game code allowed here!
"""

# String constants for in-game
TITLE = 'Galaga'  # title for the game window
MENU_MESSAGE = 'GALAGA © 1981'
START = 'START'
HI_SCORE = 'HI-SCORE'
ONE_UP = '1UP'
HI_SCORE_NUM = '{: =6}'
STAGE = 'STAGE {: =3}'
READY = 'READY'

# Resources and other file paths
RESOURCES = "resources"
SCORE_FILE = "scores.txt"

# Game states
MENU_STATE = 'menu'
MENU_DEMO = 'menu demo'
PLAY_STATE = 'play'
PLAY_STATS = 'play stats'
NEW_SCORE_STATE = 'new high score'

# Game state to start at
INITIAL_STATE = MENU_STATE

# other keys
HUD = "hud"
STARS = 'stars'
LIFE = 'life'
STAGE_1 = 1
STAGE_5 = 5
STAGE_10 = 10
STAGE_20 = 20
STAGE_30 = 30
STAGE_50 = 50

# rotation of things
ANGLE_UP = 0
ANGLE_UP_RIGHT = 1
ANGLE_RIGHT = 2
ANGLE_DOWN_RIGHT = 3
ANGLE_DOWN = 4
ANGLE_DOWN_LEFT = 5
ANGLE_LEFT = 6
ANGLE_UP_LEFT = 7

# Game space
GAME_WIDTH, GAME_HEIGHT = 224, 288
SCREEN_WIDTH, SCREEN_HEIGHT = 224, 288
GAME_CENTER_X, GAME_CENTER_Y = GAME_WIDTH // 2, GAME_HEIGHT // 2

# Where the game area really starts and ends vertically to fit the HUD
STAGE_TOP = 30
STAGE_BOTTOM = GAME_HEIGHT - 20
BADGE_TOP = GAME_HEIGHT - 19

# Frames per second
FPS = 30
FLASH_FREQUENCY = 800

# Debug flags ( REMEMBER TO REMOVE IN RELEASE!! )
SKIP_WAITING = True
