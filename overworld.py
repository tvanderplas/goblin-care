
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_TAB
)
from OpenGL.GL import glClear, glEnable, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST
from sprites import Background, Enemy, Player, PlayerBullet, Splat, Splat_Collect, Tornado, Hud_Button
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
		self.tornados = []
		self.all_sprites = []
		self.player = Player()
		self.splat_count = [0]

		self.background = Background(desert_road_png)
		self.loot_button = Hud_Button(treasure_png, (-.85, -.8))
		self.loot = ui.Window('Loot', self.splat_count, self.view, self.player)
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
			if collide_any(self.player.body, self.enemies):
				self.isRunning = False
			for enemy in group_collide(self.enemies, self.bullets, True, True):
				Splat(enemy.box.muz[:2], (self.all_sprites, self.splats))
			for splat in get_collided(self.player.body, self.splats):
				self.collect(splat)
			for tornado in get_collided(self.player.body, self.tornados):
				if tornado.is_rainbow:
					self.player.embiggen()
					for splat in self.splats:
						self.collect(splat)
				else:
					self.isRunning = False

			# input
			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.isRunning = False
				if event.type == self.ADDENEMY:
					Enemy((self.all_sprites, self.enemies))
				if event.type == self.NEWTORNADO:
					Tornado((self.all_sprites, self.tornados))
				if event.type == KEYDOWN and event.key == K_SPACE:
					PlayerBullet(*self.player.body.box.mux[:2], (self.bullets))
				if (
					event.type == MOUSEBUTTONDOWN and self.loot_button.rollover() or
					(event.type == KEYDOWN and event.key == K_TAB)
				):
					self.loot.open()

			# draw frame
			for splat in self.splats:
				splat.draw()
			for splat in self.splats_collect:
				splat.draw()
			self.player.draw()
			self.loot_button.draw()
			for bullet in self.bullets:
				bullet.draw()
			for enemy in self.enemies:
				enemy.draw()
			for tornado in self.tornados:
				tornado.draw()
			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.background.draw()
			self.clock.tick(60)
