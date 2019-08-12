
from random import randint
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
)
from helpers import moveTo, randedge
import screen
from assets import objloader
from assets.paths import * # pylint: disable=unused-wildcard-import
from math import pi

def set_sprite(image_file, location, color=(255, 255, 255), size=None):
	surface = pg.image.load(image_file).convert()
	surface.set_colorkey(color, RLEACCEL)
	if size is not None:
		surface = pg.transform.scale(surface, size)
	rect = surface.get_rect(center=location)
	return (surface, rect)

class Player:
	def __init__(self):
		self.body = objloader.Obj(sedan_body_obj, object_vs, object_fs)
		self.glass = objloader.Obj(sedan_glass_obj, object_vs, object_fs)
		self.light = objloader.Obj(cube_obj, object_vs, object_fs)
		self.light.scale(0, 0, 0)
		self.light.translate(0, 0, -2)
		self.set_light_source(self.light)
		self.rotate(pi, 1, 0, 0)
		self.generate()
		self.scale(.0025, .0045, .0045)
		self.speed = .02
		self.bigtime = 0
		self.is_big = False
	def embiggen(self):
		self.scale(2, 2, 2)
		self.bigtime = 50
		self.is_big = True
	def generate(self):
		self.body.generate()
		self.glass.generate()
	def set_light_source(self, light):
		self.body.set_light_source(light)
		self.glass.set_light_source(light)
	def translate(self, x, y, z):
		self.body.translate(x, y, z)
		self.glass.translate(x, y, z)
	def rotate(self, angle, x, y, z):
		self.body.rotate(angle, x, y, z)
		self.glass.rotate(angle, x, y, z)
	def scale(self, x, y, z):
		self.body.scale(x, y, z)
		self.glass.scale(x, y, z)
	def draw(self):
		pressed_keys = pg.key.get_pressed()
		if pressed_keys[K_w] or pressed_keys[K_UP]: # pylint: disable=undefined-variable
			self.translate(0, self.speed, 0)
		if pressed_keys[K_s] or pressed_keys[K_DOWN]: # pylint: disable=undefined-variable
			self.translate(0, -self.speed, 0)
		if pressed_keys[K_a] or pressed_keys[K_LEFT]: # pylint: disable=undefined-variable
			self.translate(-self.speed, 0, 0)
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]: # pylint: disable=undefined-variable
			self.translate(self.speed, 0, 0)
		if self.bigtime <= 0 and self.is_big:
			self.scale(.5, .5, .5)
			self.is_big = False
		if self.body.box.lx < -1:
			self.translate(-1 - self.body.box.lx, 0, 0)
		if self.body.box.ux > 1:
			self.translate(1 - self.body.box.ux, 0, 0)
		if self.body.box.uy < -1:
			self.translate(0, -1 - self.body.box.uy, 0)
		if self.body.box.ly > 1:
			self.translate(0, 1 - self.body.box.ly, 0)
		self.bigtime -= 1 if self.bigtime > 0 else 0
		self.body.draw()
		self.glass.draw()

class PlayerBullet(objloader.Obj):
	def __init__(self, x, y, *groups):
		super().__init__(square_obj, object_vs, object_fs, bullet_png)
		self.generate()
		self.set_texture(1)
		self.translate(x, y, 0)
		self.scale(.005, .005, 1)
		self.speed = .06
		for group in groups:
			group.append(self)
	def draw(self):
		self.translate(self.speed, 0, 0)
		super().draw()

class Enemy(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(*groups)
		self.surface, self.rect = set_sprite(
			green_goblin_png,
			(screen.width, randint(25, screen.height - 25)),
			color=(255, 255, 255))
		self.speed = randint(5, 20)
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Splat(pg.sprite.Sprite):
	def __init__(self, x, y, *groups):
		super().__init__(*groups)
		self.surface, self.rect = set_sprite(Splat_png, (x, y))
		self.health = 300
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()

class Splat_Collect(pg.sprite.Sprite):
	def __init__(self, x, y, destination, *groups):
		super().__init__(*groups)
		self.surface, self.rect = set_sprite(Splat_png, (x, y))
		self.destination = destination
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.destination.center, 100))
		if self.rect.colliderect(self.destination):
			self.kill()

class Tornado(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(*groups)
		self.is_rainbow = True if randint(0, 10) > 8 else False
		self.image_file = rainbow_tornado_png if self.is_rainbow else tornado_png
		self.surface, self.rect = set_sprite(self.image_file, randedge(25, screen.width, screen.height))
		self.speed = randint(5, 8)
		self.__getWaypoint()
	def __getWaypoint(self):
		x = randint(screen.width // 4, 3 * screen.width // 4)
		y = randint(screen.height // 4, 3 * screen.height // 4)
		self.waypoint = moveTo(self.rect.center, [x, y], 3000)
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.waypoint, self.speed))

class Background(objloader.Obj):
	def __init__(self, image_file):
		super().__init__(square_obj, object_vs, object_fs, image_file)
		self.generate()
		self.set_texture(1)

class Hud_Button(pg.sprite.Sprite):
	def __init__(self, image_file, location, size, *groups):
		super().__init__(*groups)
		self.image_file = image_file
		self.location = location
		self.size = size
		self.surface, self.rect = set_sprite(self.image_file, self.location, size=self.size)
		self.is_hovering = False
	def rollover(self):
		over_x = self.rect.left < pg.mouse.get_pos()[0] < self.rect.right
		over_y = self.rect.top < pg.mouse.get_pos()[1] < self.rect.bottom
		return over_x and over_y
	def update(self):
		if self.rollover() and not self.is_hovering:
			rollover_size = (self.size[0] * 5 // 4, self.size[1] * 5 // 4)
			self.surface, self.rect = set_sprite(self.image_file, self.location, size=rollover_size)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.surface, self.rect = set_sprite(self.image_file, self.location, size=self.size)
			self.is_hovering = False
