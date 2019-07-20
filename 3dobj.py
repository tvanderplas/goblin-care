
import pygame
from pygame.locals import * # pylint: disable=unused-wildcard-import
from OpenGL.GL import * # pylint: disable=unused-wildcard-import
from OpenGL.GLU import * # pylint: disable=unused-wildcard-import
from objloader import Obj, Mtl
import numpy as np

def main():
	pygame.init() # pylint: disable=no-member
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # pylint: disable=undefined-variable
	
	care = Obj('care.obj')

	glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

	gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
	glTranslatef(0.0, 0.0, -50)
	glRotatef(30, 1, 0, 0)
	while True:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT: # pylint: disable=undefined-variable
				pygame.quit() # pylint: disable=no-member
				quit()
		
		# glRotatef(1, 0, 1, 0)
		glCallList(care.gl_list)
		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		pygame.time.wait(10)

if __name__ == '__main__':
	main()
