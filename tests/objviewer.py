
import context
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from assets import objloader
import numpy as np
from math import pi
from assets import *
from shaders.paths import *
from tests.paths import *
from random import random
import screen

def main():
	pygame.init()
	display = (screen.width, screen.height)
	pygame.display.set_mode(display, FULLSCREEN|DOUBLEBUF|OPENGL)
	glEnable(GL_DEPTH_TEST)
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	light_cube = objloader.Obj(cube_obj, light_vs, light_fs, uv_test_png)
	light_cube.generate()
	square = objloader.Obj(square_obj, object_vs, object_fs, uv_test_png)
	square.generate()
	square.set_light_source(light_cube)
	square.set_texture(1)

	light_cube.translate(10, 5, -25)
	light_cube.rotate(pi / 6, 1, 0, 0)

	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
				raise SystemExit
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_w]:
			square.translate(0, 0, .1)
		if pressed_keys[K_s]:
			square.translate(0, 0, -.1)
		if pressed_keys[K_a]:
			square.translate(-.1, 0, 0)
		if pressed_keys[K_d]:
			square.translate(.1, 0, 0)
		if pressed_keys[K_SPACE]:
			square.translate(0, .1, 0)
		if pressed_keys[K_LCTRL]:
			square.translate(0, -.1, 0)
		if pressed_keys[K_UP]:
			square.rotate(pi / 1000, 1, 0, 0)
		if pressed_keys[K_DOWN]:
			square.rotate(pi / 1000, -1, 0, 0)
		if pressed_keys[K_LEFT]:
			square.rotate(pi / 1000, 0, 1, 0)
		if pressed_keys[K_RIGHT]:
			square.rotate(pi / 1000, 0, -1, 0)
		if pressed_keys[K_q]:
			square.rotate(pi / 1000, 0, 0, 1)
		if pressed_keys[K_e]:
			square.rotate(pi / 1000, 0, 0, -1)

		square.draw()

		light_cube.draw()

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
