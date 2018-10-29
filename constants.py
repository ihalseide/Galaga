
import pygame

# Game States
START_STATE = "Start"
PLAY_STATE = "Play"
SCORED_STATE = "Scored"

WIDTH, HEIGHT = 224, 288
SIZE = WIDTH, HEIGHT
CENTER_X, CENTER_Y = WIDTH//2, HEIGHT//2
CENTER = CENTER_X, CENTER_Y
FPS = 30

# events
e = 0
def new_event():
    global e
    e += 1
    return pygame.USEREVENT + e

NEW_ENEMY = new_event()
