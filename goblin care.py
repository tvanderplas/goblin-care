
import pygame as pg
import pygame.freetype as ft
# pylint: disable=no-name-in-module
from pygame.constants import (
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE
)# pylint: enable=no-name-in-module
from random import randint
from sprites import Background, Enemy, Player, PlayerBullet, Splat, Tornado, Menu_Button, Game_UI_Button
import screen

# pylint: disable=no-member
pg.init()
clock = pg.time.Clock()
view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN)

background = Background('desert road.png', [0, 0])
ADDENEMY = pg.USEREVENT + 1
NEWTORNADO = pg.USEREVENT + 2
pg.time.set_timer(ADDENEMY, randint(500, 750))
pg.time.set_timer(NEWTORNADO, randint(250, 3500))
enemies = pg.sprite.Group()
splats = pg.sprite.Group()
bullets = pg.sprite.Group()
tornados = pg.sprite.Group()
all_sprites = pg.sprite.Group()
# pylint: enable=no-member

class Game():
	def __init__(self):
		self.player = Player()
		all_sprites.add(self.player)

		inv_button_location = (screen.width // 100, screen.height * 9 // 10)
		inv_button_size = (screen.width // 19, screen.height // 12)
		self.inv_button = Game_UI_Button('treasure.png', inv_button_location, inv_button_size)
		all_sprites.add(self.inv_button)

		self.isRunning = True
	def play(self):
		while self.isRunning:

			if pg.sprite.spritecollideany(self.player, enemies):
				for sprite in all_sprites:
					sprite.kill()
				self.isRunning = False
			for enemy in pg.sprite.groupcollide(enemies, bullets, True, True):
				new_splat = Splat(enemy.rect.centerx, enemy.rect.centery)
				all_sprites.add(new_splat)
				splats.add(new_splat)
			for tornado in pg.sprite.spritecollide(self.player, tornados, False):
				if tornado.magic < 8:
					for sprite in all_sprites:
						sprite.kill()
					self.isRunning = False
				else:
					self.player.embiggen()

			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					for sprite in all_sprites:
						sprite.kill()
					self.isRunning = False
				elif event.type == ADDENEMY:
					new_enemy = Enemy()
					enemies.add(new_enemy)
					all_sprites.add(new_enemy)
				elif event.type == NEWTORNADO:
					new_tornado = Tornado()
					tornados.add(new_tornado)
					all_sprites.add(new_tornado)
				elif event.type == KEYDOWN and event.key == K_SPACE:
					new_player_bullet = PlayerBullet(self.player.rect.right, self.player.rect.centery)
					all_sprites.add(new_player_bullet)
					bullets.add(new_player_bullet)

			for sprite in all_sprites:
				sprite.update()
			for splat in splats:
				view.blit(splat.surface, splat.rect)
			view.blit(self.player.surface, self.player.rect)
			for enemy in enemies:
				view.blit(enemy.surface, enemy.rect)
			for bullet in bullets:
				view.blit(bullet.surface, bullet.rect)
			for tornado in tornados:
				view.blit(tornado.surface, tornado.rect)
			view.blit(self.inv_button.surface, self.inv_button.rect)
			pg.display.flip()
			view.blit(background.surface, background.rect)
			clock.tick(60)

menu_screen = Background('menu.png', [0, 0])
play_button = Menu_Button('Play!', (-screen.width // 5, screen.height // 2))
quit_button = Menu_Button('Quit', (-screen.width // 5, screen.height * 3 // 5))

while True:
	play_button.hover()
	quit_button.hover()
	for event in pg.event.get():
		if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
			raise SystemExit
		if event.type == MOUSEBUTTONDOWN:
			if play_button.rollover():
				game = Game()
				game.play()
			elif quit_button.rollover():
				raise SystemExit
	pg.display.flip()
	view.blit(menu_screen.surface, menu_screen.rect)
	view.blit(play_button.surface, play_button.rect)
	view.blit(quit_button.surface, quit_button.rect)
	clock.tick(60)
