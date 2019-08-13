
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_TAB
)
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame.freetype as ft
import screen
from assets.paths import window_close_png, splat_png, square_obj, cube_obj, object_vs, object_fs
from fonts.paths import calibri_ttf
from assets import objloader

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

class Button():
	def __init__(self, location, size, image_file, orientation='center', color=(255, 255, 255)):
		self.location = location
		self.size = size
		self.image_file = image_file
		self.orientation = orientation
		self.color = color

		icon = Icon(self.location, self.size, self.image_file, self.orientation, self.color)
		self.surface, self.rect = icon.surface, icon.rect
		self.is_hovering = False
	def rollover(self):
		over_x = self.rect.left <= pg.mouse.get_pos()[0] <= self.rect.right
		over_y = self.rect.top <= pg.mouse.get_pos()[1] <= self.rect.bottom
		return over_x and over_y
	def hover(self):
		if self.rollover() and not self.is_hovering:
			self.surface = Icon(
				self.location,
				self.size,
				self.image_file,
				self.orientation,
				color=(0, 0, 0)
			).surface
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.surface = Icon(
				self.location,
				self.size,
				self.image_file,
				self.orientation,
				self.color
			).surface
			self.is_hovering = False

class Window:
	def __init__(self, title, splat_count, view):
		self.clock = pg.time.Clock()
		self.view = view

		self.light = objloader.Obj(cube_obj, object_vs, object_fs)
		self.light.scale(0, 0, 0)
		self.light.translate(0, 0, 2)

		self.background = objloader.Obj(square_obj, object_vs, object_fs)
		self.background.color = (21 / 256, 26 / 256, 27 / 256, 1)
		self.background.generate()
		self.background.set_light_source(self.light)

		self.title_bar = objloader.Obj(square_obj, object_vs, object_fs)
		self.title_bar.color = (.25, .25, .25, 1)
		self.title_bar.generate()
		self.title_bar.scale(1, 1 / 30, 1)
		self.title_bar.translate(0, 1 - self.title_bar.box.uy, 0)
		self.title_bar.set_light_source(self.light)

		# self.title_bar = Element(location, (size[0], screen.height // 30), (65, 65, 65), 'topleft')
		# self.title = Text(title, self.title_bar.rect.center, self.title_bar.rect.height * 7 // 8)
		# self.close_button = Button(
		# 	(screen.width, 0),
		# 	(self.title_bar.rect.height, self.title_bar.rect.height),
		# 	window_close_png,
		# 	orientation='topright',
		# 	color=(232, 17, 35)
		# )
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
