
from random import randint
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
)
from helpers import moveTo, randedge
import screen
image_path = 'game art\\'

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surface = pg.image.load(image_path + 'car.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(0, screen.height // 2))
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
			self.surface = pg.image.load(image_path + 'car.png').convert()
			self.surface.set_colorkey((255, 255, 255), RLEACCEL)
			self.rect = self.surface.get_rect(center=(self.rect.center))
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > screen.width:
			self.rect.right = screen.width
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= screen.height:
			self.rect.bottom = screen.height
		self.bigtime -= 1 if self.bigtime > 0 else 0
	def embiggen(self):
		self.surface = pg.image.load(image_path + 'big car.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(self.rect.center))
		self.bigtime = 50

class PlayerBullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.surface = pg.image.load(image_path + 'bullet.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(x, y))
		self.speed = 30
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.right > screen.width:
			self.kill()

class Enemy(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surface = pg.image.load(image_path + 'green goblin.png').convert()
		self.surface.set_colorkey((255, 0, 0), RLEACCEL)
		self.rect = self.surface.get_rect(center=(screen.width, randint(25, screen.height - 25)))
		self.speed = randint(5, 20)
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Splat(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.surface = pg.image.load(image_path + 'Splat.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(x, y))
		self.health = 300
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()

class Splat_Collect(pg.sprite.Sprite):
	def __init__(self, x, y, destination):
		super().__init__()
		self.surface = pg.image.load(image_path + 'Splat.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(x, y))
		self.destination = destination
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.destination.center, 100))
		if self.rect.colliderect(self.destination):
			self.kill()

class Tornado(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.magic = randint(0, 10)
		self.surface = pg.image.load(image_path + ('tornado.png' if self.magic < 8 else 'rainbow_tornado.png')).convert()
		self.surface.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.surface.get_rect(center=(randedge(25, screen.width, screen.height)))
		self.speed = randint(5, 8)
		self.waypoint = []
		self.__getWaypoint()
	def __getWaypoint(self):
		x = randint(screen.width // 4, 3 * screen.width // 4)
		y = randint(screen.height // 4, 3 * screen.height // 4)
		self.waypoint = moveTo(self.rect.center, [x, y], 3000)
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.waypoint, self.speed))

class Background(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		super().__init__()
		self.surface = pg.transform.scale(pg.image.load(image_path + image_file), (screen.width, screen.height))
		self.rect = self.surface.get_rect()
		self.rect.left, self.rect.top = location

class Hud_Button(pg.sprite.Sprite):
	def __init__(self, image_file, location, size):
		super().__init__()
		self.surface = pg.image.load(image_path + image_file).convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.surface = pg.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect()
		self.image_file = image_file
		self.location, self.rect.topleft = location, location
		self.size = size
		self.is_hovering = False
	def rollover(self):
		over_x = self.rect.left < pg.mouse.get_pos()[0] < self.rect.right
		over_y = self.rect.top < pg.mouse.get_pos()[1] < self.rect.bottom
		return over_x and over_y
	def update(self):
		if self.rollover() and not self.is_hovering:
			rollover_size = (self.size[0] * 5 // 4, self.size[1] * 5 // 4)
			self.surface = pg.image.load(image_path + self.image_file).convert()
			self.surface.set_colorkey((255, 255, 255), RLEACCEL)
			self.surface = pg.transform.scale(self.surface, rollover_size)
			self.rect.move_ip(self.rect.width // 10, -self.rect.height // 5)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.surface = pg.image.load(image_path + self.image_file).convert()
			self.surface.set_colorkey((255, 255, 255), RLEACCEL)
			self.surface = pg.transform.scale(self.surface, self.size)
			self.rect.topleft = self.location
			self.is_hovering = False
