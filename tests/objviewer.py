
import context
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from assets import objloader
import numpy as np
from math import pi
from assets.paths import *
from shaders.paths import *

def main():
	pygame.init()
	display = (1024, 768)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	glEnable(GL_DEPTH_TEST)
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	light_cube = objloader.Obj(cube_obj, light_vs, light_fs, uv_test_png)
	light_cube.generate()
	square = objloader.Obj(square_obj, object_vs, object_fs, uv_test_png)
	square.generate()
	square.set_light_source(light_cube)

	objloader.set_perspective(pi / 4, *display, 0.1, 100)
	light_cube.translate(10, 5, -25)
	light_cube.rotate(pi / 6, 1, 0, 0)
	square.translate(0, 0, -50)
	# square.rotate(pi / 3, -1, 0, 0)
	# square.scale(.5, .5, .5)

	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
				raise SystemExit
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_w]:
			light_cube.translate(0, 0, .1)
		if pressed_keys[K_s]:
			light_cube.translate(0, 0, -.1)
		if pressed_keys[K_a]:
			light_cube.translate(-.1, 0, 0)
		if pressed_keys[K_d]:
			light_cube.translate(.1, 0, 0)
		if pressed_keys[K_SPACE]:
			light_cube.translate(0, .1, 0)
		if pressed_keys[K_LCTRL]:
			light_cube.translate(0, -.1, 0)
		if pressed_keys[K_UP]:
			light_cube.rotate(pi / 1000, 1, 0, 0)
		if pressed_keys[K_DOWN]:
			light_cube.rotate(pi / 1000, -1, 0, 0)
		if pressed_keys[K_LEFT]:
			light_cube.rotate(pi / 1000, 0, 1, 0)
		if pressed_keys[K_RIGHT]:
			light_cube.rotate(pi / 1000, 0, -1, 0)
		if pressed_keys[K_q]:
			light_cube.rotate(pi / 1000, 0, 0, 1)
		if pressed_keys[K_e]:
			light_cube.rotate(pi / 1000, 0, 0, -1)

		square.rotate(pi / 100, 0, 1, 0)
		square.draw()

		light_cube.rotate(pi / 100, 0, -1, 0)
		light_cube.draw()

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()