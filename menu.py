
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_ESCAPE, K_SPACE, FULLSCREEN, OPENGL, DOUBLEBUF
)
import pygame.freetype as ft
from sprites import Background
from game_engine import Game
import screen
from PIL import Image, ImageDraw, ImageFont
from assets import objloader
from assets.loader import *

class Menu_Button(objloader.Obj):
	def __init__(self, text:str, location:tuple):
		size = (screen.width // 3, screen.height // 20)
		img = Image.new('RGB', size, color = (65, 65, 65))
		font_ = ImageFont.truetype('fonts/calibri.ttf', 15)
		d = ImageDraw.Draw(img)
		d.text((10,10), text, font=font_, fill=(170, 64, 78))
		super().__init__(square_obj, object_vs, object_fs, d)
		super().generate()

		# self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		# self.rect = self.surface.fill((65, 65, 65))
		# self.text = ft.Font('fonts/calibri.ttf', size=size[1] * 7 // 8)
		# self.text.rect = self.text.get_rect(text)
		# offset = (self.rect.height - self.text.rect.height) // 2
		# text_location = ((self.rect.right - self.text.rect.width) - offset, self.rect.top + offset)
		# self.text.rect = self.text.render_to(
		# 	self.surface, text_location, text, fgcolor=(170, 64, 78)
		# )
		# self.rect.left, self.rect.top = location
		# self.is_hovering = False
	def rollover(self):
		return False # self.rect.top < pg.mouse.get_pos()[1] < self.rect.bottom
	# def hover(self):
	# 	if self.rollover() and not self.is_hovering:
	# 		self.rect.move_ip(screen.width // 30, 0)
	# 		self.is_hovering = True
	# 	if not self.rollover() and self.is_hovering:
	# 		self.rect.move_ip(-screen.width // 30, 0)
	# 		self.is_hovering = False

class Menu():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), FULLSCREEN|OPENGL|DOUBLEBUF)
		self.menu_screen = Background('menu.png')
		self.play_button = Menu_Button('Play!', (-screen.width // 5, screen.height // 2))
		self.quit_button = Menu_Button('Quit', (-screen.width // 5, screen.height * 3 // 5))
	def play(self):
		while True:
			# self.play_button.hover()
			# self.quit_button.hover()
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
			# self.play_button.draw()
			# self.quit_button.draw()
			self.clock.tick(60)
