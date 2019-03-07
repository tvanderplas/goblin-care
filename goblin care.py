import random
import math
import pygame
from pygame.locals import *
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
print("stretching prevented")

def randedge(distance):
	edge = random.choice([
		[random.randint(distance, info.current_w - distance), distance],# top
		[random.randint(distance, info.current_w - distance), info.current_h - distance],# bottom
		[distance, random.randint(distance, info.current_h - distance)],# left
		[info.current_w - distance, random.randint(distance, info.current_h - distance)],# right
	])
	return edge
def moveTo(initial, final, speed):
	displacement_x = final[0] - initial[0]
	displacement_y = final[1] - initial[1]
	slope = float(displacement_y / (displacement_x if displacement_x != 0 else 1))
	inclination = math.atan(slope)
	delta_x = speed * math.cos(inclination)
	delta_y = speed * math.sin(inclination)
	return [delta_x, delta_y] if displacement_x > 0 else [-delta_x, -delta_y]

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.image = pygame.image.load(image_path + 'car.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(0, info.current_h / 2))
		self.speed = 10
		self.bigtime = 0
	def update(self):
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_w] or pressed_keys[K_UP]:
			self.rect.move_ip(0, -self.speed)
		if pressed_keys[K_s] or pressed_keys[K_DOWN]:
			self.rect.move_ip(0, self.speed)
		if pressed_keys[K_a] or pressed_keys[K_LEFT]:
			self.rect.move_ip(-self.speed, 0)
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
			self.rect.move_ip(self.speed, 0)
		if self.bigtime <= 0:
			self.image = pygame.image.load(image_path + 'car.png').convert()
			self.image.set_colorkey((255, 255, 255), RLEACCEL)
			self.rect = self.image.get_rect(center=(self.rect.center))
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > info.current_w:
			self.rect.right = info.current_w
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= info.current_h:
			self.rect.bottom = info.current_h
		self.bigtime -= 1 if self.bigtime > 0 else 0
	def embiggen(self):
		self.image = pygame.image.load(image_path + 'big car.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(self.rect.center))
		self.bigtime = 50

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(PlayerBullet, self).__init__()
		self.image = pygame.image.load(image_path + 'bullet.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(x, y))
		self.speed = 30
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.right > info.current_w:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.image = pygame.image.load(image_path + 'green goblin.png').convert()
		self.image.set_colorkey((255, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center=(info.current_w, random.randint(25, info.current_h - 25)))
		self.speed = random.randint(5, 20)
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Splat(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Splat, self).__init__()
		self.image = pygame.image.load(image_path + 'Splat.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(x, y))
		self.health = 300
	def update(self):
		self.health -= 1
		if self.health <= 0:
			self.kill()

class Tornado(pygame.sprite.Sprite):
	def __init__(self):
		super(Tornado, self).__init__()
		self.magic = random.randint(0, 10)
		self.image = pygame.image.load(image_path + ('tornado.png' if self.magic < 8 else 'rainbow_tornado.png')).convert()
		self.image.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center=(randedge(25)))
		self.speed = random.randint(5, 8)
		self.waypoint = []
		self.__getWaypoint()
	def __getWaypoint(self):
		x = random.randint(info.current_w / 4, 3 * info.current_w / 4)
		y = random.randint(info.current_h / 4, 3 * info.current_h / 4)
		self.waypoint = moveTo(self.rect.center, [x, y], 3000)
	def update(self):
		self.rect.move_ip(moveTo(self.rect.center, self.waypoint, self.speed))

class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(image_file), (info.current_w, info.current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

pygame.init()
clock = pygame.time.Clock()
image_path = '''game art\\'''
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)

background = Background(image_path + 'desert road.png', [0, 0])
ADDENEMY = pygame.USEREVENT + 1
NEWTORNADO = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, random.randint(500, 750))
pygame.time.set_timer(NEWTORNADO, random.randint(250, 3500))
enemies = pygame.sprite.Group()
splats = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tornados = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def game():
	player = Player()
	all_sprites.add(player)
	isRunning = True
	while isRunning:

		if pygame.sprite.spritecollideany(player, enemies):
			for sprite in all_sprites:
				sprite.kill()
			isRunning = False
		for enemy in pygame.sprite.groupcollide(enemies, bullets, True, True):
			new_splat = Splat(enemy.rect.centerx, enemy.rect.centery)
			all_sprites.add(new_splat)
			splats.add(new_splat)
		for tornado in pygame.sprite.spritecollide(player, tornados, False):
			if tornado.magic < 8:
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			else:
				player.embiggen()

		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			elif event.type == ADDENEMY:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)
			elif event.type == NEWTORNADO:
				new_tornado = Tornado()
				tornados.add(new_tornado)
				all_sprites.add(new_tornado)
			elif event.type == KEYDOWN and event.key == K_SPACE:
				new_player_bullet = PlayerBullet(player.rect.right, player.rect.centery)
				all_sprites.add(new_player_bullet)
				bullets.add(new_player_bullet)

		for sprite in all_sprites:
			sprite.update()
		for splat in splats:
			screen.blit(splat.image, splat.rect)
		screen.blit(player.image, player.rect)
		for enemy in enemies:
			screen.blit(enemy.image, enemy.rect)
		for bullet in bullets:
			screen.blit(bullet.image, bullet.rect)
		for tornado in tornados:
			screen.blit(tornado.image, tornado.rect)
		pygame.display.flip()
		screen.blit(background.image, background.rect)
		clock.tick(60)

menu_screen = Background(image_path + 'stopgo.png', [0, 0])

while True:
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
			raise SystemExit
		if event.type == MOUSEBUTTONDOWN:
			if pygame.mouse.get_pos()[0] < info.current_w / 2:
				game()
			elif pygame.mouse.get_pos()[0] >= info.current_w / 2:
				raise SystemExit
	pygame.display.flip()
	screen.blit(menu_screen.image, menu_screen.rect)
	clock.tick(15)
