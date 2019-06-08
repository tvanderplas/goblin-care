
import pygame as pg
import pygame.freetype as ft
# pylint: disable=no-name-in-module
from pygame.constants import (
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE
)# pylint: enable=no-name-in-module
from random import randint
from sprites import Background, Enemy, Player, PlayerBullet, Splat, Tornado, Menu_Button
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

def game():
	player = Player()
	all_sprites.add(player)
	isRunning = True
	while isRunning:

		if pg.sprite.spritecollideany(player, enemies):
			for sprite in all_sprites:
				sprite.kill()
			isRunning = False
		for enemy in pg.sprite.groupcollide(enemies, bullets, True, True):
			new_splat = Splat(enemy.rect.centerx, enemy.rect.centery)
			all_sprites.add(new_splat)
			splats.add(new_splat)
		for tornado in pg.sprite.spritecollide(player, tornados, False):
			if tornado.magic < 8:
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			else:
				player.embiggen()

		for event in pg.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			elif event.type == ADDENEMY:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)
			elif event.type == NEWTORNADO:
				new_tornado = Tornado()
				tornados.add(new_tornado)
				all_sprites.add(new_tornado)
			elif event.type == KEYDOWN and event.key == K_SPACE:
				new_player_bullet = PlayerBullet(player.rect.right, player.rect.centery)
				all_sprites.add(new_player_bullet)
				bullets.add(new_player_bullet)

		for sprite in all_sprites:
			sprite.update()
		for splat in splats:
			view.blit(splat.surface, splat.rect)
		view.blit(player.surface, player.rect)
		for enemy in enemies:
			view.blit(enemy.surface, enemy.rect)
		for bullet in bullets:
			view.blit(bullet.surface, bullet.rect)
		for tornado in tornados:
			view.blit(tornado.surface, tornado.rect)
		pg.display.flip()
		view.blit(background.surface, background.rect)
		clock.tick(60)

menu_screen = Background('menu.png', [0, 0])
play_button = Menu_Button('Play!', (-screen.width // 5, screen.height // 2))
quit_button = Menu_Button('Quit', (-screen.width // 5, screen.height * 3 // 5))

while True:
	for event in pg.event.get():
		if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
			raise SystemExit
		if event.type == MOUSEBUTTONDOWN:
			if pg.mouse.get_pos()[0] < screen.width // 2:
				game()
			elif pg.mouse.get_pos()[0] >= screen.width // 2:
				raise SystemExit
	pg.display.flip()
	menu_screen.surface.blit(play_button.surface, play_button.rect)
	menu_screen.surface.blit(quit_button.surface, quit_button.rect)
	view.blit(menu_screen.surface, menu_screen.rect)
	clock.tick(15)
