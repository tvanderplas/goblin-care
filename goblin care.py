import random
import pygame
from pygame.locals import *
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
print("stretching prevented")

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.image = pygame.image.load(image_path + 'car.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(0, info.current_h / 2))
		self.speed = 10
	def update(self, pressed_keys):
		if pressed_keys[K_w] or pressed_keys[K_UP]:
			self.rect.move_ip(0, -self.speed)
		if pressed_keys[K_s] or pressed_keys[K_DOWN]:
			self.rect.move_ip(0, self.speed)
		if pressed_keys[K_a] or pressed_keys[K_LEFT]:
			self.rect.move_ip(-self.speed, 0)
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
			self.rect.move_ip(self.speed, 0)
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > info.current_w:
			self.rect.right = info.current_w
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= info.current_h:
			self.rect.bottom = info.current_h

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self):
		super(PlayerBullet, self).__init__()
		self.image = pygame.image.load(image_path + 'bullet.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center=(player.rect.right, player.rect.centery))
		self.speed = 30
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.right > info.current_w:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.image = pygame.image.load(image_path + 'green_goblin.png').convert()
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
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
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, random.randint(500, 750))
all_sprites = pygame.sprite.Group()


def game():
	isRunning = True
	while isRunning:

		if pygame.sprite.spritecollideany(player, enemies):
			player.kill()
			for sprite in all_sprites:
				sprite.kill()
			isRunning = False
		for enemy in pygame.sprite.groupcollide(enemies, bullets, True, True):
			new_splat = Splat(enemy.rect.centerx, enemy.rect.centery)
			all_sprites.add(new_splat)

		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				player.kill()
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			elif event.type == QUIT:
				player.kill()
				for sprite in all_sprites:
					sprite.kill()
				isRunning = False
			elif event.type == ADDENEMY:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)
			elif event.type == KEYDOWN and event.key == K_SPACE:
				new_player_bullet = PlayerBullet()
				all_sprites.add(new_player_bullet)
				bullets.add(new_player_bullet)

		pressed_keys = pygame.key.get_pressed()
		player.update(pressed_keys)
		for sprite in all_sprites:
			sprite.update()
		for entity in all_sprites:
			screen.blit(entity.image, entity.rect)
		screen.blit(player.image, player.rect)
		pygame.display.flip()
		screen.blit(background.image, background.rect)
		clock.tick(60)

menu_screen = Background(image_path + 'stopgo.png', [0, 0])

isMenuOpen = True

while isMenuOpen:
	for event in pygame.event.get():
		if event.type == MOUSEBUTTONDOWN:
			if pygame.mouse.get_pos()[0] < info.current_w / 2:
				game()
			elif pygame.mouse.get_pos()[0] >= info.current_w / 2:
				isMenuOpen = False
	pygame.display.flip()
	screen.blit(menu_screen.image, menu_screen.rect)
	clock.tick(15)
