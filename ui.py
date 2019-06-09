
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE
)
import pygame.freetype as ft
import screen

class Element():
	def __init__(self, location, size, color=(0, 0, 0)):
		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill(color)
		self.rect.left, self.rect.top = location

class Text():
	def __init__(self, text, location, size, color=(170, 64, 78)):
		self.font = ft.Font('fonts/calibri.ttf', size=size)
		self.surface, self.rect = self.font.render(text, fgcolor=color)
		self.rect.center = location
		
class Window():
	def __init__(self, title, location=(0, 0), size=(screen.width, screen.height)):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN) # pylint: disable=no-member

		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill((21, 26, 27))
		self.rect.left, self.rect.top = location

		self.title_bar = Element(location, (size[0], screen.height // 30), (65, 65, 65))
		self.title = Text(title, self.title_bar.rect.center, self.title_bar.rect.height * 7 // 8)

		self.is_open = True
	def open(self):
		while self.is_open:
			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					self.is_open = False
				# if event.type == MOUSEBUTTONDOWN and self.quit_button.rollover():
					# 	self.is_open = False
			pg.display.flip()
			self.view.blit(self.surface, self.rect)
			self.view.blit(self.title_bar.surface, self.title_bar.rect)
			self.view.blit(self.title.surface, self.title.rect)
			self.clock.tick(60)
