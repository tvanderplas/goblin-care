
from random import random, uniform
from pygame import mouse
from game.helpers import randedge, pixel_to_view, get_vector
from game.assets import objloader
from game.assets import *
from game.shaders import object_vs, object_fs, ui_vs, ui_fs
from math import pi

class Player(object):
	def __init__(self):
		self.parts = [
			objloader.Obj(sedan_body_obj, object_vs, object_fs),
			objloader.Obj(sedan_glass_obj, object_vs, object_fs),
			objloader.Obj(sedan_wheels_obj, object_vs, object_fs),
			objloader.Obj(sedan_tires_obj, object_vs, object_fs),
		]
		self.body = self.parts[0]
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
	@property
	def box(self):
		return self.parts[0].box
	def keep_on_screen(self):
		if self.box.lx < -1:
			self.translate(-1 - self.box.lx, 0, 0)
		if self.box.ux > 1:
			self.translate(1 - self.box.ux, 0, 0)
		if self.box.ly < -1:
			self.translate(0, -1 - self.box.ly, 0)
		if self.box.uy > 1:
			self.translate(0, 1 - self.box.uy, 0)
	def check_bigness(self):
		if self.bigtime <= 0 and self.is_big:
			self.scale(2/3, 2/3, 2/3)
			self.is_big = False
	def embiggen(self):
		if not self.is_big:
			self.scale(1.5, 1.5, 1.5)
			self.bigtime = 500
			self.is_big = True
	def generate(self):
		for part in self.parts:
			part.generate()
	def set_light_source(self, light):
		for part in self.parts:
			part.set_light_source(light)
	def translate(self, x, y, z):
		for part in self.parts:
			part.translate(x, y, z)
	def rotate(self, angle, x, y, z):
		for part in self.parts:
			part.rotate(angle, x, y, z)
	def scale(self, x, y, z):
		for part in self.parts:
			part.scale(x, y, z)
	def draw(self):
		self.check_bigness()
		self.keep_on_screen()
		self.bigtime -= 1 if self.bigtime > 0 else 0
		for part in self.parts:
			part.draw()

class PlayerBullet(objloader.Obj):
	def __init__(self, x, y, groups):
		super().__init__(square_obj, ui_vs, ui_fs, bullet_png)
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

class Rainbow_Bullet(objloader.Obj):
	def __init__(self, x, y, groups):
		super().__init__(square_obj, ui_vs, ui_fs, rainbow_bullet_png)
		self.generate()
		self.set_texture(1)
		self.translate(x, y, 0)
		self.scale(.05, .05, 1)
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
		super().__init__(square_obj, ui_vs, ui_fs, green_goblin_png)
		self.generate()
		self.set_texture(1)
		height = uniform(-.9, .9)
		self.translate(1, height, -.1)
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
		super().__init__(square_obj, ui_vs, ui_fs, splat_png)
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
		super().__init__(square_obj, ui_vs, ui_fs, splat_png)
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
		self.is_rainbow = True if random() > .8 else False
		self.image_file = rainbow_tornado_png if self.is_rainbow else tornado_png
		super().__init__(square_obj, ui_vs, ui_fs, self.image_file)
		self.generate()
		self.set_texture(1)
		self.scale(.06, .09, 1)
		self.translate(*randedge(.05, -1, 1, -1, 1), -.2)
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
		super().__init__(square_obj, ui_vs, ui_fs, image_file)
		self.generate()
		self.set_texture(1)
		self.translate(0, 0, .5)

class Hud_Button(objloader.Obj):
	def __init__(self, image_file, location, groups):
		super().__init__(square_obj, ui_vs, ui_fs, image_file)
		self.generate()
		self.set_texture(1)
		self.scale(.1, .15, 1)
		self.translate(*location, -.3)
		self.is_hovering = False
		self.groups = groups
		for group in groups:
			group.append(self)
	def kill(self):
		for group in self.groups:
			group.remove(self)
	def rollover(self):
		over_x = self.box.lx < pixel_to_view(*mouse.get_pos())[0] < self.box.ux
		over_y = self.box.ly < pixel_to_view(*mouse.get_pos())[1] < self.box.uy
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