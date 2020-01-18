#!/usr/bin/env python3
# play_state.py

import pygame
from pygame.math import Vector2

from .state import _State
from .. import constants as c
from .. import setup
from .. import tools
from ..components import missile, player, stars, hud

# Where the game area really starts and ends vertically to fit the HUD
STAGE_TOP = 30
STAGE_BOTTOM = c.GAME_HEIGHT - 20
# sprite resources
GRAPHICS = {
	c.LIFE: tools.grab_sheet(96, 0, 16, 16),
	c.STAGE_1:  tools.grab_sheet(208, 48,  7, 16),
	c.STAGE_5:  tools.grab_sheet(192, 48,  7, 16),
	c.STAGE_10: tools.grab_sheet(176, 48, 14, 16),
	c.STAGE_20: tools.grab_sheet(160, 48, 15, 16),
	c.STAGE_30: tools.grab_sheet(144, 48, 16, 16),
	c.STAGE_50: tools.grab_sheet(128, 48, 16, 16),
}
# Timing (in seconds)
STAGE_DURATION = 1.6
READY_DURATION = 1.6
TRANSITION_DURATION = 0.45
NEW_ENEMY_WAIT = 0.3
NEW_WAVE_WAIT = 1
START_NOISE_DURATION = 1
INTRO_MUSIC_DURATION = 6.6
START_DURATION = START_NOISE_DURATION + INTRO_MUSIC_DURATION
STAGE_BADGE_DURATION = 0.15


def _draw_mid_text(screen, text, color, location=(c.GAME_CENTER_X, c.GAME_CENTER_Y)):
	tools.draw_text(screen, text, location, color, (0, 0, 0), centered_x=True, centered_y=True)


def _make_no_stages() -> dict:
	# 0 of each stage badge
	return {c.STAGE_1: 0, c.STAGE_5: 0, c.STAGE_10: 0, c.STAGE_20: 0, c.STAGE_30: 0, c.STAGE_50: 0}


def _calc_stage_badges(stage_num: int) -> dict:
	"""
	Calculate how many of each stage badges there are for a given stage
	"""
	if stage_num <= 0:
		return _make_no_stages()
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
		return {c.STAGE_1: num_1, c.STAGE_5: num_5, c.STAGE_10: num_10, c.STAGE_20: num_20, c.STAGE_30: num_30,
				c.STAGE_50: num_50}


