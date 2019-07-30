
import pygame
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
import numpy as np

def Mtl(filename):
	contents = {}
	mtl = None
	for line in open(filename, "r"):
		if line.startswith('#'): continue
		values = line.split()
		if not values: continue
		if values[0] == 'newmtl':
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
		self.vertices = []
		self.normals = []
		self.texcoords = []
		self.faces = []
		self.colors = [
			[0, 0, 0],
			[1, 0, 0],
			[0, 1, 0],
			[0, 0, 1],
			[1, 1, 0],
			[1, 0, 1],
			[0, 1, 1],
			[1, 1, 1]
		]

		material = None
		for line in open(filename, "r"):
			if line.startswith('#'): continue
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				v = list(map(float, values[1:4]))
				if swapyz:
					v = v[0], v[2], v[1]
				self.vertices.append(v)
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
		self.indices = np.array([i[0] for i in self.faces], dtype=np.int32).flatten()
		self.indices -= 1 # change from 1-indexed to 0-indexed
		self.vertices = np.array([i + j for i, j in zip(self.vertices, self.colors)], dtype=np.float32)

	def generate(self):
		self.VAO, self.VBO, self.EBO = GLuint(), GLuint(), GLuint()
		glGenVertexArrays(1, id(self.VAO))
		self.VBO = glGenBuffers(1)
		self.EBO = glGenBuffers(1)
		glBindVertexArray(self.VAO)

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, None)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
		glEnableVertexAttribArray(0)
		glEnableVertexAttribArray(1)
