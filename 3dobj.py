
import pygame
from pygame.locals import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import shaders
from OpenGL.GLU import * # pylint: disable=unused-wildcard-import
from objloader import Obj, Mtl
import numpy as np

def main():
	pygame.init() # pylint: disable=no-member
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # pylint: disable=undefined-variable
	
	player = Obj('care.obj')
	player.generate()
	light_cube = Obj('cube.obj')
	for i, vertex in enumerate(light_cube.vertices):
		vertex[2] += 100
		light_cube.vertices[i] = vertex
	light_cube.generate()

	white = (1, 1, 1)
	red = (1, 0, 0)
	car_fragment_shader = shaders.compileShader("""#version 330 core
	out vec4 FragColor;
	
	uniform vec3 car_color;
	uniform vec3 light_color;

	void main()
	{
		float ambientStrength = 0.1;
		vec3 ambient = ambientStrength * light_color;

		vec3 result = ambient * car_color;
		FragColor = vec4(result, 1.0);
	}""", GL_FRAGMENT_SHADER)
	car_shader = shaders.compileProgram(car_fragment_shader)
	UNIFORM_LOCATIONS = {
		'light_color': glGetUniformLocation(car_shader, 'light_color'),
		'car_color': glGetUniformLocation(car_shader, 'car_color')
	}

	lamp_fragment_shader = shaders.compileShader("""#version 330 core
	out vec4 FragColor;

	void main()
	{
		FragColor = vec4(1.0); // set all 4 vector values to 1.0
	}""", GL_FRAGMENT_SHADER)
	lamp_shader = shaders.compileProgram(lamp_fragment_shader)

	gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
	glTranslatef(0, 0, -1500)
	glRotatef(-60, 1, 0, 0)
	glRotatef(180, 0, 0, 1)

	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT: # pylint: disable=undefined-variable
				pygame.quit() # pylint: disable=no-member
				quit()
		
		glRotatef(1, 0, 0, 1)

		shaders.glUseProgram(car_shader) # pylint: disable=no-member
		glUniform3f(UNIFORM_LOCATIONS['light_color'], *white)
		glUniform3f(UNIFORM_LOCATIONS['car_color'], *red)
		glCallList(player.gl_list)

		shaders.glUseProgram(lamp_shader) # pylint: disable=no-member
		glCallList(light_cube.gl_list)

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
