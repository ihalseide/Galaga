import os

import pygame

FONT = pygame.font.Font(os.path.join("fonts", "ARCADECLASSIC.TTF"), 13)

GFX = pygame.image.load("sheet.png").convert()
GFX.set_colorkey((0,0,0), pygame.RLEACCEL)

def grab(x,y,w,h):
    return GFX.subsurface((x,y,w,h))
