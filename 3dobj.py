
import pygame
from pygame.locals import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import shaders
import objloader
import numpy as np
from math import pi

def main():
	pygame.init() # pylint: disable=no-member
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # pylint: disable=undefined-variable
	glEnable(GL_DEPTH_TEST)

	player = objloader.Obj('care.obj')
	player.generate()
	light_cube = objloader.Obj('cube.obj')
	light_cube.generate()

	car_vertex_shader = shaders.compileShader("""
	#version 330 core
	layout (location = 0) in vec3 vertex_position;
	layout (location = 1) in vec3 vertex_normal;
	layout (location = 2) in vec3 vertex_color;

	out vec3 position;
	out vec3 normal;
	out vec3 color;

	uniform mat4 car_transform;

	void main()
	{
		gl_Position = car_transform * vec4(vertex_position, 1.0);
		position = vertex_position;
		normal = vertex_normal;
		color = vertex_color;
	}""", GL_VERTEX_SHADER)
	car_fragment_shader = shaders.compileShader("""
	#version 330 core
	out vec4 FragColor;

	in vec3 position;
	in vec3 normal;
	in vec3 color;
	uniform vec3 light_color;
	uniform vec3 light_position;

	void main()
	{
		// ambient
		float ambientStrength = 0.1;
		vec3 ambient = ambientStrength * light_color;

		vec3 light_direction = normalize(light_position - position);
		float diff = max(dot(normal, light_direction), 0.0);
		vec3 diffuse = diff * light_color;
		vec3 result = (ambient + diffuse) * color;
		FragColor = vec4(result, 1.0);
	}""", GL_FRAGMENT_SHADER)
	car_shader = shaders.compileProgram(car_vertex_shader, car_fragment_shader)

	lamp_vertex_shader = shaders.compileShader("""
	#version 330 core
	layout (location = 0) in vec3 vertex_position;
	layout (location = 1) in vec3 vertex_normal;
	layout (location = 2) in vec3 vertex_color;

	out vec3 position;
	out vec3 normal;
	out vec3 color;

	uniform mat4 lamp_transform;

	void main()
	{
		gl_Position = lamp_transform * vec4(vertex_position, 1.0);
		position = vec3(lamp_transform * vec4(vertex_position, 1.0));
		normal = vertex_normal;
		color = vertex_color;
	}""", GL_VERTEX_SHADER)
	lamp_fragment_shader = shaders.compileShader("""
	#version 330 core
	out vec4 FragColor;

	in vec3 position;
	in vec3 normal;
	in vec3 color;

	void main()
	{
		FragColor = vec4(color, 1.0);
	}""", GL_FRAGMENT_SHADER)
	lamp_shader = shaders.compileProgram(lamp_vertex_shader, lamp_fragment_shader)
	UNIFORM_LOCATIONS = {
		'car_transform': glGetUniformLocation(car_shader, 'car_transform'),
		'light_color': glGetUniformLocation(car_shader, 'light_color'),
		'light_position': glGetUniformLocation(car_shader, 'light_position'),
		'lamp_transform': glGetUniformLocation(lamp_shader, 'lamp_transform')
	}
	shaders.glUseProgram(car_shader) # pylint: disable=no-member
	glUniform3fv(UNIFORM_LOCATIONS['light_color'], 1, (1,1,1))

	objloader.set_perspective(pi / 4, *display, 0.1, 100)
	light_cube.translate(10, 10, -50)
	light_cube.scale(.1, .1, .1)
	player.translate(0, 0, -50)
	player.rotate(pi / 2, -1, 0, 0)
	player.rotate(pi / 6, 1, 0, 0)
	player.scale(.1, .1, .1)
	light_cube.rotate(pi / 6, 1, 0, 0)
	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT: # pylint: disable=undefined-variable
				pygame.quit() # pylint: disable=no-member
				quit()

		shaders.glUseProgram(car_shader) # pylint: disable=no-member
		player.rotate(pi / 1000, 0, 0, 1)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['car_transform'], 1, False, player.model * player.perspective)
		glUniform3f(UNIFORM_LOCATIONS['light_position'], *light_cube.position)
		glBindVertexArray(player.VAO)
		glDrawElements(GL_TRIANGLES, len(player.indices), GL_UNSIGNED_INT, None)

		shaders.glUseProgram(lamp_shader) # pylint: disable=no-member
		light_cube.rotate(pi / 1000, 0, 1, 0)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['lamp_transform'], 1, False, light_cube.model * light_cube.perspective)
		glBindVertexArray(light_cube.VAO)
		glDrawElements(GL_TRIANGLES, len(light_cube.indices), GL_UNSIGNED_INT, None)

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
