__author__ = "Izak Halseide"

import pygame
from pygame.math import Vector2

from data import constants as c, player, hud, missile, stars, stages
from data import setup
from data import tools
from data.explosion import Explosion
from data.state import State

# sprite resources for HUD
GRAPHICS = {
    c.LIFE: tools.grab_sheet(96, 0, 16, 16),
    c.STAGE_1: tools.grab_sheet(208, 48, 7, 16),
    c.STAGE_5: tools.grab_sheet(192, 48, 7, 16),
    c.STAGE_10: tools.grab_sheet(176, 48, 14, 16),
    c.STAGE_20: tools.grab_sheet(160, 48, 15, 16),
    c.STAGE_30: tools.grab_sheet(144, 48, 16, 16),
    c.STAGE_50: tools.grab_sheet(128, 48, 16, 16),
}

# Timing (in milliseconds)
STAGE_DURATION = 1600
READY_DURATION = 1600
TRANSITION_DURATION = 450
NEW_ENEMY_WAIT = 300
NEW_WAVE_WAIT = 1000
INTRO_MUSIC_DURATION = 6600
START_NOISE_WAIT = 1000
START_DURATION = START_NOISE_WAIT + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 150


class Play(State):

    @staticmethod
    def draw_mid_text(screen, text, color, line=1):
        x, y = c.GAME_CENTER_X, c.GAME_CENTER_Y + 16 * line
        tools.draw_text(screen, text, (x, y), color, centered_x=True, centered_y=True)

    @staticmethod
    def calc_stage_badges(stage_num: int) -> dict:
        """
        Calculate how many of each stage badges there are for a given stage
        """
        if stage_num <= 0:
            num_1 = num_5 = num_10 = num_20 = num_30 = num_50 = 0
        else:
            w_stage = stage_num  # temp. var
            num_50 = w_stage // c.STAGE_50
            w_stage -= num_50 * c.STAGE_50
            num_30 = w_stage // c.STAGE_30
            w_stage -= num_30 * c.STAGE_30
            num_20 = w_stage // c.STAGE_20
            w_stage -= num_20 * c.STAGE_20
            num_10 = w_stage // c.STAGE_10
            w_stage -= num_10 * c.STAGE_10
            num_5 = w_stage // c.STAGE_5
            num_1 = w_stage - num_5 * c.STAGE_5
        return {
            c.STAGE_1: num_1, c.STAGE_5: num_5, c.STAGE_10: num_10, c.STAGE_20: num_20, c.STAGE_30: num_30,
            c.STAGE_50: num_50}

    @staticmethod
    def play_badge_noise():
        setup.get_sfx('stage_award').play()

    @staticmethod
    def play_fire_noise():
        setup.get_sfx("fighter_fire").play()

    def __init__(self, persist=None):
        # do the things all states must do...
        State.__init__(self, persist)
        self.next = c.PLAY_STATS
        self.current_time = 0

        # init stars
        maybe_stars = self.persist.get(c.STARS)
        self.stars = maybe_stars if maybe_stars else stars.Stars()
        self.stars.set_moving(False)

        # init hud
        maybe_hud = self.persist.get(c.HUD)
        self.hud = maybe_hud if maybe_hud else hud.Hud(0, 30000)

        # init player
        self.is_player_alive = False
        self.player = player.Player(x=c.GAME_WIDTH // 2, y=c.GAME_HEIGHT - 25)
        self.extra_lives = 3
        self.can_control_player = False
        self.last_fire_time = 0

        # init stage badges
        self.stage_num = 0
        self.num_badges = 0
        self.stage_badges = self.calc_stage_badges(self.stage_num)
        self.is_animating_stage_badges = False
        self.stage_badge_animation_step = 0
        self.stage_badge_animation_timer = 0

        # missile sprites and such
        self.missiles = pygame.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()

        # Explosions sprites
        self.explosions = pygame.sprite.Group()

        # enemies and level
        # TODO: add path following and circling around, etc. to enemies
        self.formation_spread_pixels: int = 0
        self.formation_x_offset: int = 0
        self.formation_y_offset = c.STAGE_TOP + 10
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.the_stage: stages.Stage = stages.load_stage(1)  # pre-load stage #1
        self.is_ready = False
        self.should_return_enemies_to_formation = False

        # game area boundary
        self.bounds = pygame.Rect(0, c.STAGE_TOP, c.GAME_WIDTH, c.STAGE_BOTTOM - c.STAGE_TOP)

        # timers
        self.blocking_timer = 0  # this timer is for timing how long to show messages on screen
        self.is_starting = True
        self.has_started_intro_music = False
        self.should_show_ready = False
        self.should_show_stage = False
        self.should_spawn_enemies = False
        self.flashing_timer = 0
        self.flash_flag = False

    def cleanup(self):
        return self.persist

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.is_player_alive and self.can_control_player:
                self.fighter_shoots()

    def fighter_shoots(self):
        self.play_fire_noise()
        # v is multiplied by speed in the missile class
        # noinspection PyArgumentList
        v = Vector2(0, -0.350)
        x = self.player.rect.centerx
        y = self.player.rect.top + 10
        m = missile.Missile(x, y, v, is_enemy=False)
        self.last_fire_time = self.current_time
        self.missiles.add(m)

    def play_intro_music(self):
        if c.SKIP_WAITING:
            self.has_started_intro_music = True
            self.blocking_timer = START_DURATION
            return
        setup.get_sfx("theme").play()
        self.has_started_intro_music = True

    def animate_stage_badges(self, dt):
        if not self.is_animating_stage_badges:
            return

        if self.stage_badge_animation_step > self.num_badges:
            self.is_animating_stage_badges = False

        self.stage_badge_animation_timer += dt

        if (self.stage_badge_animation_timer >= STAGE_BADGE_DURATION) and (
                self.stage_badge_animation_step < self.num_badges):
            self.stage_badge_animation_step += 1
            self.stage_badge_animation_timer = 0
            self.play_badge_noise()

    def get_formation_pos(self, formation_x, formation_y):
        # TODO: factor in "spread"
        x = self.formation_x_offset + formation_x * 17
        y = self.formation_y_offset + formation_y * 17
        return x, y

    def update(self, delta_time, keys):
        self.current_time += delta_time
        self.update_missiles(delta_time)
        self.animate_stage_badges(delta_time)
        self.stars.update(delta_time)
        self.update_timers(delta_time)
        self.explosions.update(delta_time, self.flash_flag)
        # update player
        if self.is_player_alive:
            self.update_player(delta_time, keys)
        # update stage spawning
        if self.the_stage:
            self.update_stage(delta_time)
        # update enemies
        if self.the_stage and self.enemies:
            self.enemies.update(delta_time, self.flash_flag)

    def update_stage(self, dt: float):
        if self.is_ready:
            self.the_stage.update(dt)
            new_enemy = self.the_stage.get_new_enemy()
            if new_enemy:
                self.enemies.add(new_enemy)

    def add_explosion(self, x, y):
        self.explosions.add(Explosion(x, y))
        setup.get_sfx("explosion").play()

    def update_missiles(self, delta_time):
        for m in self.missiles.sprites():
            m.update(delta_time, self.flash_flag)
            hit_enemies = pygame.sprite.spritecollide(m, self.enemies, dokill=False)
            for sprite in hit_enemies:
                sprite.kill()
                self.add_explosion(sprite.x, sprite.y)
                # TODO: add to score
                # TODO: create score text
            if not self.bounds.contains(m.rect) or hit_enemies:
                m.kill()

    def decrement_lives(self):
        self.extra_lives -= 1

    def update_timers(self, dt: float):
        # the "blocking" timer that blocks stuff
        if self.is_starting:
            self.blocking_timer += dt
            if not self.has_started_intro_music:
                if self.blocking_timer >= START_NOISE_WAIT:
                    self.play_intro_music()
            if self.blocking_timer >= START_DURATION:
                self.done_starting()
        elif self.should_show_stage:
            self.blocking_timer += dt
            if self.blocking_timer >= STAGE_DURATION:
                self.done_showing_stage()
                self.show_ready()
        elif self.should_show_ready:
            self.blocking_timer += dt
            if self.blocking_timer >= READY_DURATION:
                self.done_with_ready()
        # the "flashing timer" for synchronized flashing of some things
        self.flashing_timer += dt
        if self.flashing_timer >= c.FLASH_FREQUENCY:
            self.flashing_timer = 0
            self.flash_flag = not self.flash_flag

    def show_ready(self):
        self.should_show_ready = True
        self.stars.set_moving(1)

    def done_showing_stage(self):
        self.should_show_stage = False
        self.blocking_timer = 0

    def done_with_ready(self):
        self.should_show_ready = False
        self.can_control_player = True
        self.blocking_timer = 0
        self.is_ready = True

    def done_starting(self):
        self.is_starting = False
        self.blocking_timer = 0
        self.spawn_player()
        self.decrement_lives()
        self.stage_num = 0
        self.next_stage()
        self.should_show_stage = True

    def next_stage(self):
        self.stage_num += 1
        # this check is made because stage #1 is pre-loaded
        # ERROR BELOW: self.the_stage is None
        if not self.the_stage.stage_num == self.stage_num:
            self.the_stage = stages.load_stage(self.stage_num)
            self.the_stage.enemy_group_reference = self.enemies
        self.update_stage_badges()
        self.start_animating_stage_badges()

    def start_animating_stage_badges(self):
        self.is_animating_stage_badges = True
        self.stage_badge_animation_step = 0

    def update_stage_badges(self):
        self.stage_badges = self.calc_stage_badges(self.stage_num)
        self.num_badges = sum(self.stage_badges.values())

    def spawn_player(self):
        self.is_player_alive = True
        self.player = player.Player(c.GAME_WIDTH // 2, c.GAME_HEIGHT - 25)

    def display(self, screen, dt):
        # clear screen
        screen.fill(pygame.Color('black'))
        # stars
        self.stars.display(screen)
        if self.the_stage:
            # draw enemies
            for enemy in self.enemies:
                enemy.display(screen)
        # draw player
        if self.is_player_alive:
            self.player.display(screen)
        # draw bullets
        for m in self.missiles:
            m.display(screen)
        # draw explosions
        for x in self.explosions:
            x.display(screen)
        # draw HUD
        self.display_hud(screen)
        # debug
        # tools.draw_text(screen, str(len(self.explosions)), (40, 40), pygame.Color('red'))
        if c.SKIP_WAITING:
            pygame.draw.rect(screen, pygame.Color('green'), (0, 0, c.GAME_WIDTH, c.GAME_HEIGHT), 1)

    # pygame.draw.rect(screen, (255,255,255), self.bounds, 1)

    def draw_lives(self, screen):
        # lives
        for i in range(self.extra_lives):
            screen.blit(GRAPHICS[c.LIFE], (3 + i * 16, c.STAGE_BOTTOM + 1, 16, 16))

    def display_hud(self, screen):
        # clear the top for the hud when in play state
        screen.fill(pygame.Color('black'), (0, 0, c.GAME_WIDTH, c.STAGE_TOP))
        # call external hud
        self.hud.display(screen)
        # clear spot for lives and stages
        screen.fill(pygame.Color('black'), (0, c.STAGE_BOTTOM, c.GAME_WIDTH, c.GAME_HEIGHT - c.STAGE_BOTTOM))
        self.draw_lives(screen)
        # stage badges
        self.draw_stage_badges(screen)
        # draw middle message
        self.show_state(screen)

    def draw_stage_badges(self, screen):
        # draw the stage level badges
        draw_x = c.GAME_WIDTH
        h = c.BADGE_TOP
        number_to_draw = self.stage_badge_animation_step

        for n in range(self.stage_badges[c.STAGE_1]):
            if number_to_draw > 0:
                draw_x -= 8
                screen.blit(GRAPHICS[c.STAGE_1], (draw_x, h, 7, 16))
                number_to_draw -= 1
            else:
                return

        for n in range(self.stage_badges[c.STAGE_5]):
            if number_to_draw > 0:
                draw_x -= 8
                screen.blit(GRAPHICS[c.STAGE_5], (draw_x, h, 7, 16))
                number_to_draw -= 1
            else:
                return

        for n in range(self.stage_badges[c.STAGE_10]):
            if number_to_draw > 0:
                draw_x -= 14
                screen.blit(GRAPHICS[c.STAGE_10], (draw_x, h, 14, 16))
                number_to_draw -= 1
            else:
                return

        for n in range(self.stage_badges[c.STAGE_20]):
            if number_to_draw > 0:
                draw_x -= 16
                screen.blit(GRAPHICS[c.STAGE_20], (draw_x, h, 16, 16))
                number_to_draw -= 1
            else:
                return

        for n in range(self.stage_badges[c.STAGE_30]):
            if number_to_draw > 0:
                draw_x -= 16
                screen.blit(GRAPHICS[c.STAGE_30], (draw_x, h, 16, 16))
                number_to_draw -= 1
            else:
                return

        for n in range(self.stage_badges[c.STAGE_50]):
            if number_to_draw > 0:
                draw_x -= 16
                screen.blit(GRAPHICS[c.STAGE_50], (draw_x, h, 16, 16))
                number_to_draw -= 1
            else:
                return

    def show_state(self, screen):
        if self.is_starting:
            self.draw_mid_text(screen, c.START, pygame.Color("red"))
        elif self.should_show_stage:
            # pad the number to 3 digits
            self.draw_mid_text(screen, c.STAGE.format(self.stage_num), pygame.Color('skyblue'))
        elif self.should_show_ready:
            self.draw_mid_text(screen, c.READY, pygame.Color('red'))

    def update_player(self, dt, keys):
        if self.is_player_alive and self.can_control_player:
            self.player.update(dt, keys)
        if self.player.rect.left < self.bounds.left:
            self.player.rect.left = self.bounds.left
        elif self.player.rect.right > self.bounds.right:
            self.player.rect.right = self.bounds.right
