
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_TAB
)
from sprites import Background, Enemy, Player, PlayerBullet, Splat, Splat_Collect, Tornado, Hud_Button
import ui
import screen
from random import randint

class Game():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN) # pylint: disable=no-member
		self.ADDENEMY = pg.USEREVENT + 1 # pylint: disable=no-member
		self.NEWTORNADO = pg.USEREVENT + 2 # pylint: disable=no-member

		pg.time.set_timer(self.ADDENEMY, randint(500, 750))
		pg.time.set_timer(self.NEWTORNADO, randint(250, 3500))

		self.enemies = pg.sprite.Group()
		self.splats = pg.sprite.Group()
		self.splats_collect = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.tornados = pg.sprite.Group()
		self.all_sprites = pg.sprite.Group()

		self.player = Player()
		self.all_sprites.add(self.player)

		self.background = Background('desert road.png', [0, 0])
		inv_button_location = (screen.width // 100, screen.height * 9 // 10)
		inv_button_size = (screen.width // 19, screen.height // 12)
		self.inv_button = Hud_Button('treasure.png', inv_button_location, inv_button_size)
		self.all_sprites.add(self.inv_button)

		self.splat_count = 0
		self.isRunning = True
	def play(self):
		while self.isRunning:

			if pg.sprite.spritecollideany(self.player, self.enemies):
				self.all_sprites.empty()
				self.isRunning = False
			for enemy in pg.sprite.groupcollide(self.enemies, self.bullets, True, True):
				new_splat = Splat(enemy.rect.centerx, enemy.rect.centery)
				self.all_sprites.add(new_splat)
				self.splats.add(new_splat)
			for splat in pg.sprite.spritecollide(self.player, self.splats, False):
				self.splat_count += 1
				collect = Splat_Collect(*splat.rect.center, self.inv_button.rect)
				self.splats_collect.add(collect)
				self.all_sprites.add(collect)
				splat.kill()
			for tornado in pg.sprite.spritecollide(self.player, self.tornados, False):
				if tornado.magic < 8:
					self.all_sprites.empty()
					self.isRunning = False
				else:
					self.player.embiggen()

			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.all_sprites.empty()
					self.isRunning = False
				elif event.type == self.ADDENEMY:
					new_enemy = Enemy()
					self.enemies.add(new_enemy)
					self.all_sprites.add(new_enemy)
				elif event.type == self.NEWTORNADO:
					new_tornado = Tornado()
					self.tornados.add(new_tornado)
					self.all_sprites.add(new_tornado)
				elif event.type == KEYDOWN and event.key == K_SPACE:
					new_player_bullet = PlayerBullet(self.player.rect.right, self.player.rect.centery)
					self.all_sprites.add(new_player_bullet)
					self.bullets.add(new_player_bullet)
				elif (
					event.type == MOUSEBUTTONDOWN and self.inv_button.rollover() or
					(event.type == KEYDOWN and event.key == K_TAB)
				):
					loot = ui.Window('Loot', self.splat_count)
					loot.open()

			self.all_sprites.update()
			self.view.blits([(splat.surface, splat.rect) for splat in self.splats])
			self.view.blit(self.player.surface, self.player.rect)
			self.view.blits([(enemy.surface, enemy.rect) for enemy in self.enemies])
			self.view.blits([(bullet.surface, bullet.rect) for bullet in self.bullets])
			self.view.blits([(tornado.surface, tornado.rect) for tornado in self.tornados])
			self.view.blits([(splat.surface, splat.rect) for splat in self.splats_collect])
			self.view.blit(self.inv_button.surface, self.inv_button.rect)
			pg.display.flip()
			self.view.blit(self.background.surface, self.background.rect)
			self.clock.tick(60)
