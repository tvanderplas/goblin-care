
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
	light_cube.vertices[::] /= 10
	light_cube.generate()

	white = (1, 1, 1)
	red = (1, 0, 0)
	player_model = np.array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	player_view = np.array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	player_projection = np.array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	car_vertex_shader = shaders.compileShader("""
	#version 330 core
	layout (location = 0) in vec3 aPos;
	layout (location = 1) in vec3 aNormal;

	out vec3 FragPos;
	out vec3 Normal;

	uniform mat4 model;
	uniform mat4 view;
	uniform mat4 projection;

	void main()
	{
		FragPos = vec3(model * vec4(aPos, 1.0));
		Normal = mat3(transpose(inverse(model))) * aNormal; 
	
		gl_Position = projection * view * vec4(FragPos, 1.0);
	}""", GL_VERTEX_SHADER)
	car_fragment_shader = shaders.compileShader("""
	#version 330 core
	out vec4 FragColor;

	in vec3 Normal;
	in vec3 FragPos;

	uniform vec3 lightPos;
	uniform vec3 viewPos;
	uniform vec3 car_color;
	uniform vec3 light_color;

	void main()
	{
		// ambient
		float ambientStrength = 0.1;
		vec3 ambient = ambientStrength * light_color;
	
		// diffuse
		vec3 norm = normalize(Normal);
		vec3 lightDir = normalize(lightPos - FragPos);
		float diff = max(dot(norm, lightDir), 0.0);
		vec3 diffuse = diff * light_color;
	}""", GL_FRAGMENT_SHADER)
	car_shader = shaders.compileProgram(car_vertex_shader, car_fragment_shader)
	UNIFORM_LOCATIONS = {
		'light_color': glGetUniformLocation(car_shader, 'light_color'),
		'car_color': glGetUniformLocation(car_shader, 'car_color'),
		'model': glGetUniformLocation(car_shader, 'model'),
		'view': glGetUniformLocation(car_shader, 'view'),
		'projection': glGetUniformLocation(car_shader, 'projection')
	}

	lamp_vertex_shader = shaders.compileShader("""
	#version 330 core
	layout (location = 0) in vec3 aPos;

	void main()
	{
		gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
	}""", GL_VERTEX_SHADER)
	lamp_fragment_shader = shaders.compileShader("""#version 330 core
	out vec4 FragColor;

	void main()
	{
		FragColor = vec4(1.0); // set all 4 vector values to 1.0
	}""", GL_FRAGMENT_SHADER)
	lamp_shader = shaders.compileProgram(lamp_vertex_shader, lamp_fragment_shader)

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
		glBindVertexArray(player.VAO)
		glUniform3f(UNIFORM_LOCATIONS['light_color'], *white)
		glUniform3f(UNIFORM_LOCATIONS['car_color'], *red)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['model'], 1, False, player_model)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['view'], 1, False, player_view)
		glUniformMatrix4fv(UNIFORM_LOCATIONS['projection'], 1, False, player_projection)

		shaders.glUseProgram(lamp_shader) # pylint: disable=no-member
		glBindVertexArray(light_cube.VAO)
		glDrawArrays(GL_TRIANGLES, 0, len(light_cube.vertices) // 3)

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
