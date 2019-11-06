
from PIL import Image
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import shaders
from pywavefront import Wavefront
import numpy as np
import glm
from math import pi
from ast import literal_eval

PERSPECTIVE = glm.mat4()
obj_list = []

def set_perspective(angle, width, height, z_min, z_max):
	PERSPECTIVE = glm.mat4(glm.perspective(angle, width / height, z_min, z_max))
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

class Box:
	def __init__(self, lx=None, ux=None, ly=None, uy=None, lz=None, uz=None):
		self.lx = lx
		self.ux = ux
		self.ly = ly
		self.uy = uy
		self.lz = lz
		self.uz = uz
		self.mlx = (lx, self.avg([ly, uy]), self.avg([lz, uz]))
		self.mux = (ux, self.avg([ly, uy]), self.avg([lz, uz]))
		self.mly = (self.avg([lx, ux]), ly, self.avg([lz, uz]))
		self.muy = (self.avg([lx, ux]), uy, self.avg([lz, uz]))
		self.mlz = (self.avg([lx, ux]), self.avg([ly, uy]), lz)
		self.muz = (self.avg([lx, ux]), self.avg([ly, uy]), uz)

	def avg(self, arg:list):
		return sum(arg) / len(arg)

class Obj:
	def __init__(self, scene, v_shader, f_shader, texture=None):
		"""Loads a Wavefront OBJ file. """
		self.vertex_info = [] # unique combinations of position, normal and color
		self.model = glm.mat4()
		self.perspective = PERSPECTIVE
		obj_list.append(self)
		self.position = np.array([0, 0, 0], np.float32)
		self.light = self
		self.light.color = (0, 0, 0)
		self.light.position = (0, 0, 0)
		self.shader = None
		self.vertex_shader = open(v_shader)
		self.fragment_shader = open(f_shader)
		self.texture_mode = 0
		self.texture = texture
		self.translated = glm.mat4()
		self.rotated = glm.mat4()
		self.scaled = glm.mat4()

		scene = Wavefront(scene)
		scene.parse()
		for material in scene.materials.values():
			vertex_format = 0
			for i in material.vertex_format:
				if i.isdigit():
					vertex_format += int(i)
			vertices = np.array(material.vertices, np.float32).reshape(len(material.vertices) // vertex_format, vertex_format)
			indices, vertex_info = dedup_and_index(vertices)
			self.color = material.diffuse
		self.indices = np.array(indices, np.int32)
		self.vertex_info = np.array(vertex_info, np.float32)
		self.get_box()

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
		self.set_texture(self.texture_mode)

	def get_box(self):
		minimums = [min(self.vertex_info[::, i]) for i in range(5, 8)]
		maximums = [max(self.vertex_info[::, i]) for i in range(5, 8)]
		lx, ly, lz = glm.vec3(self.translated * self.scaled * glm.vec4(minimums + [1]))
		ux, uy, uz = glm.vec3(self.translated * self.scaled * glm.vec4(maximums + [1]))
		self.box = Box(lx, ux, ly, uy, lz, uz)

	def compile_shader(self):
		vertex_shader = shaders.compileShader(self.vertex_shader, GL_VERTEX_SHADER)
		fragment_shader = shaders.compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)
		self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
		self.uniforms = {}
		for name in ('model', 'transform', 'self_color', 'light_color', 'light_position', 'texture_mode'):
			self.uniforms[name] = glGetUniformLocation(self.shader, name)

	def set_light_source(self, source):
		self.light = source

	def use_shader(self):
		if self.shader == None:
			self.compile_shader()
		shaders.glUseProgram(self.shader) # pylint: disable=no-member
		for name, address in self.uniforms.items():
			if name == 'model':
				glUniformMatrix4fv(address, 1, False, np.matrix(self.model))
			if name == 'transform':
				glUniformMatrix4fv(address, 1, False, np.matrix(self.model) * np.matrix(self.perspective))
			if name == 'self_color':
				glUniform4f(address, *self.color)
			if name == 'light_color':
				glUniform3f(address, *self.light.color[:3])
			if name == 'light_position':
				glUniform3f(address, *self.light.position[:3])
			if name == 'texture_mode':
				glUniform1i(address, self.texture_mode)

	def set_texture(self, setting):
		self.texture_mode = setting
		if self.texture_mode:
			self.apply_texture()

	def apply_texture(self):
		if isinstance(self.texture, Image.Image):
			texture = self.texture
		else:
			texture = Image.open(self.texture)
		texture_data = np.flipud(np.asarray(texture)).tobytes()

		glBindVertexArray(self.VAO)
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		self.tex_id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		glTexImage2D(GL_TEXTURE_2D, 0, 4, *texture.size, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glGenerateMipmap(GL_TEXTURE_2D)

	def set_perspective(self, angle, width, height, z_min, z_max):
		self.perspective = glm.mat4(glm.perspective(angle, width / height, z_min, z_max))

	def translate(self, x, y, z):
		self.translated = glm.mat4(glm.translate(self.translated, [x, y, z]))
		self.model = self.translated * self.rotated * self.scaled
		self.get_box()
		self.position += np.array([x, y, z], np.float32)

	def rotate(self, angle, x, y, z):
		self.rotated = glm.mat4(glm.rotate(self.rotated, angle, [x, y, z]))
		self.model = self.translated * self.rotated * self.scaled
		self.get_box()

	def scale(self, x, y, z):
		self.scaled = glm.mat4(glm.scale(self.scaled, [x, y, z]))
		self.model = self.translated * self.rotated * self.scaled
		self.get_box()

	def draw(self):
		self.use_shader() # pylint: disable=no-member
		glBindVertexArray(self.VAO)
		if self.texture_mode:
			glBindTexture(GL_TEXTURE_2D, self.tex_id)
		glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
