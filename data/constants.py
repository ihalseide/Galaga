"""
Constants for the rest of the game - no importing from other game code allowed here!
"""

TITLE = 'Galaga'  # title for the game window

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
SPEED = 'speed'
COLORS = 'colors'
ON: bool = True
OFF: bool = False

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
