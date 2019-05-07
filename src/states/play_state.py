import time
import math

import pygame
from pygame.math import Vector2

from .. import setup
from .. import tools
from .. import stages
from .. import timing
from .. import scoring
from .. import constants as c

from ..tools import threaded
from ..components import player, missile, enemies, stars, hud

from .state import _State

# States within the play state
INTRO = "intro"
STAGE_CHANGE = "stage change"
READY = "ready"
STAGE = "stage"
GAME_OVER = "game over"

FIRE_COOLDOWN = 0.4

STAGE_TOP = 20
STAGE_BOTTOM = c.HEIGHT - STAGE_TOP
BADGE_X = c.WIDTH - 2

# sprite resources
GRAPHICS = {
    'life': tools.sheet_grab_cells(7, 0),
    'stage 1': tools.sheet_grab(13*16, 48, 7, 16),
    'stage 5': tools.sheet_grab(12*16, 48, 7, 16),
    'stage 10': tools.sheet_grab(11*16, 48, 14, 16),
    'stage 20': tools.sheet_grab(10*16, 48, 15, 16),
    'stage 30': tools.sheet_grab(9*16, 48, 16, 16),
    'stage 50': tools.sheet_grab(8*16, 48, 16, 16),
}
STAGE_DURATION = 1.6       # secconds 
READY_DURATION = 1.6       # ''
TRANSITION_DURATION = 0.45 # ''
BADGE_TIME = 0.045           # ''

class Play(_State):
    def __init__(self, persist={}):
        _State.__init__(self, persist)
        # star background
        stars.set_moving(False)
        # vars
        self.highscore = scoring.get_high()
        self.score = 0
        self.extra_lives = 3
        self.timer = None
        self.state_timer = 0
        # player vars
        self.shots = 0
        self.hits = 0
        self.last_fire_time = 0
        # stage manager
        self.state = INTRO
        self.stage_num = 25
        self.stage_badges = {}
        self.badge_num = 0
        self.shown_badges = 0
        # sprites
        self.missiles = pygame.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        # hud timing
        self.show_message = False
        self.message = None
        # start the intro
        theme = setup.SFX.get('theme')
        theme.play()
        # when done, start stage 1
        self.state = INTRO
        self.timer = timing.Countdown(theme.get_length() + TRANSITION_DURATION)

    def create_player(self):
        self.extra_lives -= 1
        self.players.add(player.Player())
        
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # shoot missiles
                self.player_fire()

    def update(self, dt, keys):
        # stars
        stars.update(dt)
        # player
        self.update_player(dt, keys)
        # update sprites
        self.missiles.update(dt)
        self.enemies.update(dt)
        self.enemy_missiles.update(dt)
        # state
        if self.timer:
            self.timer.update(dt)
        if self.state == INTRO:
            if self.timer.done:
                self.state = STAGE_CHANGE
                self.stage_num += 1
                # how many of each type needed
                self.stage_badges = tools.calc_stage_badges(self.stage_num)
                # count the number of badges needed to draw
                self.badge_num = sum(x for x in self.stage_badges.values())
                # animate them
                self.shown_badges = 0
                self.timer = timing.Countdown(BADGE_TIME)
        elif self.state == STAGE_CHANGE:
            # when the stage badges update
            if self.timer.done:
                # create more badges on a timer
                if self.shown_badges < self.badge_num:
                    self.shown_badges += 1
                    setup.SFX['stage award'].play()
                    self.timer = timing.Countdown(BADGE_TIME)
                else:
                    # done with badges, setup stage
                    self.state = STAGE
                    self.timer = None
                    self.create_player()
                    stars.set_moving(1)
        elif self.state == STAGE:
            pass

    def display(self, screen, dt):
        # clear screen
        screen.fill((0,0,0))
        # stars
        stars.display(screen)
        # draw enemies
        # draw player
        if self.players:
            self.players.draw(screen)
        # draw bullets
        if self.missiles:
            self.missiles.draw(screen)
        if self.enemy_missiles:
            self.enemy_missiles.draw(screen)
        # draw HUD
        self.draw_hud(screen, dt)

    def draw_hud(self, screen, dt):
        # call external hud
        hud.draw_for_play(screen, dt, self.score, self.highscore)
        # clear spot for lives and stages
        pygame.draw.rect(screen, pygame.Color('black'),
                         (0, STAGE_BOTTOM, c.WIDTH, c.HEIGHT - STAGE_BOTTOM))
        # lives
        for i in range(self.extra_lives):
            screen.blit(GRAPHICS['life'], (1+i*16, STAGE_BOTTOM + 1, 16, 16))
        # stage badges
        if self.stage_badges:
            self.draw_stage_badges(screen)
        # draw middle message
        if self.show_message:
            if self.message == 'start' or self.message == 'ready':
                color = pygame.Color('red')
            elif self.message == 'stage':
                color = pygame.Color('skyblue')
            self.mid_text(screen, self.message, color, c.SCREEN_CENTER)

    def draw_stage_badges(self, screen):
        # draw the stage level badges
        draw_x = BADGE_X
        h = STAGE_BOTTOM
        drawn = 0
        for n in range(self.stage_badges[1]):
            if drawn >= self.shown_badges: break
            draw_x -= 8
            screen.blit(GRAPHICS['stage 1'], (draw_x, h, 7, 16))
            drawn += 1
        for n in range(self.stage_badges[5]):
            if drawn >= self.shown_badges: break
            draw_x -= 8
            screen.blit(GRAPHICS['stage 5'], (draw_x, h, 7, 16))
            drawn += 1
        for n in range(self.stage_badges[10]):
            if drawn >= self.shown_badges: break
            draw_x -= 14
            screen.blit(GRAPHICS['stage 10'], (draw_x, h, 14, 16))
            drawn += 1
        for n in range(self.stage_badges[20]):
            if drawn >= self.shown_badges: break
            draw_x -= 16
            screen.blit(GRAPHICS['stage 20'], (draw_x, h, 16, 16))
            drawn += 1
        for n in range(self.stage_badges[30]):
            if drawn >= self.shown_badges: break
            draw_x -= 16
            screen.blit(GRAPHICS['stage 30'], (draw_x, h, 16, 16))
            drawn += 1
        for n in range(self.stage_badges[50]):
            if drawn >= self.shown_badges: break
            draw_x -= 16
            screen.blit(GRAPHICS['stage 50'], (draw_x, h, 16, 16))
            drawn += 1

    def mid_text(self, screen, text, color, location=c.SCREEN_CENTER):
        t = tools.font_render(text, color)
        rect = t.get_rect()
        rect.center = location
        screen.blit(t, rect)

    def create_missile(self, player):
        # v is multiplied by speed in the missile class
        v = Vector2(0, -1)
        x = player.rect.centerx
        y = player.rect.top + 10
        m = missile.Missile((x,y), v, enemy=False)
        self.missiles.add(m)

    def player_fire(self):
        # check limit fire rate
        if (time.time() - self.last_fire_time) >= FIRE_COOLDOWN:
            # play sound
            setup.SFX["player fire"].play()
            # create right number of missiles
            for p in self.players:
                self.create_missile(p)
            # limit fire rate
            self.last_fire_time = time.time()

    def update_player(self, dt, keys):
        self.players.update(dt, keys)
        