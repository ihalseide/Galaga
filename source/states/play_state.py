
import math
import random # used for stars

import pygame
from pygame.math import Vector2

from .. import stages
from .. import timing
from .state import _State
from .. import setup
from .. import constants as c
from ..components import star, player

class Play(_State):
    START = "Intro"
    STAGE_CHANGE = "Stage Change"
    READY = "Ready"
    STAGE = "Stage"
    STATS = "Stage Statistics"
    GAME_OVER = "Game Over"

    BLINK_1UP = 0.45 # seconds
    INTRO_DURATION = 5 # seconds
    STAGE_DURATION = 1.6, 0.4 # ''
    READY_DURATION = 1.6, 0.4 # ''
    ENEMY_TIME_GAP = 0.1 # ''
    TRANSITION_DURATION = 0.45 # ''
    STAR_NUM = 100
    STAR_COLORS = (pygame.Color("red"), pygame.Color("blue"),
                   pygame.Color("blue"), pygame.Color("lightgreen"),
                   pygame.Color("white"))
    STAR_LAYERS = 2
    STAR_PHASES = [0, 0.25, 0.1]
    MAIN_FONT = pygame.font.Font(setup.FONTS["ARCADECLASSIC"], 12)

    def __init__(self):
        _State.__init__(self)

    def startup(self, time, persist={}):
        _State.startup(self, time, persist)

        self.highscore = persist.get("highscore")
        self.score = 0
        self.extra_lives = 3
        self.stage_num = 99 # stage 0 is start
        self.state = self.START
        self.stage = None
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

        self.missiles = None
        self.enemy_missiles = None
        self.enemies = None
        self.player = None
        self.create_stars()

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        pass

    def update(self, dt, keys):
        _State.update(self, dt, keys)
        if self.state == self.START:
            self.update_stars(dt, moving=False)
            if self.state_timer >= self.INTRO_DURATION:
                self.state = self.STAGE_CHANGE
                self.state_timer = 0
                self.transition_timer = self.TRANSITION_DURATION
                self.next_stage()
        else:
            self.update_stars(dt, moving=True)
            if self.state == self.STAGE_CHANGE:
                if self.state_timer >= self.STAGE_DURATION:
                    self.state = self.READY
                    self.transition_timer = self.TRANSITION_DURATION
                    self.state_timer = 0
            elif self.state == self.READY:
                if self.state_timer >= self.READY_DURATION:
                    self.state = self.STAGE
                    self.state_timer = 0
            else:
                self.update_player(dt, keys)
                self.missiles.update(dt, self.bounds)
                if self.state == self.STAGE:
                    self.update_stage(dt)
                elif self.state == self.STATS:
                    pass
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
        if self.enemies: self.enemies.draw(screen)
        if self.missiles: self.missiles.draw(screen)
        if self.enemy_missiles: self.enemy_missiles.draw(screen)
        self.show_state(screen, dt)
        self.draw_hud(screen, dt)

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

    def update_stars(self, dt, moving):
        for s in self.stars:
            s.update(dt, self.bounds, moving)

    def update_stage(self, dt):
        pass

    def draw_hud(self, screen, dt):
        grab = setup.GFX["sheet"].subsurface
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
            screen.blit(grab((102, 1, 16, 16)),
                        (1+i*16, self.bounds.bottom + 1, 16, 16))
        # calculate num. of stage symbols
        if self.stage_num == 0:
            return
        w_stage = self.stage_num # temporary modification
        num_50 = w_stage // 50
        w_stage -= num_50 * 50
        num_30 = w_stage // 30
        w_stage -= num_30 * 30
        num_20 = w_stage // 20
        w_stage -= num_20*20
        num_10 = w_stage // 10
        w_stage -= num_10*10
        num_5 = w_stage // 5
        num_1 = w_stage - num_5*5
        draw_x = c.WIDTH
        for n in range(num_1):
            draw_x -= 8
            screen.blit(grab((221, 1, 7, 16)),
                        (draw_x, c.HEIGHT-20, 7, 16))
        for n in range(num_5):
            draw_x -= 8
            screen.blit(grab((204, 1, 7, 16)),
                        (draw_x, c.HEIGHT-20, 7, 16))
        for n in range(num_10):
            draw_x -= 14
            screen.blit(grab((188, 1, 14, 16)),
                        (draw_x, c.HEIGHT-20, 14, 16))
        for n in range(num_20):
            draw_x -= 16
            screen.blit(grab((170, 1, 16, 16)),
                        (draw_x, c.HEIGHT-20, 16, 16))
        for n in range(num_30):
            draw_x -= 16
            screen.blit(grab((153, 1, 16, 16)),
                        (draw_x, c.HEIGHT-20, 16, 16))
        for n in range(num_50):
            draw_x -= 16
            screen.blit(grab((136, 1, 16, 16)),
                        (draw_x, c.HEIGHT-20, 16, 16))

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
            # v is multiplied by speed in the missile class
            v = Vector2(0, -1)
            x = player.rect.centerx
            y = player.rect.top - 3
            m = missile.Missile((x,y), v, enemy=False)
            player.last_fire_time = self.current_time
            self.missiles.add(m)

    def next_stage(self):
        self.stage_start = self.current_time
        self.stage_num += 1
        self.stage = stages.stages[self.stage_num - 1]

        self.enemies = pygame.sprite.Group()
        if not self.enemy_missiles:
            self.enemy_missiles = pygame.sprite.Group()
        if not self.missiles:
            self.missiles = pygame.sprite.Group()
        if not self.player:
            self.extra_lives -= 1
            self.player = pygame.sprite.Group(player.Player())

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
