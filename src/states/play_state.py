
import time
import math

import pygame
from pygame.math import Vector2

from .state import _State
from .. import setup
from .. import tools
from .. import stages
from .. import timing
from .. import constants as c
from ..tools import threaded
from ..components import player, missile, enemies, stars, hud

class Play(_State):
    # States within the play state
    START = "Intro"
    STAGE_CHANGE = "Stage Change"
    READY = "Ready"
    STAGE = "Stage"
    STATS = "Stage Statistics"
    GAME_OVER = "Game Over"

    STAGE_TOP = 20
    STAGE_BOTTOM = c.HEIGHT - 20
    # sprite resources
    GRAPHICS = {
        'life': tools.sheet_grab_cells(7, 0),
        'stage 1': tools.sheet_grab(7, 3, 7, 16),
        'stage 5': tools.sheet_grab(0, 3, 7, 16),
        'stage 10': tools.sheet_grab(0, 3, 14, 16),
        'stage 20': tools.sheet_grab(0, 3, 15, 16),
        'stage 30': tools.sheet_grab(0, 3, 16, 16),
        'stage 50': tools.sheet_grab(8, 3, 16, 16),
    }
    STAGE_DURATION = 1.6       # secconds 
    READY_DURATION = 1.6       # ''
    TRANSITION_DURATION = 0.45 # ''
    NEW_ENEMY_WAIT = 0.3       # ''
    NEW_WAVE_WAIT = 1          # '' 

    def __init__(self, persist={}):
        _State.__init__(self, persist)
        # vars
        self.highscore = persist.get("highscore")
        self.score = 0
        self.extra_lives = 3
        self.state = self.START
        self.transition_timer = 0
        self.state_timer = 0
        # statistics
        self.shots = 0
        self.hits = 0
        # stage manager
        self.stager = None
        self.stage_num = 0
        self.stage = None
        self.stage_badges = {}
        # star background
        stars.set_moving(False)
        # hud element timing
        self.enemy_animation_timer = enemies.Enemy.ANIMATION_TIME
        # sprites
        self.missiles = None
        self.enemy_missiles = None
        self.enemies = None
        self.player = None
        # sound
        setup.SFX["theme"].play()
        self.intro_duration = (setup.SFX["theme"].get_length()
                               + self.TRANSITION_DURATION)

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        pass

    def update(self, dt, keys):
        _State.update(self, dt, keys)
        stars.update(dt)

    def display(self, screen, dt):
        # clear screen
        screen.fill((0,0,0))
        # stars
        stars.display(screen)
        # draw enemies
        # draw player
        # draw bullets
        # draw HUD
        self.draw_hud(screen, dt)

    def draw_hud(self, screen, dt):
        # call external hud
        hud.draw_for_play(screen, dt, self.score, self.highscore)
        # clear spot for lives and stages
        bottom = self.STAGE_BOTTOM
        pygame.draw.rect(screen, pygame.Color('black'),
                         (0, bottom, c.WIDTH, c.HEIGHT - bottom))
        # lives
        for i in range(self.extra_lives):
            screen.blit(self.GRAPHICS['life'],
                        (1+i*16, self.STAGE_BOTTOM + 1, 16, 16))
        # stage badges
        if self.stage_badges:
            self.draw_stage_badges(screen)
        # draw middle message
        self.show_state(screen, dt)

    def draw_stage_badges(self, screen):
        # draw the stage level badges
        draw_x = c.WIDTH
        h = c.HEIGHT - 20
        for n in range(self.stage_badges[1]):
            draw_x -= 8
            screen.blit(self.GRAPHICS['stage 1'], (draw_x, h, 7, 16))
        for n in range(self.stage_badges[5]):
            draw_x -= 8
            screen.blit(self.GRAPHICS['stage 5'], (draw_x, h, 7, 16))
        for n in range(self.stage_badges[10]):
            draw_x -= 14
            screen.blit(self.GRAPHICS['stage 10'], (draw_x, h, 14, 16))
        for n in range(self.stage_badges[20]):
            draw_x -= 16
            screen.blit(self.GRAPHICS['stage 20'], (draw_x, h, 16, 16))
        for n in range(self.stage_badges[30]):
            draw_x -= 16
            screen.blit(self.GRAPHICS['stage 30'], (draw_x, h, 16, 16))
        for n in range(self.stage_badges[50]):
            draw_x -= 16
            screen.blit(self.GRAPHICS['stage 50'], (draw_x, h, 16, 16))

    def mid_text(self, screen, text, color, location=c.SCREEN_CENTER):
        t = tools.font_render(text, False, color)
        rect = t.get_rect()
        rect.center = location
        screen.blit(t, rect)

    def show_state(self, screen, dt):
        if self.transition_timer:
            return
        elif self.state == self.START:
            self.mid_text(screen, "START", pygame.Color("red"), c.SCREEN_CENTER)
        elif self.state == self.STAGE_CHANGE:
            s = "STAGE %s" %(self.stage_num)
            self.mid_text(screen, s, pygame.Color("skyblue"), c.SCREEN_CENTER)
        elif self.state == self.READY:
            self.mid_text(screen, "READY", pygame.Color("red"), c.SCREEN_CENTER)

    def player_fire(self, dt, player):
        if player.can_fire(self.current_time):
            setup.SFX["player fire"].play()
            # v is multiplied by speed in the missile class
            v = Vector2(0, -1)
            x = player.rect.centerx
            y = player.rect.top + 10
            m = missile.Missile((x,y), v, enemy=False)
            player.last_fire_time = self.current_time
            self.missiles.add(m)

    def update_player(self, dt, keys):
        self.player.update(dt, keys)
        players = [p for p in self.player if p.controllable]
        counted_shot = False
        for p in players:
            if keys[pygame.K_SPACE]:
                if not counted_shot and p.can_fire(self.current_time):
                    self.shots += 1
                    counted_shot = True
                self.player_fire(dt, p)
            if p.rect.left < self.bounds.left:
                p.rect.left = self.bounds.left
            elif p.rect.right > self.bounds.right:
                p.rect.right = self.bounds.right
