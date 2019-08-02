
import pygame
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
import numpy as np
import glm
from math import pi
from ast import literal_eval
import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))

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

def Mtl(filename):
	contents = {}
	mtl = None
	for line in open(filename, "r"):
		if line.startswith('#'): continue
		values = line.split()
		if not values: continue
		if values[0] == 'newmtl':
			if values[1][:5] == 'color':
				contents.update(color=values[1][6::])
			mtl = contents[values[1]] = {}
		elif mtl is None:
			raise ValueError("mtl file doesn't start with newmtl stmt")
		elif values[0] == 'map_Kd':
			# load the texture referred to by this declaration
			mtl[values[0]] = values[1] # pylint: disable=unsupported-assignment-operation
			surf = pygame.image.load(mtl['map_Kd']) # pylint: disable=unsubscriptable-object
			image = pygame.image.tostring(surf, 'RGBA', 1)
			ix, iy = surf.get_rect().size
			texid = mtl['texture_Kd'] = glGenTextures(1) # pylint: disable=unsupported-assignment-operation
			glBindTexture(GL_TEXTURE_2D, texid)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
				GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
				GL_LINEAR)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
				GL_UNSIGNED_BYTE, image)
		else:
			mtl[values[0]] = list(map(float, values[1:])) # pylint: disable=unsupported-assignment-operation
	return contents

class Obj:
	def __init__(self, filename, swapyz=False):
		"""Loads a Wavefront OBJ file. """
		self.points = [] # only unique positions
		self.vertex_info = [] # unique combinations of position, normal and color
		self.normals = []
		self.texcoords = []
		self.faces = []
		self.model = np.matrix(identity, np.float32)
		self.perspective = PERSPECTIVE
		obj_list.append(self)
		self.position = np.array([0, 0, 0], np.float32)

		material = None
		print(filename)
		for line in open(filename, "r"):
			if line.startswith('#'): continue
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				v = list(map(float, values[1:4]))
				if swapyz:
					v = v[0], v[2], v[1]
				self.points.append(v)
			elif values[0] == 'vn':
				v = list(map(float, values[1:4]))
				if swapyz:
					v = v[0], v[2], v[1]
				self.normals.append(v)
			elif values[0] == 'vt':
				self.texcoords.append(map(float, values[1:3]))
			elif values[0] in ('usemtl', 'usemat'):
				material = values[1]
			elif values[0] == 'mtllib':
				self.mtl = Mtl(values[1])
			elif values[0] == 'f':
				face = []
				texcoords = []
				norms = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0]))
					if len(w) >= 2 and len(w[1]) > 0:
						texcoords.append(int(w[1]))
					else:
						texcoords.append(0)
					if len(w) >= 3 and len(w[2]) > 0:
						norms.append(int(w[2]))
					else:
						norms.append(0)
				self.faces.append((face, norms, texcoords, material))
		color = self.mtl.get('color', [.5, .5, .5])
		if isinstance(color, str):
			self.color = [int(color[i:i+2], 16) / 256 for i in (0, 2, 4)]
		self.indices = [f[0] for f in self.faces]
		self.faces = [self.indices[i] + self.normals[i] for i in range(len(self.indices))]
		vertex_info = {}
		for i, face in enumerate(self.faces):
			for j, vertex in enumerate([*[self.points[i - 1] + face[3:] + self.color for i in face[:3]]]):
				strung = str(vertex)
				if strung in vertex_info:
					self.indices[i][j] = vertex_info[strung]
				else:
					self.indices[i][j] = len(vertex_info)
					vertex_info[strung] = self.indices[i][j]
		for i in vertex_info.keys():
			self.vertex_info.append(literal_eval(i))
		self.vertex_info = np.array(self.vertex_info, np.float32)
		self.indices = np.array(self.indices, np.int32).flatten()

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

		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, None)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
		glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
		glEnableVertexAttribArray(0)
		glEnableVertexAttribArray(1)
		glEnableVertexAttribArray(2)
		glBindVertexArray(0)

	def set_perspective(self, angle, width, height, z_min, z_max):
		self.perspective = np.matrix(glm.perspective(angle, width / height, z_min, z_max), np.float32)

	def translate(self, x, y, z):
		self.model = np.matrix(glm.translate(self.model, [x, y, z]), np.float32)
		self.position += np.array([x, y, z], np.float32)

	def rotate(self, angle, x, y, z):
		self.model = np.matrix(glm.rotate(self.model, angle, [x, y, z]), np.float32)

	def scale(self, x, y, z):
		self.model = np.matrix(glm.scale(self.model, [x, y, z]), np.float32)
