
from random import randint
import pygame as pg
from pygame.constants import ( # pylint: disable=no-name-in-module
	RLEACCEL, MOUSEBUTTONDOWN, KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
)
import pygame.freetype as ft
from helpers import moveTo, randedge
import screen
image_path = 'game art\\'

class Player(pg.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surface = pg.image.load(image_path + 'car.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(0, screen.height // 2))
		self.speed = 10
		self.bigtime = 0
	def update(self):
		pressed_keys = pg.key.get_pressed()
		if pressed_keys[K_w] or pressed_keys[K_UP]:
			self.rect.move_ip(0, -self.speed)
		if pressed_keys[K_s] or pressed_keys[K_DOWN]:
			self.rect.move_ip(0, self.speed)
		if pressed_keys[K_a] or pressed_keys[K_LEFT]:
			self.rect.move_ip(-self.speed, 0)
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
			self.rect.move_ip(self.speed, 0)
		if self.bigtime <= 0:
			self.surface = pg.image.load(image_path + 'car.png').convert()
			self.surface.set_colorkey((255, 255, 255), RLEACCEL)
			self.rect = self.surface.get_rect(center=(self.rect.center))
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > screen.width:
			self.rect.right = screen.width
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= screen.height:
			self.rect.bottom = screen.height
		self.bigtime -= 1 if self.bigtime > 0 else 0
	def embiggen(self):
		self.surface = pg.image.load(image_path + 'big car.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(self.rect.center))
		self.bigtime = 50

class PlayerBullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		super(PlayerBullet, self).__init__()
		self.surface = pg.image.load(image_path + 'bullet.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(x, y))
		self.speed = 30
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.right > screen.width:
			self.kill()

class Enemy(pg.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surface = pg.image.load(image_path + 'green goblin.png').convert()
		self.surface.set_colorkey((255, 0, 0), RLEACCEL)
		self.rect = self.surface.get_rect(center=(screen.width, randint(25, screen.height - 25)))
		self.speed = randint(5, 20)
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Splat(pg.sprite.Sprite):
	def __init__(self, x, y):
		super(Splat, self).__init__()
		self.surface = pg.image.load(image_path + 'Splat.png').convert()
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surface.get_rect(center=(x, y))
		self.health = 300
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()

class Tornado(pg.sprite.Sprite):
	def __init__(self):
		super(Tornado, self).__init__()
		self.magic = randint(0, 10)
		self.surface = pg.image.load(image_path + ('tornado.png' if self.magic < 8 else 'rainbow_tornado.png')).convert()
		self.surface.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.surface.get_rect(center=(randedge(25, screen.width, screen.height)))
		self.speed = randint(5, 8)
		self.waypoint = []
		self.__getWaypoint()
	def __getWaypoint(self):
		x = randint(screen.width // 4, 3 * screen.width // 4)
		y = randint(screen.height // 4, 3 * screen.height // 4)
		self.waypoint = moveTo(self.rect.center, [x, y], 3000)
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.waypoint, self.speed))

class Background(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.surface = pg.transform.scale(pg.image.load(image_path + image_file), (screen.width, screen.height))
		self.rect = self.surface.get_rect()
		self.rect.left, self.rect.top = location

class Hud_Button(pg.sprite.Sprite):
	def __init__(self, image_file, location, size):
		pg.sprite.Sprite.__init__(self)
		self.surface = pg.image.load(image_path + image_file)
		self.surface.set_colorkey((255, 255, 255), RLEACCEL)
		self.surface = pg.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect()
		self.rect.left, self.rect.top = location
	def rollover(self):
		over_x = self.rect.left < pg.mouse.get_pos()[0] < self.rect.right
		over_y = self.rect.top < pg.mouse.get_pos()[1] < self.rect.bottom
		return over_x and over_y
	def update(self):
		pass

class Game_UI_Element():
	def __init__(self, location, size, color=(0, 0, 0)):
		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill(color)
		self.rect.left, self.rect.top = location

class Game_UI_Text():
	def __init__(self, text, location, size, color=(170, 64, 78)):
		self.font = ft.Font('fonts/calibri.ttf', size=size)
		self.surface, self.rect = self.font.render(text, fgcolor=color)
		self.rect.center = location
		
class Game_UI_Window():
	def __init__(self, title, location=(0, 0), size=(screen.width, screen.height)):
		self.clock = pg.time.Clock()
		self.view = pg.display.set_mode((screen.width, screen.height), pg.FULLSCREEN) # pylint: disable=no-member

		self.surface = pg.Surface(size) # pylint: disable=too-many-function-args
		self.rect = self.surface.fill((21, 26, 27))
		self.rect.left, self.rect.top = location

		self.title_bar = Game_UI_Element(location, (size[0], screen.height // 30), (65, 65, 65))
		self.title = Game_UI_Text(title, self.title_bar.rect.center, self.title_bar.rect.height * 7 // 8)

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
