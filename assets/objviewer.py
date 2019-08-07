
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

	light_cube = objloader.Obj('cube.obj', 'light.vs', 'light.fs')
	light_cube.generate()
	square = objloader.Obj('square.obj', 'object.vs', 'object.fs')
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
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT: # pylint: disable=undefined-variable
				raise SystemExit
			if (event.type == KEYDOWN and event.key == K_SPACE): # pylint: disable=undefined-variable
				square.set_texture(square.texture_mode ^ 1)

		square.rotate(pi / 100, 0, 1, 0)
		square.draw()

		light_cube.rotate(pi / 100, 0, -1, 0)
		light_cube.draw()

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
