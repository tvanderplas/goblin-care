
from random import random, uniform
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
)
from helpers import randedge, pixel_to_view, get_vector
from assets import objloader
from assets.paths import * # pylint: disable=unused-wildcard-import
from math import pi

class Player:
	def __init__(self):
		self.body = objloader.Obj(sedan_body_obj, object_vs, object_fs)
		self.glass = objloader.Obj(sedan_glass_obj, object_vs, object_fs)
		self.wheels = objloader.Obj(sedan_wheels_obj, object_vs, object_fs)
		self.tires = objloader.Obj(sedan_tires_obj, object_vs, object_fs)
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
		if not self.is_big:
			self.scale(1.5, 1.5, 1.5)
			self.bigtime = 150
			self.is_big = True
	def generate(self):
		self.body.generate()
		self.glass.generate()
		self.wheels.generate()
		self.tires.generate()
	def set_light_source(self, light):
		self.body.set_light_source(light)
		self.glass.set_light_source(light)
		self.wheels.set_light_source(light)
		self.tires.set_light_source(light)
	def translate(self, x, y, z):
		self.body.translate(x, y, z)
		self.glass.translate(x, y, z)
		self.wheels.translate(x, y, z)
		self.tires.translate(x, y, z)
	def rotate(self, angle, x, y, z):
		self.body.rotate(angle, x, y, z)
		self.glass.rotate(angle, x, y, z)
		self.wheels.rotate(angle, x, y, z)
		self.tires.rotate(angle, x, y, z)
	def scale(self, x, y, z):
		self.body.scale(x, y, z)
		self.glass.scale(x, y, z)
		self.wheels.scale(x, y, z)
		self.tires.scale(x, y, z)
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
			self.scale(2/3, 2/3, 2/3)
			self.is_big = False
		if self.body.box.lx < -1:
			self.translate(-1 - self.body.box.lx, 0, 0)
		if self.body.box.ux > 1:
			self.translate(1 - self.body.box.ux, 0, 0)
		if self.body.box.ly < -1:
			self.translate(0, -1 - self.body.box.ly, 0)
		if self.body.box.uy > 1:
			self.translate(0, 1 - self.body.box.uy, 0)
		self.bigtime -= 1 if self.bigtime > 0 else 0
		self.body.draw()
		self.glass.draw()
		self.wheels.draw()
		self.tires.draw()

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
		self.groups = groups
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def update(self):
		self.translate(self.speed, 0, 0)
		if self.box.lx > 1:
			self.kill()
	def draw(self):
		self.update()
		super().draw()

class Enemy(objloader.Obj):
	def __init__(self, groups):
		super().__init__(square_obj, object_vs, object_fs, green_goblin_png)
		self.generate()
		self.set_texture(1)
		height = uniform(-.9, .9)
		self.translate(1, height, 0)
		self.scale(.04, .06, 1)
		self.speed = uniform(.001, .005)
		for group in groups:
			group.append(self)
		self.groups = groups
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def update(self):
		self.translate(-self.speed, 0, 0)
		if self.box.ux < -1:
			self.kill()
	def draw(self):
		self.update()
		super().draw()

class Splat(objloader.Obj):
	def __init__(self, location, groups):
		super().__init__(square_obj, object_vs, object_fs, splat_png)
		self.generate()
		self.set_texture(1)
		self.translate(*location, 0)
		self.scale(.04, .06, 1)
		self.health = 600
		for group in groups:
			group.append(self)
		self.groups = groups
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()
	def draw(self):
		self.update()
		super().draw()

class Splat_Collect(objloader.Obj):
	def __init__(self, location, destination, groups):
		super().__init__(square_obj, object_vs, object_fs, splat_png)
		self.generate()
		self.set_texture(1)
		self.translate(*location, 0)
		self.scale(.04, .06, 1)
		self.destination = destination
		self.vector = get_vector(.1, *destination, *location)
		for group in groups:
			group.append(self)
		self.groups = groups
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def update(self):
		if self.box.lx < self.destination[0] and self.box.ly < self.destination[1]:
			self.kill()
		self.translate(*self.vector, 0)
	def draw(self):
		self.update()
		super().draw()


class Tornado(objloader.Obj):
	def __init__(self, groups):
		self.is_rainbow = True if random() > .9 else False
		self.image_file = rainbow_tornado_png if self.is_rainbow else tornado_png
		super().__init__(square_obj, object_vs, object_fs, self.image_file)
		self.generate()
		self.set_texture(1)
		self.scale(.06, .09, 1)
		self.translate(*randedge(.05, -1, 1, -1, 1), 0)
		self.speed = uniform(.001, .003)
		self.vector = get_vector(
			self.speed,
			uniform(-.5, .5) - self.box.mlz[0],
			uniform(-.5, .5) - self.box.mlz[1],
			*self.box.muz[:2],
		)
		self.groups = groups
		for group in groups:
			group.append(self)
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def update(self):
		self.translate(*self.vector, 0)
		if any([
			self.box.ux < -1.05,
			self.box.lx > 1.05,
			self.box.uy < -1.05,
			self.box.ly > 1.05
		]):
			self.kill()
	def draw(self):
		self.update()
		super().draw()

class Background(objloader.Obj):
	def __init__(self, image_file):
		super().__init__(square_obj, object_vs, object_fs, image_file)
		self.generate()
		self.set_texture(1)
		self.translate(0, 0, .5)

class Hud_Button(objloader.Obj):
	def __init__(self, image_file, location):
		super().__init__(square_obj, object_vs, object_fs, image_file)
		self.generate()
		self.set_texture(1)
		self.scale(.1, .15, 1)
		self.translate(*location, 0)
		self.is_hovering = False
	def rollover(self):
		over_x = self.box.lx < pixel_to_view(*pg.mouse.get_pos())[0] < self.box.ux
		over_y = self.box.ly < pixel_to_view(*pg.mouse.get_pos())[1] < self.box.uy
		return over_x and over_y
	def update(self):
		if self.rollover() and not self.is_hovering:
			self.scale(1.25, 1.25, 1)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.scale(.8, .8, 1)
			self.is_hovering = False
	def draw(self):
		self.update()
		super().draw()