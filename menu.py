
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE
)
from sprites import Background, Menu_Button
from game_engine import Game
import screen

class Menu():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN) # pylint: disable=no-member
		self.menu_screen = Background('menu.png', [0, 0])
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
			self.view.blit(self.menu_screen.surface, self.menu_screen.rect)
			self.view.blit(self.play_button.surface, self.play_button.rect)
			self.view.blit(self.quit_button.surface, self.quit_button.rect)
			self.clock.tick(60)