class Play(_State):
	def __init__(self, persist=None):
		# do the things all states must do...
		_State.__init__(self, persist)
		self.next = c.PLAY_STATS
		self.current_time = 0
		# TODO: load scores?
		self._init_hud()
		self._init_stage_badges()
		# star background
		self._init_stars()
		# sprites
		self.missiles = pygame.sprite.Group()
		self.enemy_missiles = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		# player/fighter
		self._init_player()
		# game area boundary
		self.bounds = pygame.Rect(0, STAGE_TOP, c.GAME_WIDTH, STAGE_BOTTOM - STAGE_TOP)
		# sound
		self.intro_duration = START_DURATION
		# timers
		self.start_timer = 0
		self.is_starting = True
		self.should_play_start_noise = True
		self.should_play_intro_music = False
		self.has_started_intro_music = False

	def _init_stars(self):
		maybe_stars = self.persist.get(c.STARS)
		self.stars = maybe_stars if maybe_stars else stars.Stars()
		self.stars.set_moving(False)

	def _init_hud(self):
		maybe_hud = self.persist.get(c.HUD)
		self.hud = maybe_hud if maybe_hud else hud.Hud(0, 30000)

	def _init_player(self):
		self.is_player_alive = False
		self.player = player.Player()
		self.extra_lives = 3

	def _init_stage_badges(self):
		self.stage_num = 0
		self.num_badges = 0
		self.stage_badges = _calc_stage_badges(self.stage_num)
		self.is_animating_stage_badges = False
		self.stage_badge_animation_step = 0
		self.stage_badge_animation_timer = 0
		self.should_play_badge_noise = False

	def cleanup(self):
		return self.persist

	def get_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if self.is_player_alive:
					self.player_fire(self.player)

	def play_start_noise(self):
		setup.SFX['start_noise'].play()
		self.should_play_start_noise = False

	def play_intro_music(self):
		setup.SFX["theme"].play()
		self.has_started_intro_music = True
		self.should_play_intro_music = False

	def animate_stage_badges(self, dt):
		if not self.is_animating_stage_badges:
			return

		if self.stage_badge_animation_step > self.num_badges:
			self.is_animating_stage_badges = False

		self.stage_badge_animation_timer += dt

		if self.stage_badge_animation_timer >= STAGE_BADGE_DURATION and self.stage_badge_animation_step < self.num_badges:
			self.stage_badge_animation_step += 1
			self.stage_badge_animation_timer = 0
			self.should_play_badge_noise = True

	def play_badge_noise(self):
		setup.SFX['stage_award'].play()
		self.should_play_badge_noise = False

	def update(self, dt, keys):
		_State.update(self, dt, keys)
		if self.should_play_start_noise:
			self.play_start_noise()
		if self.should_play_intro_music:
			self.play_intro_music()
		if self.should_play_badge_noise:
			self.play_badge_noise()
		self.animate_stage_badges(dt)
		self.current_time += dt
		self.stars.update(dt)
		self.update_timers(dt)
		if self.is_player_alive:
			self.update_player(dt, keys)

	def decrement_lives(self):
		self.extra_lives -= 1

	def update_timers(self, dt: float):
		if self.is_starting:
			self.start_timer += dt
			if not self.has_started_intro_music:
				if self.start_timer >= START_NOISE_DURATION:
					self.should_play_intro_music = True
			if self.start_timer >= self.intro_duration:
				self.done_starting()

	def done_starting(self):
		self.is_starting = False
		self.start_timer = 0
		self.spawn_player()
		self.decrement_lives()
		self.stage_num = 0
		self.next_stage()

	def next_stage(self):
		self.stage_num += 1
		self.update_stage_badges()
		self.start_animating_stage_badges()

	def start_animating_stage_badges(self):
		self.is_animating_stage_badges = True
		self.stage_badge_animation_step = 0

	def update_stage_badges(self):
		self.stage_badges = _calc_stage_badges(self.stage_num)
		self.num_badges = sum(self.stage_badges.values())

	def spawn_player(self):
		self.is_player_alive = True
		self.player = player.Player()

	def display(self, screen, dt):
		# clear screen
		screen.fill((0, 0, 0))
		# stars
		self.stars.display(screen)
		# draw enemies
		# draw player
		if self.is_player_alive:
			self.player.display(screen)
		# draw bullets
		# draw HUD
		self.draw_hud(screen, dt)

	# pygame.draw.rect(screen, (255,255,255), self.bounds, 1)

	def draw_lives(self, screen):
		# lives
		for i in range(self.extra_lives):
			screen.blit(GRAPHICS['life'], (3 + i * 16, STAGE_BOTTOM + 1, 16, 16))

	def draw_hud(self, screen, dt):
		# call external hud
		self.hud.display(screen)
		# clear spot for lives and stages
		screen.fill(pygame.Color('black'), (0, STAGE_BOTTOM, c.GAME_WIDTH, c.GAME_HEIGHT - STAGE_BOTTOM))
		self.draw_lives(screen)
		# stage badges
		self.draw_stage_badges(screen)
		# draw middle message
		self.show_state(screen)

	def draw_stage_badges(self, screen):
		# draw the stage level badges
		draw_x = c.GAME_WIDTH
		h = c.GAME_HEIGHT - 20
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
			_draw_mid_text(screen, "START", pygame.Color("red"))

	def player_fire(self, a_player):
		if a_player.can_fire(self.current_time):
			setup.SFX["fighter_fire"].play()
			# v is multiplied by speed in the missile class
			# noinspection PyArgumentList
			v = Vector2(0, -1)
			x = a_player.rect.centerx
			y = a_player.rect.top + 10
			m = missile.Missile((x, y), v, is_enemy=False)
			a_player.last_fire_time = self.current_time
			self.missiles.add(m)

	def update_player(self, dt, keys):
		self.player.update(dt, keys)
		if self.player.rect.left < self.bounds.left:
			self.player.rect.left = self.bounds.left
		elif self.player.rect.right > self.bounds.right:
			self.player.rect.right = self.bounds.right
