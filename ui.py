
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

class Element():
	def __init__(self, location, size, color=(0, 0, 0), orientation='center'):
		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill(color)
		self.rect.left, self.rect.top = location
		if orientation == 'center':
			self.rect.center = location
		elif orientation == 'topright':
			self.rect.topright = location
		elif orientation == 'topleft':
			self.rect.topleft = location

class Text():
	def __init__(self, text, location, size, orientation='center', color=(170, 64, 78)):
		self.font = ft.Font(calibri_ttf, size=size)
		self.surface, self.rect = self.font.render(text, fgcolor=color)
		if orientation == 'center':
			self.rect.center = location
		elif orientation == 'midleft':
			self.rect.midleft = location

class Icon():
	def __init__(self, location, size, image_file, orientation='center', color=(255, 255, 255)):
		self.surface = pg.image.load(image_file).convert()
		self.surface.set_colorkey(color, RLEACCEL)
		self.surface = pg.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect()
		if orientation == 'center':
			self.rect.center = location
		elif orientation == 'topright':
			self.rect.topright = location
		elif orientation == 'topleft':
			self.rect.topleft = location

class Close_Button:
	def __init__(self):
		self.close_button = objloader.Obj(square_obj, object_vs, object_fs, window_close_png)
		self.close_button.generate()
		self.close_button.set_texture(1)
		self.close_button.scale(1 / 20, 1 / 15, 1)
		self.close_button.translate(
			1 - self.close_button.box.ux,
			1 - self.close_button.box.uy,
			0
		)

		self.close_button_hover = objloader.Obj(square_obj, object_vs, object_fs, window_close_active_png)
		self.close_button_hover.generate()
		self.close_button_hover.set_texture(1)
		self.close_button_hover.scale(1 / 20, 1 / 15, 1)
		self.close_button_hover.translate(
			1 - self.close_button_hover.box.ux,
			1 - self.close_button_hover.box.uy,
			0
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

class Window:
	def __init__(self, title, splat_count, view):
		self.clock = pg.time.Clock()
		self.view = view

		self.background = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.background.generate()
		self.background.color = (21 / 256, 26 / 256, 27 / 256, 1)

		self.title_bar = objloader.Obj(square_obj, ui_vs, ui_fs)
		self.title_bar.generate()
		self.title_bar.color = (.25, .25, .25)
		self.title_bar.scale(1, 1 / 15, 1)
		self.title_bar.translate(0, 1 - self.title_bar.box.uy, 0)

		text_image_file = text_image(title, (170, 64, 78))
		self.title_text = objloader.Obj(square_obj, object_vs, object_fs, text_image_file)
		self.title_text.generate()
		self.title_text.set_texture(1)
		self.title_text.scale(1, .1, 1)
		self.title_text.scale(.66, .66, 1)
		self.title_text.translate(0, 1 - self.title_text.box.uy, 0)

		self.close_button = Close_Button()

		self.splat_icon = Icon(
			(screen.width // 50, screen.height * 11 // 12),
			(screen.width // 25, screen.height // 16),
			splat_png,
			orientation='topleft'
		)
		self.splat_count = Text(
			str(splat_count),
			(screen.width // 15, screen.height * 19 // 20),
			screen.height // 16,
			orientation='midleft'
		)
		self.is_open = True
	def draw(self):
		self.background.draw()
		self.title_bar.draw()
		self.title_text.draw()
		self.close_button.draw()
	def open(self):
		while self.is_open:
			# self.close_button.hover()
			for event in pg.event.get():
				if (
					(event.type == KEYDOWN and event.key == K_ESCAPE) or
					(event.type == KEYDOWN and event.key == K_TAB) or
					# (event.type == MOUSEBUTTONDOWN and self.close_button.rollover()) or
					event.type == QUIT
				):
					self.is_open = False
			pg.display.flip()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.draw()
			# self.view.blit(self.surface, self.rect)
			# self.view.blit(self.title_bar.surface, self.title_bar.rect)
			# self.view.blit(self.title.surface, self.title.rect)
			# self.view.blit(self.close_button.surface, self.close_button.rect)
			# self.view.blit(self.splat_icon.surface, self.splat_icon.rect)
			# self.view.blit(self.splat_count.surface, self.splat_count.rect)
			self.clock.tick(60)
