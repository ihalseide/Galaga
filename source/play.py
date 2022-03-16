import pygame
from pygame.math import Vector2
from . import constants as c, tools, setup, hud, scoring, sprites
from .setup import play_sound, stop_sounds
from .stars import StarField
from .tools import calc_stage_badges, draw_text
from .states import State, draw_mid_text

# Play state timings
STAGE_DURATION = 1600
READY_DURATION = 1600
INTRO_MUSIC_DURATION = 6600
START_NOISE_WAIT = 0
START_DURATION = START_NOISE_WAIT + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 200
FIRE_COOLDOWN = 200

# game area boundary
STAGE_BOUNDS = pygame.Rect(0, c.STAGE_TOP_Y, c.GAME_SIZE.width, c.STAGE_BOTTOM_Y - c.STAGE_TOP_Y)


class Play(State):

    def __init__(self, persist):
        # do the things all states must do...
        State.__init__(self, persist)

        # Setup stars
        self.persist.stars.moving = False

        # Score
        self.score = 0
        self.one_up_score = self.persist.one_up_score
        self.high_score = self.persist.high_score

        # init player
        self.is_player_alive = False
        self.player = None
        self.extra_lives = 3
        self.can_control_player = False
        self.last_fire_time = 0
        self.num_shots = 0
        self.num_hits = 0

        # init stage number and badge icons
        self.stage_num = 0
        self.num_badges = 0
        self.stage_badges = tools.calc_stage_badges(self.stage_num)
        self.is_animating_stage_badges = False
        self.stage_badge_animation_step = 0
        self.stage_badge_animation_timer = 0

        # missile sprites and such
        self.missiles = pygame.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()

        # Explosions sprites
        self.explosions = pygame.sprite.Group()

        # enemies and level
        self.formation_spread: int = 0
        self.formation_x_offset: int = 0
        self.formation_y_offset = c.STAGE_TOP_Y + 16
        self.the_stage = None
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()

        # timers:
        self.blocking_timer = 0  # this timer is for timing how long to show messages on screen
        self.flashing_text_timer = 0
        self.animation_beat_timer = 0
        self.animation_flag = False
        self.is_flashing_text = False
        self.show_1up_text = True

        # state
        self.is_starting = True
        self.has_started_intro_music = False
        self.should_show_ready = False
        self.should_show_stage = False
        self.should_spawn_enemies = False
        self.is_done_spawning_enemies = False
        self.is_ready = False
        self.should_reform_enemies = False
        self.should_show_game_over = False

    def cleanup(self):
        return c.Persist(stars=self.persist.stars,
                         scores=self.persist.scores,
                         current_score=self.score,
                         one_up_score=self.one_up_score,
                         high_score=self.high_score,
                         num_shots=self.num_shots,
                         num_hits=self.num_hits,
                         stage_num=self.stage_num)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            if keypress == pygame.K_SPACE and self.is_player_alive and self.can_control_player:
                if self.current_time >= (self.last_fire_time + FIRE_COOLDOWN):
                    self.fighter_shoots()
                    self.last_fire_time = self.current_time

            elif keypress == pygame.K_ESCAPE:
                # TODO: (DEBUG) skip things when [ESC] is pressed
                if not self.is_ready:
                    self.done_starting()
                    self.done_with_ready()
                    self.done_showing_stage()
                    stop_sounds()
                else:
                    quit()

            elif keypress == pygame.K_r:
                # TODO: (DEBUG) reset the state when [R] is pressed
                self.__init__(self.persist)

            elif keypress == pygame.K_k:
                # TODO: (DEBUG) kill the player when [K] is pressed
                self.kill_player()

    def fighter_shoots(self):
        play_sound('fighter_fire')
        # v is multiplied by speed in the missile class
        v = Vector2(0, -0.350)
        x = self.player.rect.centerx
        y = self.player.rect.top + 10
        m = sprites.Missile(x, y, v, is_enemy=False)
        self.missiles.add(m)
        self.num_shots += 1

    def play_intro_music(self):
        # Make the game play the intro music and wait
        stop_sounds()
        setup.get_sfx("theme").play()
        self.has_started_intro_music = True

    def animate_stage_badges(self, delta_time):
        if not self.is_animating_stage_badges:
            return

        if self.stage_badge_animation_step > self.num_badges:
            self.is_animating_stage_badges = False

        self.stage_badge_animation_timer += delta_time

        if (self.stage_badge_animation_timer >= STAGE_BADGE_DURATION) and (
                self.stage_badge_animation_step < self.num_badges):
            self.stage_badge_animation_step += 1
            self.stage_badge_animation_timer = 0
            play_sound('stage_award')

    def update(self, delta_time, keys):
        # More important things to update
        self.update_timers(delta_time)
        self.update_player(delta_time, keys)
        self.update_enemies(delta_time)

        # Less important graphical things to update
        self.update_text_sprites(delta_time)
        self.update_explosions(delta_time)
        self.update_stars(delta_time)
        self.animate_stage_badges(delta_time)
        self.update_missiles(delta_time)

    def update_enemies(self, delta_time):
        # update enemies
        if self.the_stage and self.enemies:
            self.enemies.update(delta_time, self.animation_flag)

    def add_explosion(self, x, y, is_player_type=False):
        self.explosions.add(sprites.Explosion(x, y, is_player_type=is_player_type))

    def update_missiles(self, delta_time):
        for a_missile in self.missiles.sprites():
            a_missile.update(delta_time, self.animation_flag)

            # Only work on the first enemy hit
            for enemy in self.enemies:
                if not enemy.is_visible:
                    continue
                if enemy.rect.colliderect(a_missile.rect):
                    enemy.kill()
                    a_missile.kill()
                    self.num_hits += 1
                    self.add_explosion(enemy.x, enemy.y)
                    play_sound("enemy_hit_1")
                    points = 0
                    if isinstance(enemy, sprites.Bee):
                        points = 400
                    elif isinstance(enemy, sprites.Butterfly):
                        points = 400
                    elif isinstance(enemy, sprites.Purple):
                        points = 800
                        sprites.ScoreText(enemy.x, enemy.y, points)
                    self.score += points
                    self.high_score = max(self.score, self.high_score)
                    if not STAGE_BOUNDS.contains(a_missile.rect):
                        a_missile.kill()
                    break

    def kill_player(self):
        if self.player is None or not self.is_player_alive:
            return
        play_sound("explosion")
        self.is_player_alive = False
        self.player.kill()
        self.add_explosion(self.player.x, self.player.y, is_player_type=True)
        self.reform_enemies()

    def reform_enemies(self):
        self.is_ready = False
        self.should_reform_enemies = True
        # TODO: fix
        self.done_reforming_enemies()

    def done_reforming_enemies(self):
        self.should_show_ready = True
        self.should_reform_enemies = False
        self.spawn_player()

    def decrement_lives(self):
        self.extra_lives -= 1

    def update_timers(self, delta_time: float):
        # the "blocking" timer that blocks stuff
        if self.is_starting:
            self.blocking_timer += delta_time
            if not self.has_started_intro_music:
                if self.blocking_timer >= START_NOISE_WAIT:
                    self.play_intro_music()
            if self.blocking_timer >= START_DURATION:
                self.done_starting()
        elif self.should_show_stage:
            self.blocking_timer += delta_time
            if self.blocking_timer >= STAGE_DURATION:
                self.done_showing_stage()
                self.show_ready()
        elif self.should_show_ready:
            self.blocking_timer += delta_time
            if self.blocking_timer >= READY_DURATION:
                self.done_with_ready()
        elif self.should_show_game_over:
            self.blocking_timer += delta_time
            if self.blocking_timer >= GAME_OVER_DURATION:
                self.done_showing_game_over()

        # The separate timer for synchronized animation of some things
        self.animation_beat_timer += delta_time
        if self.animation_beat_timer >= c.ENEMY_ANIMATION_FREQ:
            self.animation_beat_timer = 0
            self.animation_flag = not self.animation_flag

        # The separate timer for flashing the 1UP text
        if self.is_flashing_text:
            self.flashing_text_timer += delta_time
            if self.flashing_text_timer >= c.TEXT_FLASH_FREQ:
                self.flashing_text_timer = 0
                self.show_1up_text = not self.show_1up_text

    def show_ready(self):
        self.should_show_ready = True
        self.persist.stars.moving = 1

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
        self.stage_num = 0
        self.next_stage()
        self.should_show_stage = True
        self.is_flashing_text = True

    def next_stage(self):
        self.stage_num += 1

        # TODO: add enemies

        self.update_stage_badges()
        self.start_animating_stage_badges()

    def start_animating_stage_badges(self):
        self.is_animating_stage_badges = True
        self.stage_badge_animation_step = 0

    def update_stage_badges(self):
        self.stage_badges = tools.calc_stage_badges(self.stage_num)
        self.num_badges = sum(self.stage_badges)

    def spawn_player(self):
        if self.extra_lives == 0:
            self.show_game_over()
            return
        self.decrement_lives()
        self.is_player_alive = True
        self.player = sprites.Player(x=c.GAME_SIZE.width // 2, y=c.STAGE_BOTTOM_Y - 16)

    def show_game_over(self):
        self.should_show_game_over = True

    def done_showing_game_over(self):
        self.should_show_game_over = False
        self.is_done = True
        self.next_state_name = c.GAME_OVER_STATE

    def display(self, screen: pygame.Surface):
        # clear screen
        screen.fill(c.BLACK)
        # stars
        self.persist.stars.display(screen)
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
        # display text sprites
        for ts in sprites.ScoreText.text_sprites:
            ts.display(screen)
        # draw HUD
        self.show_state(screen)
        hud.display(screen, one_up_score=self.persist.one_up_score, high_score=self.persist.high_score,
                    offset_y=0, num_extra_lives=self.extra_lives, stage_badges=self.stage_badges,
                    stage_badge_animation_step=self.stage_badge_animation_step, show_1up=self.show_1up_text)

    def show_state(self, screen):
        if self.is_starting:
            draw_mid_text(screen, c.START_TEXT, c.RED)
        elif self.should_show_stage:
            # pad the number to 3 digits
            draw_mid_text(screen, c.STAGE_FORMAT_STR.format(self.stage_num), c.LIGHT_BLUE)
        elif self.should_show_ready:
            draw_mid_text(screen, c.READY, c.RED)
        elif self.should_show_game_over:
            draw_mid_text(screen, c.GAME_OVER_TEXT, c.RED)

    def update_player(self, dt, keys):
        e = 3
        if self.player and self.is_player_alive:
            if self.can_control_player:
                self.player.update(dt, keys)

            if self.player.rect.left < STAGE_BOUNDS.left:
                self.player.rect.left = STAGE_BOUNDS.left
            elif self.player.rect.right > STAGE_BOUNDS.right - e:
                self.player.rect.right = STAGE_BOUNDS.right - e

    def update_text_sprites(self, delta_time):
        # update score text things
        sprites.ScoreText.text_sprites.update(delta_time, self.animation_flag)

    def update_stars(self, delta_time):
        self.persist.stars.update(delta_time)

    def update_explosions(self, delta_time):
        self.explosions.update(delta_time, self.animation_flag)


