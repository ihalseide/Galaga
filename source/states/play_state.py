
import time
import math
import random # used for stars

import pygame
from pygame.math import Vector2

from .. import setup
from .. import stages
from .. import timing
from ..tools import threaded
from .state import _State
from .. import constants as c
from ..components import star, player, missile, enemies

class Play(_State):
    START = "Intro"
    STAGE_CHANGE = "Stage Change"
    READY = "Ready"
    STAGE = "Stage"
    STATS = "Stage Statistics"
    GAME_OVER = "Game Over"

    LIFE = "Life"
    STAGE_1, STAGE_5, STAGE_10 =  1, 5, 10
    STAGE_20, STAGE_30, STAGE_50 = 20, 30, 50
    GRAPHICS = {
        LIFE: setup.grab_cells(6, 0, x_off=1, y_off=1, x_gap=1, y_gap=1),
        STAGE_1: setup.grab(222, 1, 7, 16),
        STAGE_5: setup.grab(205, 1, 7, 16),
        STAGE_10: setup.grab(189, 1, 14, 16),
        STAGE_20: setup.grab(171, 1, 16, 16),
        STAGE_30: setup.grab(154, 1, 16, 16),
        STAGE_50: setup.grab(137, 1, 16, 16),
    }
    BLINK_1UP = 0.45 # seconds
    STAGE_DURATION = 1.6 # ''
    READY_DURATION = 1.6 # ''
    TRANSITION_DURATION = 0.45 # ''
    NEW_ENEMY_WAIT = 0.3
    NEW_WAVE_WAIT = 1
    STAR_NUM = 90
    STAR_COLORS = (pygame.Color("red"), pygame.Color("blue"),
                   pygame.Color("blue"), pygame.Color("lightgreen"),
                   pygame.Color("white"))
    STAR_LAYERS = 2
    STAR_PHASES = [0, 0.25, 0.1]
    MAIN_FONT = pygame.font.Font(setup.FONTS["ARCADECLASSIC"], 12)
    random.seed(999)

    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)
        # vars
        self.highscore = persist.get("highscore")
        self.score = 0
        self.extra_lives = 3
        self.stage_num = 0 # stage 0 is start
        self.state = self.START
        self.stage = None
        self.stage_badges = None
        self.transition_timer = 0
        self.state_timer = 0
        self.shots = 0
        self.hits = 0
        self.stage_start = self.current_time
        self.bounds = pygame.Rect(0, 20, c.WIDTH, c.HEIGHT - 40)
        # star background
        self.moving = False
        # hud element timing
        self.timer_1up = timing.ToggleTicker(self.BLINK_1UP)
        self.enemy_animation_timer = enemies.Enemy.ANIMATION_TIME
        # sprites
        self.missiles = None
        self.enemy_missiles = None
        self.enemies = None
        self.player = None
        self.create_stars()
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
        if self.state == self.START:
            self.update_stars(dt, moving=0)
            if self.state_timer >= self.intro_duration:
                self.switch_state(self.STAGE_CHANGE)
        else:
            self.update_stars(dt, moving=1)
            if self.state == self.STAGE_CHANGE:
                if self.state_timer >= self.STAGE_DURATION:
                    self.switch_state(self.READY)
            elif self.state == self.READY:
                if self.state_timer >= self.READY_DURATION:
                    self.switch_state(self.STAGE)
            else:
                self.update_player(dt, keys)
                self.missiles.update(dt, self.bounds)
                self.enemies.update(dt)
                enemy_hits = pygame.sprite.groupcollide(self.enemies,
                              self.missiles, False, True)
                for enemy, hits in enemy_hits.items():
                    enemy.hit()

        # update timers
        if self.transition_timer and self.transition_timer > 0:
            self.transition_timer -= dt
        else:
            self.transition_timer = None
        self.state_timer += dt

    def display(self, screen, dt):
        screen.fill((0,0,0))
        self.draw_stars(screen)
        if self.player: self.player.draw(screen)
        if self.enemies:
            if self.enemy_animation_timer and self.enemy_animation_timer > 0:
                self.enemy_animation_timer -= dt
            else:
                self.enemy_animation_timer = enemies.Enemy.ANIMATION_TIME
                for e in self.enemies:
                    e.animate(dt)
            self.enemies.draw(screen)
        if self.missiles: self.missiles.draw(screen)
        if self.enemy_missiles: self.enemy_missiles.draw(screen)
        self.show_state(screen, dt)
        self.draw_hud(screen, dt)

    def switch_state(self, new_state):
        """
        For states within the game
        """
        self.state = new_state
        self.state_timer = 0
        if self.state == self.STAGE_CHANGE:
            self.transition_timer = self.TRANSITION_DURATION
            self.next_stage()
        elif self.state == self.READY:
            self.transition_timer = self.TRANSITION_DURATION
        elif self.state == self.STAGE:
            pass

    def create_stars(self):
        self.stars = []
        for i in range(self.STAR_NUM):
            x = random.randint(self.bounds.left, self.bounds.right)
            y = random.randint(self.bounds.top, self.bounds.bottom)
            c = random.choice(self.STAR_COLORS)
            z = random.randint(0, self.STAR_LAYERS-1)
            t = random.choice(self.STAR_PHASES)
            b = bool(random.randint(0,1))
            s = star.Star((x,y), color=c, z=z, twinkles=b, time_offset=t)
            self.stars.append(s)
        return self.stars

    def draw_stars(self, screen):
        for s in self.stars:
            s.display(screen)

    def update_stars(self, dt, moving:int):
        """
        Moving up, down, or not at all. (1,-1, or 0)
        """
        for s in self.stars:
            s.update(dt, self.bounds, moving)

    def calc_stage_badges(self):
        if self.stage_num == 0:
            return {}
        else:
            w_stage = self.stage_num # temporary modification
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
            return {self.STAGE_1: num_1, self.STAGE_5: num_5,
                    self.STAGE_10: num_10, self.STAGE_20: num_20,
                    self.STAGE_30: num_30, self.STAGE_50: num_50}

    def draw_hud(self, screen, dt):
        # --- top hud: score and highscore
        pygame.draw.rect(screen, (0,0,0), (0,0, c.WIDTH, 20))
        self.timer_1up.update(dt)
        if self.timer_1up.on:
            t = self.MAIN_FONT.render("1 UP", False, (255,0,0))
            screen.blit(t, (22, 1))
        if self.score == 0:
            score = "00"
        else:
            score = str(self.score).zfill(round(math.log(self.score, 10)))
        t = self.MAIN_FONT.render(score, False, (255,255,255))
        w = t.get_rect().width
        screen.blit(t, (60-w, 10))
        t = self.MAIN_FONT.render("HIGH SCORE", False, (255,0,0))
        size = t.get_rect().width
        screen.blit(t, ((c.WIDTH - size)//2, 1))
        score = str(self.highscore)
        t = self.MAIN_FONT.render(score, False, (255,255,255))
        size = t.get_rect().width
        screen.blit(t, ((c.WIDTH - size)//2, 10))
        # --- bottom hud: lives and stage
        pygame.draw.rect(screen, (0,0,0),
                         (0,self.bounds.bottom,c.WIDTH,20))
        # lives
        for i in range(self.extra_lives):
            screen.blit(self.GRAPHICS[self.LIFE],
                        (1+i*16, self.bounds.bottom + 1, 16, 16))

        if self.stage_badges: self.draw_stage_badges(screen)

    def draw_stage_badges(self, screen):
        # draw the stage level badges
        draw_x = c.WIDTH
        h = c.HEIGHT - 20
        for n in range(self.stage_badges[self.STAGE_1]):
            draw_x -= 8
            screen.blit(self.GRAPHICS[self.STAGE_1], (draw_x, h, 7, 16))
        for n in range(self.stage_badges[self.STAGE_5]):
            draw_x -= 8
            screen.blit(self.GRAPHICS[self.STAGE_5], (draw_x, h, 7, 16))
        for n in range(self.stage_badges[self.STAGE_10]):
            draw_x -= 14
            screen.blit(self.GRAPHICS[self.STAGE_10], (draw_x, h, 14, 16))
        for n in range(self.stage_badges[self.STAGE_20]):
            draw_x -= 16
            screen.blit(self.GRAPHICS[self.STAGE_20], (draw_x, h, 16, 16))
        for n in range(self.stage_badges[self.STAGE_30]):
            draw_x -= 16
            screen.blit(self.GRAPHICS[self.STAGE_30], (draw_x, g, 16, 16))
        for n in range(self.stage_badges[self.STAGE_50]):
            draw_x -= 16
            screen.blit(self.GRAPHICS[self.STAGE_50], (draw_x, h, 16, 16))

    def mid_text(self, screen, text, color, location=c.SCREEN_CENTER):
        t = self.MAIN_FONT.render(text, False, color)
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

    @threaded
    def startup_stage(self):
        for i, wave_g in enumerate(self.stage.wave_groups):
            for j, wave in enumerate(wave_g):
                path = wave.path
                loc = wave.start_slot
                for k, enemy_spot in enumerate(wave.enemies):
                    r, c = enemy_spot.row, enemy_spot.col
                    e = enemy_spot.enemy(loc, path, (r, c))
                    self.enemies.add(e)
                    time.sleep(self.NEW_ENEMY_WAIT)
            time.sleep(self.NEW_WAVE_WAIT)

    def next_stage(self):
        setup.SFX["stage award"].play()
        # vars helpful
        self.stage_start = self.current_time
        self.stage_num += 1
        self.stage_badges = self.calc_stage_badges()
        self.stage = stages.stages[self.stage_num]
        # sprites setup
        self.enemies = pygame.sprite.Group()
        if not self.enemy_missiles:
            self.enemy_missiles = pygame.sprite.Group()
        if not self.missiles:
            self.missiles = pygame.sprite.Group()
        if not self.player:
            self.extra_lives -= 1
            self.player = pygame.sprite.Group(player.Player())
        self.startup_stage()

    def update_player(self, dt, keys):
        self.player.update(dt, keys)
        # make controllable players shoot
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
