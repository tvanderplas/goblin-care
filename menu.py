
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, FULLSCREEN, OPENGL, DOUBLEBUF
)
import pygame.freetype as ft
from sprites import Background
from game_engine import Game
import screen

class Menu_Button():
	def __init__(self, text:str, location:tuple, size:tuple=(screen.width // 3, screen.height // 20)):
		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill((65, 65, 65))
		self.text = ft.Font('fonts/calibri.ttf', size=size[1] * 7 // 8)
		self.text.rect = self.text.get_rect(text)
		offset = (self.rect.height - self.text.rect.height) // 2
		text_location = ((self.rect.right - self.text.rect.width) - offset, self.rect.top + offset)
		self.text.rect = self.text.render_to(
			self.surface, text_location, text, fgcolor=(170, 64, 78)
		)
		self.rect.left, self.rect.top = location
		self.is_hovering = False
	def rollover(self):
		return self.rect.top < pg.mouse.get_pos()[1] < self.rect.bottom
	def hover(self):
		if self.rollover() and not self.is_hovering:
			self.rect.move_ip(screen.width // 30, 0)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.rect.move_ip(-screen.width // 30, 0)
			self.is_hovering = False

class Menu():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), FULLSCREEN|OPENGL|DOUBLEBUF)
		self.menu_screen = Background('menu.png')
		self.play_button = Menu_Button('Play!', (-screen.width // 5, screen.height // 2))
		self.quit_button = Menu_Button('Quit', (-screen.width // 5, screen.height * 3 // 5))
	def play(self):
		while True:
			self.play_button.hover()
			self.quit_button.hover()
			for event in pg.event.get():
				if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
					raise SystemExit
				if event.type == MOUSEBUTTONDOWN:
					if self.play_button.rollover():
						game = Game()
						game.play()
					elif self.quit_button.rollover():
						raise SystemExit
			pg.display.flip()
			self.menu_screen.draw()
			# self.view.blit(self.play_button.surface, self.play_button.rect)
			# self.view.blit(self.quit_button.surface, self.quit_button.rect)
			self.clock.tick(60)
