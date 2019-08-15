
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_TAB
)
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame.freetype as ft
import screen
from assets.paths import window_close_png, window_close_active_png, splat_png, square_obj, cube_obj, object_vs, object_fs, ui_vs, ui_fs
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
		self.fill = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.fill.generate()
		self.fill.color = color
		self.fill.scale(1 / 30, 1 / 21, 1)
		self.fill.translate(*location, -.1)

		self.border = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.border.generate()
		self.border.color = [1, 1, 1, .25]
		self.border.scale(1 / 20, 1 / 15, 1)
		self.border.translate(*location, 0)
	def rollover(self):
		over_x = self.border.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.border.box.ux
		over_y = self.border.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.border.box.uy
		return over_x and over_y
	def draw(self):
		if self.rollover():
			self.border.color[3] = .75
		else:
			self.border.color[3] = .25
		self.border.draw()
		self.fill.draw()

class Window:
	def __init__(self, title, splat_count, view):
		self.clock = pg.time.Clock()
		self.view = view

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

		self.splat_icon = objloader.Obj(square_obj, object_vs, object_fs, splat_png)
		self.splat_icon.generate()
		self.splat_icon.set_texture(1)
		self.splat_icon.scale(.04, .06, 1)
		self.splat_icon.translate(-.9, -.9, 0)

		text_image_file = text_image(str(splat_count), (170, 64, 78), 'left')
		self.splats_number = objloader.Obj(square_obj, object_vs, object_fs, text_image_file)
		self.splats_number.generate()
		self.splats_number.set_texture(1)
		self.splats_number.scale(1, .1, 1)
		self.splats_number.translate(.2, -.9, 0)

		self.car = Player()
		self.car.generate()
		self.car.scale(5, 3, 5)
		self.car.rotate(pi / 3, 1, 0, 0)

		self.color_select = Color_Button((.5, .5), (1, 1, 0, 1))

		self.is_open = True
	def draw(self):
		self.background.draw()
		self.title_bar.draw()
		self.title_text.draw()
		self.close_button.draw()
		self.splat_icon.draw()
		self.splats_number.draw()
		self.color_select.draw()
		self.car.rotate(pi / 500, 0, 0, 1)
		self.car.draw()
	def open(self):
		while self.is_open:
			for event in pg.event.get():
				if (
					(event.type == KEYDOWN and event.key == K_ESCAPE) or
					(event.type == KEYDOWN and event.key == K_TAB) or
					(event.type == MOUSEBUTTONDOWN and self.close_button.rollover()) or
					event.type == QUIT
				):
					self.is_open = False
			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.draw()
			self.clock.tick(60)
