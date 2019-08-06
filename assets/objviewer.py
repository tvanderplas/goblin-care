
import pygame
from pygame.locals import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import shaders
import objloader
import numpy as np
from math import pi

def main():
	pygame.init() # pylint: disable=no-member
	display = (1024, 768)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # pylint: disable=undefined-variable
	glEnable(GL_DEPTH_TEST)

	light_cube = objloader.Obj('cube.obj', 'basic vertex shader.vs', 'basic fragment shader.fs')
	light_cube.generate()
	player = objloader.Obj('sedan_body.obj', 'car body.vs', 'car body.fs')
	player.generate()
	player.set_light_source(light_cube)
	glass = objloader.Obj('sedan_glass.obj', 'car body.vs', 'car body.fs')
	glass.generate()
	glass.set_light_source(light_cube)

	objloader.set_perspective(pi / 4, *display, 0.1, 100)
	light_cube.translate(10, 5, -25)
	light_cube.rotate(pi / 6, 1, 0, 0)
	player.translate(0, 0, -50)
	player.rotate(pi / 3, -1, 0, 0)
	player.scale(.5, .5, .5)
	glass.translate(0, 0, -50)
	glass.rotate(pi / 3, -1, 0, 0)
	glass.scale(.5, .5, .5)
	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT: # pylint: disable=undefined-variable
				raise SystemExit
			if (event.type == KEYDOWN and event.key == K_SPACE):
				player.set_texture(player.texture_mode ^ 1)

		player.rotate(pi / 1000, 0, 0, 1)
		player.draw()

		glass.rotate(pi / 1000, 0, 0, 1)
		glass.draw()

		light_cube.rotate(pi / 100, 0, -1, 0)
		light_cube.draw()

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
