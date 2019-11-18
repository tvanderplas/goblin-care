
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_TAB, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d
)
from OpenGL.GL import glClear, glEnable, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST
from sprites import Background, Enemy, Player, PlayerBullet, Rainbow_Bullet, Splat, Splat_Collect, Tornado, Hud_Button
import ui
from random import randint
from assets.paths import desert_road_png, treasure_png
from helpers import group_collide, collide_any, get_collided

class Game():
	def __init__(self, view):
		self.clock = pg.time.Clock()
		self.view = view
		glEnable(GL_DEPTH_TEST)

		self.ADDENEMY = pg.USEREVENT + 1 # pylint: disable=no-member
		pg.time.set_timer(self.ADDENEMY, randint(500, 750))
		self.NEWTORNADO = pg.USEREVENT + 2 # pylint: disable=no-member
		pg.time.set_timer(self.NEWTORNADO, randint(5000, 20000))

		self.enemies = []
		self.splats = []
		self.splats_collect = []
		self.bullets = []
		self.pierce_bullets = []
		self.tornados = []
		self.all_sprites = []
		self.player = Player()
		self.splat_count = [0]

		self.background = Background(desert_road_png)
		self.loot_button = Hud_Button(treasure_png, (-.85, -.8), (self.all_sprites,))
		self.loot = ui.Loot_Screen('Loot', self.splat_count, self.view, self.player)
		self.loot.paint_select[0].active = True
		self.loot.paint_select[0].owned = True

		self.isRunning = True
	def collect(self, splat):
		self.splat_count[0] += 1
		Splat_Collect(splat.box.muz[:2], (-.85, -.8), (self.all_sprites, self.splats_collect))
		splat.kill()
	def play(self):
		while self.isRunning:

			# collisions
			if collide_any(self.player, self.enemies):
				self.isRunning = False
			get_collided(self.loot_button, self.splats_collect, False, True)
			for enemy in group_collide(self.enemies, self.bullets, True, True):
				Splat(enemy.box.muz[:2], (self.all_sprites, self.splats))
			for enemy in group_collide(self.enemies, self.pierce_bullets, True, False):
				Splat(enemy.box.muz[:2], (self.all_sprites, self.splats))
			for splat in get_collided(self.player, self.splats):
				self.collect(splat)
			for tornado in get_collided(self.player, self.tornados):
				if tornado.is_rainbow:
					self.player.embiggen()
					for splat in self.splats:
						self.collect(splat)
				else:
					self.isRunning = False

			# input
			pressed_keys = pg.key.get_pressed()
			if pressed_keys[K_w] or pressed_keys[K_UP]: # pylint: disable=undefined-variable
				self.player.translate(0, self.player.speed, 0)
			if pressed_keys[K_s] or pressed_keys[K_DOWN]: # pylint: disable=undefined-variable
				self.player.translate(0, -self.player.speed, 0)
			if pressed_keys[K_a] or pressed_keys[K_LEFT]: # pylint: disable=undefined-variable
				self.player.translate(-self.player.speed, 0, 0)
			if pressed_keys[K_d] or pressed_keys[K_RIGHT]: # pylint: disable=undefined-variable
				self.player.translate(self.player.speed, 0, 0)

			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.isRunning = False
				if event.type == self.ADDENEMY:
					Enemy((self.all_sprites, self.enemies))
				if event.type == self.NEWTORNADO:
					Tornado((self.all_sprites, self.tornados))
				if event.type == KEYDOWN and event.key == K_SPACE:
					if self.player.is_big:
						Rainbow_Bullet(*self.player.box.mux[:2], (self.all_sprites, self.pierce_bullets))
					else:
						PlayerBullet(*self.player.box.mux[:2], (self.all_sprites, self.bullets))
				if (
					event.type == MOUSEBUTTONDOWN and self.loot_button.rollover() or
					(event.type == KEYDOWN and event.key == K_TAB)
				):
					self.loot.open()

			# draw frame
			self.player.draw()
			for sprite in self.all_sprites:
				sprite.draw()
			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.background.draw()
			self.clock.tick(60)
