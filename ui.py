
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE
)
import pygame.freetype as ft
import screen
from sprites import image_path

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
		self.font = ft.Font('fonts/calibri.ttf', size=size)
		self.surface, self.rect = self.font.render(text, fgcolor=color)
		if orientation == 'center':
			self.rect.center = location
		elif orientation == 'midleft':
			self.rect.midleft = location

class Icon():
	def __init__(self, location, size, image_file, orientation='center'):
		self.surface = pg.image.load(image_path + image_file).convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.surface = pg.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect()
		if orientation == 'center':
			self.rect.center = location
		elif orientation == 'topright':
			self.rect.topright = location
		elif orientation == 'topleft':
			self.rect.topleft = location

class Button():
	def __init__(self, location, size, image_file, orientation='center'):
		icon = Icon(location, size, image_file, orientation)
		self.surface, self.rect = icon.surface, icon.rect
		self.is_hovering = False
	def rollover(self):
		over_x = self.rect.left <= pg.mouse.get_pos()[0] <= self.rect.right
		over_y = self.rect.top <= pg.mouse.get_pos()[1] <= self.rect.bottom
		return over_x and over_y
	def hover(self):
		if self.rollover() and not self.is_hovering:
			# highlight red
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			# remove highlight
			self.is_hovering = False


class Window():
	def __init__(self, title, splat_count, location=(0, 0), size=(screen.width, screen.height)):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN) # pylint: disable=no-member

		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill((21, 26, 27))
		self.rect.left, self.rect.top = location

		self.title_bar = Element(location, (size[0], screen.height // 30), (65, 65, 65), 'topleft')
		self.title = Text(title, self.title_bar.rect.center, self.title_bar.rect.height * 7 // 8)
		self.close_button = Button(
			(screen.width, 0),
			(self.title_bar.rect.height, self.title_bar.rect.height),
			'window close.png',
			orientation='topright'
		)
		self.splat_icon = Icon(
			(screen.width // 50, screen.height * 11 // 12),
			(screen.width // 25, screen.height // 16),
			'splat.png',
			orientation='topleft'
		)
		self.splat_count = Text(
			str(splat_count),
			(screen.width // 15, screen.height * 19 // 20),
			screen.height // 16,
			orientation='midleft'
		)
		self.is_open = True
	def open(self):
		while self.is_open:
			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.is_open = False
				if event.type == MOUSEBUTTONDOWN and self.close_button.rollover():
						self.is_open = False
			pg.display.flip()
			self.view.blit(self.surface, self.rect)
			self.view.blit(self.title_bar.surface, self.title_bar.rect)
			self.view.blit(self.title.surface, self.title.rect)
			self.view.blit(self.close_button.surface, self.close_button.rect)
			self.view.blit(self.splat_icon.surface, self.splat_icon.rect)
			self.view.blit(self.splat_count.surface, self.splat_count.rect)
			self.clock.tick(60)
