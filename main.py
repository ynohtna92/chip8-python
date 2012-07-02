import chip8, sys, os
from OpenGL.GLUT import *
from OpenGL.GL import *

scale = 10
gfx_width  = 64*scale
gfx_height = 32*scale
screenData=[[[0,0,0] for x in range(64)] for y in range(32)]

c8= chip8.Chip8()

def main(argv):
	if len(argv) < 2:
		sys.exit('Usage: %s chip8_game' % argv[0])
	if not os.path.exists(argv[1]):
		sys.exit('ERROR: Game %s was not found!' % argv[1])

	game_path = argv[1]
	
	c8.loadApplication(game_path)
	
	glutInit(argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(gfx_width, gfx_height)
	glutInitWindowPosition(320, 320)
	glutCreateWindow('Python Chip8 Emulator')
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutIdleFunc(display)
	'''glutKeyboardFunc(keyboardDown)
	glutKeyboardUpFunc(keyboardUp)'''
	
	setupTexture()
	
	glutMainLoop()
	'''while 1:
		c8.emulateCycle()
		if c8.drawFlag:
			c8.debugRender()'''

def display():
	c8.emulateCycle()
	if c8.drawFlag:
		glClear(GL_COLOR_BUFFER_BIT)
		'''updateQuards()'''
		updateTexture()
		
		glutSwapBuffers()
		c8.drawFlag = False

def updateQuards():
	for y in range(32)[::-1]:
		for x in range(64)[::-1]:
			if c8.gfx[(y*64)+x]:
				glColor3f(1.0, 1.0, 1.0)
			else:
				glColor3f(0.0, 0.0, 0.0)
			drawPixel(x, y)
def drawPixel(x, y):
	glBegin(GL_QUADS)
	
	glVertex3f((x*scale)+0.0,     (y * scale)+0.0,     0.0);
	glVertex3f((x*scale)+0.0,     (y * scale)+scale, 0.0);
	glVertex3f((x*scale)+scale, (y * scale)+scale, 0.0);
	glVertex3f((x*scale)+scale, (y * scale)+0.0,     0.0);
	glEnd()

def setupTexture():
	glTexImage2D(GL_TEXTURE_2D, 0, 3, 64, 32, 0, GL_RGB, GL_UNSIGNED_BYTE, screenData)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glEnable(GL_TEXTURE_2D);

def updateTexture():
        for y in range(32):
                for x in range(64):
                        if c8.gfx[(y*64)+x]:
                                screenData[y][x] = [255, 255, 255]
                        else:
                                screenData[y][x] = [0, 0, 0]
	
	glTexSubImage2D(GL_TEXTURE_2D, 0 ,0, 0, 64, 32, GL_RGB, GL_UNSIGNED_BYTE, screenData);
	
	glBegin(GL_QUADS)
	glTexCoord2d(0.0, 1.0)
	glVertex2d(0.0, 0.0)
	glTexCoord2d(1.0, 1.0)
	glVertex2d(gfx_width, 0.0)
	glTexCoord2d(1.0, 0.0)
	glVertex2d(gfx_width, gfx_height)
	glTexCoord2d(0.0, 0.0)
	glVertex2d(0.0, gfx_height)
	glEnd()

def reshape(w, h):
   glViewport(0, 0, w, h)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0, w, 0, h, -1.0, 1.0)
   glMatrixMode(GL_MODELVIEW)
   gfx_width = w
   gfx_hight =h

def keyboardDown():
	pass
def keyboardUp():
	pass
if __name__ == "__main__":
	sys.exit(main(sys.argv))
