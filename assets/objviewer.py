
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

	player = objloader.Obj('sedan_uvmap.obj', 'car body.vs', 'car body.fs')
	player.generate()
	glass = objloader.Obj('sedan_glass.obj', 'car body.vs', 'car body.fs')
	glass.generate()
	light_cube = objloader.Obj('cube.obj', 'basic vertex shader.vs', 'basic fragment shader.fs')
	light_cube.generate()

	car_vertex_shader = shaders.compileShader(open('car body.vs'), GL_VERTEX_SHADER)
	car_fragment_shader = shaders.compileShader(open('car body.fs'), GL_FRAGMENT_SHADER)
	car_shader = shaders.compileProgram(car_vertex_shader, car_fragment_shader)

	UNIFORM_LOCATIONS = {
		'model': glGetUniformLocation(car_shader, 'model'),
		'transform': glGetUniformLocation(car_shader, 'transform'),
		'light_color': glGetUniformLocation(car_shader, 'light_color'),
		'light_position': glGetUniformLocation(car_shader, 'light_position')
	}
	shaders.glUseProgram(car_shader) # pylint: disable=no-member
	glUniform3fv(UNIFORM_LOCATIONS['light_color'], 1, (1,1,1))

	objloader.set_perspective(pi / 4, *display, 0.1, 100)
	light_cube.translate(10, 5, -25)
	light_cube.rotate(pi / 6, 1, 0, 0)
	light_cube.scale(.1, .1, .1)
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

		shaders.glUseProgram(car_shader) # pylint: disable=no-member
		player.rotate(pi / 1000, 0, 0, 1)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['transform'], 1, False, player.model * player.perspective)
		glUniform3f(UNIFORM_LOCATIONS['light_position'], *light_cube.position)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['model'], 1, False, player.model)
		glBindVertexArray(player.VAO)
		glDrawElements(GL_TRIANGLES, len(player.indices), GL_UNSIGNED_INT, None)

		glass.rotate(pi / 1000, 0, 0, 1)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['transform'], 1, False, glass.model * glass.perspective)
		glUniform3f(UNIFORM_LOCATIONS['light_position'], *light_cube.position)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['model'], 1, False, glass.model)
		glBindVertexArray(glass.VAO)
		glDrawElements(GL_TRIANGLES, len(glass.indices), GL_UNSIGNED_INT, None)

		light_cube.rotate(pi / 100, 0, -1, 0)
		light_cube.draw()

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
