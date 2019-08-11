
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_TAB, FULLSCREEN, OPENGL, DOUBLEBUF
)
from sprites import Background, Enemy, Player, PlayerBullet, Splat, Splat_Collect, Tornado, Hud_Button
import ui
import screen
from random import randint
from assets.paths import desert_road_png, treasure_png

class Game():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), FULLSCREEN|OPENGL|DOUBLEBUF) # pylint: disable=no-member

		self.ADDENEMY = pg.USEREVENT + 1 # pylint: disable=no-member
		pg.time.set_timer(self.ADDENEMY, randint(500, 750))
		self.NEWTORNADO = pg.USEREVENT + 2 # pylint: disable=no-member
		pg.time.set_timer(self.NEWTORNADO, randint(1000, 3500))

		self.enemies = pg.sprite.Group()
		self.splats = pg.sprite.Group()
		self.splats_collect = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.tornados = pg.sprite.Group()
		self.all_sprites = pg.sprite.Group()

		self.player = Player()

		self.background = Background(desert_road_png)
		loot_button_location = (screen.width // 20, screen.height * 11 // 12)
		loot_button_size = (screen.width // 19, screen.height // 12)
		self.loot_button = Hud_Button(treasure_png, loot_button_location, loot_button_size, self.all_sprites)

		self.splat_count = 0
		self.isRunning = True
	def play(self):
		while self.isRunning:

			# if pg.sprite.spritecollideany(self.player, self.enemies):
			# 	self.isRunning = False
			for enemy in pg.sprite.groupcollide(self.enemies, self.bullets, True, True):
				Splat(enemy.rect.centerx, enemy.rect.centery, (self.all_sprites, self.splats))
			# for splat in pg.sprite.spritecollide(self.player, self.splats, False):
			# 	self.splat_count += 1
			# 	Splat_Collect(*splat.rect.center, self.loot_button.rect, (self.all_sprites, self.splats_collect))
			# 	splat.kill()
			# for tornado in pg.sprite.spritecollide(self.player, self.tornados, False):
			# 	if tornado.is_rainbow:
			# 		self.player.embiggen()
			# 	else:
			# 		self.isRunning = False

			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.isRunning = False
				elif event.type == self.ADDENEMY:
					Enemy((self.all_sprites, self.enemies))
				elif event.type == self.NEWTORNADO:
					Tornado((self.all_sprites, self.tornados))
				elif event.type == KEYDOWN and event.key == K_SPACE:
					PlayerBullet(*self.player.body.box.mux, (self.all_sprites, self.bullets))
				elif (
					event.type == MOUSEBUTTONDOWN and self.loot_button.rollover() or
					(event.type == KEYDOWN and event.key == K_TAB)
				):
					loot = ui.Window('Loot', self.splat_count)
					loot.open()

			self.all_sprites.update()
			# self.view.blits([(splat.surface, splat.rect) for splat in self.splats])
			self.player.draw()
			# self.view.blits([(enemy.surface, enemy.rect) for enemy in self.enemies])
			# self.view.blits([(bullet.surface, bullet.rect) for bullet in self.bullets])
			# self.view.blits([(tornado.surface, tornado.rect) for tornado in self.tornados])
			# self.view.blits([(splat.surface, splat.rect) for splat in self.splats_collect])
			# self.view.blit(self.loot_button.surface, self.loot_button.rect)
			pg.display.flip()
			self.background.draw()
			self.clock.tick(60)
