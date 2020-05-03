
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, FULLSCREEN, OPENGL, DOUBLEBUF
)
import pygame.freetype as ft
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from sprites import Background
import overworld
import screen
from PIL import Image, ImageDraw, ImageFont
from assets import objloader
from assets import square_obj, menu_png, controls_png
from shaders import object_vs, object_fs, ui_vs, ui_fs
from fonts import calibri_ttf
from helpers import pixel_to_view, text_image
from ui import Ui_Image

class Pointer_Indicator(objloader.Obj):
	def __init__(self):
		super().__init__(square_obj, object_vs, object_fs)
		self.generate()
		self.scale(.01, .01, .01)
		self.color = (0, 1, 1, 1)

	def update(self):
		mousepos = pixel_to_view(*pg.mouse.get_pos())
		vector = [mousepos[i] - self.position[i] for i in range(2)]
		self.translate(vector[0], vector[1], 0)

	def draw(self):
		self.update()
		super().draw()

class Controls_Popup:
	def __init__(self):
		self.background = Ui_Image(controls_png)
		self.visible = False
	def show(self):
		self.visible = True
	def hide(self):
		self.visible = False
	def toggle(self):
		self.visible ^= 1
	def draw(self):
		if self.visible:
			self.background.draw()

class Menu_Button:
	def __init__(self, text:str, location:tuple):
		self.background = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.background.color = (.25, .25, .25, 1)
		self.background.generate()
		self.background.translate(*location, 0)
		self.background.scale(.33, .05, 1)

		self.text = objloader.Obj(square_obj, object_vs, object_fs, text_image(text, (170, 64, 78), 'right'))
		self.text.generate()
		self.text.set_texture(1)
		self.text.scale(1, .1, 1)
		self.text.scale(.5, .5, 1)
		self.text.translate(*location, 0)
		self.text.translate(-.2, 0, 0)

		self.is_hovering = False

	def rollover(self):
		return self.background.box.ly < pixel_to_view(*pg.mouse.get_pos())[1] < self.background.box.uy

	def hover(self):
		if self.rollover() and not self.is_hovering:
			self.background.translate(1 / 8, 0, 0)
			self.text.translate(1 / 8, 0, 0)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.background.translate(-1 / 8, 0, 0)
			self.text.translate(-1 / 8, 0, 0)
			self.is_hovering = False

	def draw(self):
		self.hover()
		self.background.draw()
		self.text.draw()

class Menu():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), FULLSCREEN|OPENGL|DOUBLEBUF)
		self.menu_screen = Background(menu_png)
		self.play_button = Menu_Button('Play!', (-1.05, 0))
		self.controls_button = Menu_Button('Controls   ', (-1.05, -.2))
		self.quit_button = Menu_Button('Quit', (-1.05, -.4))
		self.controls = Controls_Popup()
	def play(self):
		while True:
			for event in pg.event.get():
				if event.type == QUIT or (
					event.type == KEYDOWN and event.key == K_ESCAPE and not self.controls.visible
				):
					raise SystemExit
				if event.type == KEYDOWN and event.key == K_ESCAPE and self.controls.visible:
					self.controls.toggle()
				if event.type == MOUSEBUTTONDOWN:
					if self.play_button.rollover():
						game = overworld.Game(self.view)
						game.play()
						self.__init__()
					elif self.controls_button.rollover():
						self.controls.toggle()
					elif self.quit_button.rollover():
						raise SystemExit
			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.menu_screen.draw()
			self.play_button.draw()
			self.controls_button.draw()
			self.quit_button.draw()
			self.controls.draw()
			self.clock.tick(60)
