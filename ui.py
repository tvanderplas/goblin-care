
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_TAB
)
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame.freetype as ft
import screen
from assets import (
	window_close_png, window_close_active_png, splat_png, square_obj, cube_obj, fractal_png, pink_bubbles_png,
	depot_png, red_gloop_png, blue_squares_png, buy_png
)
from fonts.paths import calibri_ttf
from assets import objloader
from shaders.paths import object_vs, object_fs, ui_vs, ui_fs
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
		self.cost = 5
		self.owned = False
		self.fill = Ui_Color(color)
		self.fill.scale(.03, .05, 1)
		self.fill.translate(*location, -.1)

		self.border = Ui_Color([1, 1, 1, .25])
		self.border.scale(.04, .06, 1)
		self.border.translate(*location, 0)

		self.buy_button = Buy_Button(self.cost)
	def rollover(self):
		over_x = self.border.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.border.box.ux
		over_y = self.border.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.border.box.uy
		return over_x and over_y
	def draw(self):
		if self.active and not self.owned:
			self.buy_button.draw()
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
		self.cost = 20
		self.owned = False
		self.fill = Ui_Image(texture)
		self.fill.scale(.03, .05, 1)
		self.fill.translate(x, y, -.1)

		self.border = Ui_Color([1, 1, 1, .25])
		self.border.scale(.04, .06, 1)
		self.border.translate(x, y, 0)

		self.buy_button = Buy_Button(self.cost)
	def rollover(self):
		over_x = self.border.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.border.box.ux
		over_y = self.border.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.border.box.uy
		return over_x and over_y
	def draw(self):
		if self.active and not self.owned:
			self.buy_button.draw()
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

class Ui_Color(objloader.Obj):
	def __init__(self, color):
		super().__init__(square_obj, ui_vs, ui_fs)
		self.generate()
		self.color = color

class Ui_Image(objloader.Obj):
	def __init__(self, image):
		super().__init__(square_obj, object_vs, object_fs, image)
		self.generate()
		self.set_texture(1)

class Splats_Number(Text):
	def __init__(self, text):
		super().__init__(str(text))
		self.scale(1, .1, 1)
		self.translate(.2, -.9, 0)
	def update(self, text):
		self.__init__(text)

class Buy_Button:
	def __init__(self, cost):
		self.buy_button = Ui_Image(buy_png)
		self.buy_button.scale(.08, .06, 1)
		self.buy_button.translate(-.05, -.4, 0)

		self.cost_icon = Ui_Image(splat_png)
		self.cost_icon.scale(.04, .06, 1)
		self.cost_icon.translate(-.075, -.27, 0)

		self.splat_cost = Text(str(cost))
		self.splat_cost.scale(.28, .07, 1)
		self.splat_cost.translate(.25, -.27, 0)
	def rollover(self):
		over_x = self.buy_button.box.lx <= pixel_to_view(*pg.mouse.get_pos())[0] <= self.buy_button.box.ux
		over_y = self.buy_button.box.ly <= pixel_to_view(*pg.mouse.get_pos())[1] <= self.buy_button.box.uy
		return over_x and over_y
	def draw(self):
		self.buy_button.draw()
		self.cost_icon.draw()
		self.splat_cost.draw()

class Loot_Screen:
	def __init__(self, title, splat_count, view, player):
		self.clock = pg.time.Clock()
		self.view = view
		self.splat_count = splat_count

		self.background = Ui_Color((21 / 256, 26 / 256, 27 / 256, 1))
		self.background.translate(0, 0, .9)

		self.title_bar = Ui_Color((.25, .25, .25, 1))
		self.title_bar.scale(1, 1 / 15, 1)
		self.title_bar.translate(0, 1 - self.title_bar.box.uy, 0)

		self.title_text = Text(title, 'center')
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
					if all([
						event.type == MOUSEBUTTONDOWN,
						button.buy_button.rollover(),
						button.active,
						self.splat_count[0] >= button.cost
					]):
						self.splat_count[0] -= button.cost
						button.owned = True
						self.splats_number.update(str(self.splat_count[0]))
						if type(button) == Color_Button:
								self.player.body.color = button.fill.color
								self.player.body.set_texture(0)
						elif type(button) == Texture_Button:
								self.player.body.texture = button.fill.texture
								self.player.body.set_texture(1)
					if event.type == MOUSEBUTTONDOWN and button.rollover():
						for other_button in self.paint_select:
							other_button.active = False
						button.active = True
						if type(button) == Color_Button:
							self.car.body.color = button.fill.color
							self.car.body.set_texture(0)
							if button.owned:
								self.player.body.color = button.fill.color
								self.player.body.set_texture(0)
						elif type(button) == Texture_Button:
							self.car.body.texture = button.fill.texture
							self.car.body.set_texture(1)
							if button.owned:
								self.player.body.texture = button.fill.texture
								self.player.body.set_texture(1)

			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.draw()
			self.clock.tick(60)
