
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
from assets.paths import square_obj, object_vs, object_fs, Menu_Button_png, menu_png

def pixel_to_view(x, y):
	vx = x / (screen.width / 2) - 1
	vy = y / (screen.height / 2) - 1
	return (-vx, -vy)

class Menu_Button(objloader.Obj):
	def __init__(self, text:str, location:tuple):
		size = (screen.width // 3, screen.height // 20)
		img = Image.new('RGB', size, color = (65, 65, 65))
		text_location = (size[0] * 3 / 4, size[1] / 8)
		font_ = ImageFont.truetype('fonts/calibri.ttf', size[1] * 7 // 8)
		decoration = ImageDraw.Draw(img)
		decoration.text(text_location, text, font=font_, fill=(170, 64, 78))
		img.save(Menu_Button_png)

		super().__init__(square_obj, object_vs, object_fs, Menu_Button_png)
		self.generate()
		self.translate(*location, 0)
		self.scale(.33, .05, 1)
		self.set_texture(1)

		self.is_hovering = False

	def rollover(self):
		return self.box.ly < pixel_to_view(*pg.mouse.get_pos())[1] < self.box.uy

	def hover(self):
		if self.rollover() and not self.is_hovering:
			self.translate(1 / 30, 0, 0)
			self.is_hovering = True
		if not self.rollover() and self.is_hovering:
			self.translate(-1 / 30, 0, 0)
			self.is_hovering = False

class Menu():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), FULLSCREEN|OPENGL|DOUBLEBUF)
		self.menu_screen = Background(menu_png)
		self.play_button = Menu_Button('Play!', (-1, 0))
		self.quit_button = Menu_Button('Quit', (-1, -.2))
	def play(self):
		while True:
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
			self.play_button.hover()
			self.play_button.draw()
			self.quit_button.hover()
			self.quit_button.draw()
			self.clock.tick(60)
