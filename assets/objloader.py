
from pywavefront import Wavefront
import pygame
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import shaders
import numpy as np
import glm
from math import pi
from ast import literal_eval

identity = [
	[1, 0, 0, 0],
	[0, 1, 0, 0],
	[0, 0, 1, 0],
	[0, 0, 0, 1]
]

PERSPECTIVE = np.matrix(identity, np.float32)
obj_list = []

def set_perspective(angle, width, height, z_min, z_max):
	PERSPECTIVE = np.matrix(glm.perspective(angle, width / height, z_min, z_max), np.float32)
	for i in obj_list:
		i.perspective = PERSPECTIVE

def dedup_and_index(sequence):
	sequence_ref = {}
	new_sequence = []
	indices = [i for i in range(len(sequence))]
	for i, vertex in enumerate(list(sequence)):
		strung = str(list(vertex))
		if strung in sequence_ref:
			indices[i] = sequence_ref[strung]
		else:
			indices[i] = len(sequence_ref)
			sequence_ref[strung] = indices[i]
	for i in sequence_ref.keys():
		new_sequence.append(literal_eval(i))
	return indices, new_sequence

class Obj:
	def __init__(self, filename, v_shader, f_shader):
		"""Loads a Wavefront OBJ file. """
		self.filename = filename
		self.vertex_info = [] # unique combinations of position, normal and color
		self.model = np.matrix(identity, np.float32)
		self.perspective = PERSPECTIVE
		obj_list.append(self)
		self.position = np.array([0, 0, 0], np.float32)
		self.shader = None
		self.vertex_shader = open(v_shader)
		self.fragment_shader = open(f_shader)

		scene = Wavefront(self.filename)
		scene.parse()

		for material in scene.materials.values():
			vertex_format = 0
			for i in material.vertex_format:
				if i.isdigit():
					vertex_format += int(i)
			vertices = np.array(material.vertices, np.float32).reshape(len(material.vertices) // vertex_format, vertex_format)
			indices, vertex_info = dedup_and_index(vertices)
		self.indices = np.array(indices, np.int32)
		self.vertex_info = np.array(vertex_info, np.float32)

	def generate(self):
		self.VAO, self.VBO, self.EBO = GLuint(), GLuint(), GLuint()
		self.VAO = glGenVertexArrays(1)
		glBindVertexArray(self.VAO)
		self.VBO = glGenBuffers(1)
		self.EBO = glGenBuffers(1)

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, self.vertex_info, GL_STATIC_DRAW)

		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

		glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 32, None)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(8))
		glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
		glEnableVertexAttribArray(0)
		glEnableVertexAttribArray(1)
		glEnableVertexAttribArray(2)
		glBindVertexArray(0)

	def compile_shader(self):
		vertex_shader = shaders.compileShader(self.vertex_shader, GL_VERTEX_SHADER)
		fragment_shader = shaders.compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)
		self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
		self.uniforms = {}
		for name in ('model', 'transform', 'light_color', 'light_position'):
			self.uniforms[name] = glGetUniformLocation(self.shader, name)

	def use_shader(self):
		if self.shader == None:
			self.compile_shader()
		shaders.glUseProgram(self.shader) # pylint: disable=no-member
		for uniform in self.uniforms.keys():
			glUniformMatrix4fv(self.uniforms.get('transform', 0), 1, False, self.model * self.perspective)

	def set_perspective(self, angle, width, height, z_min, z_max):
		self.perspective = np.matrix(glm.perspective(angle, width / height, z_min, z_max), np.float32)

	def translate(self, x, y, z):
		self.model = np.matrix(glm.translate(self.model, [x, y, z]), np.float32)
		self.position += np.array([x, y, z], np.float32)

	def rotate(self, angle, x, y, z):
		self.model = np.matrix(glm.rotate(self.model, angle, [x, y, z]), np.float32)

	def scale(self, x, y, z):
		self.model = np.matrix(glm.scale(self.model, [x, y, z]), np.float32)

	def draw(self):
		self.use_shader() # pylint: disable=no-member
		glBindVertexArray(self.VAO)
		glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
