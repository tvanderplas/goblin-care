
from random import randint
import pygame as pg
# pylint: disable=no-name-in-module
from pygame.constants import (
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
)# pylint: enable=no-name-in-module
from helpers import moveTo, randedge
image_path = 'game art\\'

class Player(pg.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.image = pg.image.load(image_path + 'car.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(0, pg.display.Info().current_h // 2))
		self.speed = 10
		self.bigtime = 0
	def update(self):
		pressed_keys = pg.key.get_pressed()
		if pressed_keys[K_w] or pressed_keys[K_UP]:
			self.rect.move_ip(0, -self.speed)
		if pressed_keys[K_s] or pressed_keys[K_DOWN]:
			self.rect.move_ip(0, self.speed)
		if pressed_keys[K_a] or pressed_keys[K_LEFT]:
			self.rect.move_ip(-self.speed, 0)
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
			self.rect.move_ip(self.speed, 0)
		if self.bigtime <= 0:
			self.image = pg.image.load(image_path + 'car.png').convert()
			self.image.set_colorkey((255, 255, 255), RLEACCEL)
			self.rect = self.image.get_rect(center=(self.rect.center))
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > pg.display.Info().current_w:
			self.rect.right = pg.display.Info().current_w
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= pg.display.Info().current_h:
			self.rect.bottom = pg.display.Info().current_h
		self.bigtime -= 1 if self.bigtime > 0 else 0
	def embiggen(self):
		self.image = pg.image.load(image_path + 'big car.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(self.rect.center))
		self.bigtime = 50

class PlayerBullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		super(PlayerBullet, self).__init__()
		self.image = pg.image.load(image_path + 'bullet.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(x, y))
		self.speed = 30
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.right > pg.display.Info().current_w:
			self.kill()

class Enemy(pg.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.image = pg.image.load(image_path + 'green goblin.png').convert()
		self.image.set_colorkey((255, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center=(pg.display.Info().current_w, randint(25, pg.display.Info().current_h - 25)))
		self.speed = randint(5, 20)
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Splat(pg.sprite.Sprite):
	def __init__(self, x, y):
		super(Splat, self).__init__()
		self.image = pg.image.load(image_path + 'Splat.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(x, y))
		self.health = 300
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()

class Tornado(pg.sprite.Sprite):
	def __init__(self):
		super(Tornado, self).__init__()
		self.magic = randint(0, 10)
		self.image = pg.image.load(image_path + ('tornado.png' if self.magic < 8 else 'rainbow_tornado.png')).convert()
		self.image.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center=(randedge(25)))
		self.speed = randint(5, 8)
		self.waypoint = []
		self.__getWaypoint()
	def __getWaypoint(self):
		x = randint(pg.display.Info().current_w // 4, 3 * pg.display.Info().current_w // 4)
		y = randint(pg.display.Info().current_h // 4, 3 * pg.display.Info().current_h // 4)
		self.waypoint = moveTo(self.rect.center, [x, y], 3000)
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.waypoint, self.speed))

class Background(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(pg.image.load(image_file), (pg.display.Info().current_w, pg.display.Info().current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
