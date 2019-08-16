
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_TAB
)
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame.freetype as ft
import screen
from assets.paths import (
	window_close_png, window_close_active_png, splat_png, square_obj, cube_obj,
	object_vs, object_fs, ui_vs, ui_fs, fractal_png, pink_bubbles_png,
	depot_png, red_gloop_png, blue_squares_png
)
from fonts.paths import calibri_ttf
from assets import objloader
from helpers import text_image, pixel_to_view
from sprites import Player
from math import pi

class Close_Button:
	def __init__(self):
		self.close_button = objloader.Obj(square_obj, object_vs, object_fs, window_close_png)
		self.close_button.generate()
		self.close_button.set_texture(1)
		self.close_button.scale(1 / 20, 1 / 15, 1)
		self.close_button.translate(
			1 - self.close_button.box.ux,
			1 - self.close_button.box.uy,
			-.1
		)

		self.close_button_hover = objloader.Obj(square_obj, object_vs, object_fs, window_close_active_png)
		self.close_button_hover.generate()
		self.close_button_hover.set_texture(1)
		self.close_button_hover.scale(1 / 20, 1 / 15, 1)
		self.close_button_hover.translate(
			1 - self.close_button_hover.box.ux,
			1 - self.close_button_hover.box.uy,
			-.1
		)
	def rollover(self):
		over_x = self.close_button.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.close_button.box.ux
		over_y = self.close_button.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.close_button.box.uy
		return over_x and over_y
	def draw(self):
		if self.rollover():
			self.close_button_hover.draw()
		else:
			self.close_button.draw()

class Color_Button:
	def __init__(self, location, color):
		self.active = False
		self.fill = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.fill.generate()
		self.fill.color = color
		self.fill.scale(.03, .05, 1)
		self.fill.translate(*location, -.1)

		self.border = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.border.generate()
		self.border.color = [1, 1, 1, .25]
		self.border.scale(.04, .06, 1)
		self.border.translate(*location, 0)
	def rollover(self):
		over_x = self.border.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.border.box.ux
		over_y = self.border.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.border.box.uy
		return over_x and over_y
	def draw(self):
		self.border.color[3] = .25
		if self.rollover():
			self.border.color[3] = .5
		if self.active:
			self.border.color[3] = 1
		self.border.draw()
		self.fill.draw()

class Texture_Button:
	def __init__(self, x, y, texture):
		self.active = False
		self.fill = objloader.Obj(square_obj, object_vs, object_fs, texture)
		self.fill.generate()
		self.fill.set_texture(1)
		self.fill.scale(.03, .05, 1)
		self.fill.translate(x, y, -.1)

		self.border = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.border.generate()
		self.border.color = [1, 1, 1, .25]
		self.border.scale(.04, .06, 1)
		self.border.translate(x, y, 0)
	def rollover(self):
		over_x = self.border.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.border.box.ux
		over_y = self.border.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.border.box.uy
		return over_x and over_y
	def draw(self):
		self.border.color[3] = .25
		if self.rollover():
			self.border.color[3] = .5
		if self.active:
			self.border.color[3] = 1
		self.border.draw()
		self.fill.draw()

class Text(objloader.Obj):
	def __init__(self, text, orientation='left'):
		text_image_file = text_image(text, (170, 64, 78), orientation)
		super().__init__(square_obj, object_vs, object_fs, text_image_file)
		self.generate()
		self.set_texture(1)

class Splats_Number(Text):
	def __init__(self, text):
		super().__init__(str(text))
		self.scale(1, .1, 1)
		self.translate(.2, -.9, 0)
	def update(self, text):
		self.__init__(text)

class Window:
	def __init__(self, title, splat_count, view, player):
		self.clock = pg.time.Clock()
		self.view = view
		self.splat_count = splat_count

		self.background = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.background.generate()
		self.background.color = (21 / 256, 26 / 256, 27 / 256, 1)
		self.background.translate(0, 0, .9)

		self.title_bar = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.title_bar.generate()
		self.title_bar.color = (.25, .25, .25, 1)
		self.title_bar.scale(1, 1 / 15, 1)
		self.title_bar.translate(0, 1 - self.title_bar.box.uy, 0)

		text_image_file = text_image(title, (170, 64, 78))
		self.title_text = objloader.Obj(square_obj, object_vs, object_fs, text_image_file)
		self.title_text.generate()
		self.title_text.set_texture(1)
		self.title_text.scale(1, .1, 1)
		self.title_text.scale(.66, .66, 1)
		self.title_text.translate(0, 1 - self.title_text.box.uy, -.1)

		self.close_button = Close_Button()

		self.paint_select = []
		for args in [
			(-.95, .78, 1, 0, 0, 1), # red
			(-.95, .64, 0, .449, 0, 1), # green
			(-.85, .78, .7245, .7245, .7245, 1), # silver
			(-.85, .64, .977, .977, 0, 1), # yellow
			(-.85, .50, 1, 0.078125, 0.703125, 1) # pink
		]:
			self.paint_select.append(Color_Button(args[:2], args[2:]))

		for args in [
			(-.95, .50, blue_squares_png),
			(-.95, .36, red_gloop_png),
			(-.85, .36, pink_bubbles_png),
			(-.95, .22, depot_png),
			(-.85, .22, fractal_png)
		]:
			self.paint_select.append(Texture_Button(*args))

		self.splat_icon = objloader.Obj(square_obj, object_vs, object_fs, splat_png)
		self.splat_icon.generate()
		self.splat_icon.set_texture(1)
		self.splat_icon.scale(.04, .06, 1)
		self.splat_icon.translate(-.9, -.9, 0)

		self.splats_number = Splats_Number(str(splat_count[0]))

		self.player = player

		self.car = Player()
		self.car.generate()
		self.car.scale(5, 3, 5)
		self.car.rotate(pi / 3, 1, 0, 0)
	def draw(self):
		self.background.draw()
		self.title_bar.draw()
		self.title_text.draw()
		self.close_button.draw()
		self.splat_icon.draw()
		self.splats_number.draw()
		for button in self.paint_select:
			button.draw()
		self.car.rotate(pi / 500, 0, 0, 1)
		self.car.draw()
	def open(self):
		self.splats_number.update(str(self.splat_count[0]))
		self.is_open = True
		while self.is_open:
			for event in pg.event.get():
				if (
					(event.type == KEYDOWN and event.key == K_ESCAPE) or
					(event.type == KEYDOWN and event.key == K_TAB) or
					(event.type == MOUSEBUTTONDOWN and self.close_button.rollover()) or
					event.type == QUIT
				):
					self.is_open = False

				for button in self.paint_select:
					if event.type == MOUSEBUTTONDOWN and button.rollover():
						for other_button in self.paint_select:
							other_button.active = False
						button.active = True
						if type(button) == Color_Button:
							self.car.body.color = button.fill.color
							self.car.body.set_texture(0)
							self.player.body.color = button.fill.color
							self.player.body.set_texture(0)
						elif type(button) == Texture_Button:
							self.player.body.texture = button.fill.texture
							self.player.body.set_texture(1)
							self.car.body.texture = button.fill.texture
							self.car.body.set_texture(1)

			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.draw()
			self.clock.tick(60)
