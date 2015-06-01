import chip8, disasm, sys, os, time
from OpenGL.GLUT import *
from OpenGL.GL import *

scale = 10
gfx_width  = 64*scale
gfx_height = 32*scale
screenData = [[[0,0,0] for x in xrange(64)] for y in xrange(32)]

c8 = chip8.Chip8()
disasm = disasm.Disasm()

fps = 0
frame = 0
timebase = 0
paused = False
game_path = ''

colors = [
	[0,0,0],
	[255,255,255],
	[255,151,115],
	[0,178,92],
	[109,167,209],
	[250,105,105],
	[132,255,0],
]
background_color = 0
text_color = 1

def main(argv):
	global game_path

	if len(argv) < 2:
		sys.exit('Usage: %s chip8_game' % argv[0])
	if not os.path.exists(argv[1]):
		sys.exit('ERROR: Game %s was not found!' % argv[1])

	game_path = argv[1]

	c8.loadApplication(game_path)

	glutInit(argv)
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
	glutInitWindowSize(gfx_width, gfx_height)
	glutInitWindowPosition(320, 320)
	glutCreateWindow('Python Chip8 Emulator - ' + argv[1].split("\\")[-1])
	glutReshapeFunc(reshape)
	glutIdleFunc(glutPostRedisplay)
	glutKeyboardFunc(keyboardDown)
	glutKeyboardUpFunc(keyboardUp)
	glutSpecialFunc(processSpecialKeys)
	
	setupTexture()
	
	glutMainLoop()
	'''while 1:
		c8.emulateCycle()
		if c8.drawFlag:
			c8.debugRender()'''

def display(w, h):
	global paused

	#if c8.drawFlag:
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, w, 0, h, -1, 1)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()   
	gfx_width = w
	gfx_hight = h

	# Render
	glClearColor(0, 0, 0, 0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	if not paused:
		if not disasm.enabled:
			interval = c8.clock
			current_time = time.clock()

			if (c8.last_time + (interval/1000)) < current_time:
				c8.updateTimers()
				for ops in xrange(c8.numFrames):
					c8.emulateCycle()
					calcFps()
				if c8.drawFlag:	
				#	updateQuards()
					updateTexture()
				#	glutSwapBuffers()
					c8.drawFlag = False
				c8.last_time = current_time

	drawTexture()
	if c8.debug:
		drawDebug()
	if disasm.enabled:
		drawDisasm()
	if paused:
		drawPaused()
	#glutSwapBuffers()
	glFlush()

def updateQuards():
	global colors, text_color,background_color

	for y in xrange(32):
		for x in xrange(64):
			if c8.gfx[(y*64)+x]:
				glColor3f(colors[text_color][0], colors[text_color][1], colors[text_color][2])
			else:
				glColor3f(colors[background_color][0], colors[background_color][1], colors[background_color][2])
			drawPixel(x, y)

def drawPixel(x, y):
	glBegin(GL_QUADS)
	
	glVertex3f((x*scale)+0.0, (y * scale)+0.0, 0.0);
	glVertex3f((x*scale)+0.0, (y * scale)+scale, 0.0);
	glVertex3f((x*scale)+scale, (y * scale)+scale, 0.0);
	glVertex3f((x*scale)+scale, (y * scale)+0.0, 0.0);
	glEnd()

def setupTexture():
	glTexImage2D(GL_TEXTURE_2D, 0, 3, 64, 32, 0, GL_RGB, GL_UNSIGNED_BYTE, screenData)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glEnable(GL_TEXTURE_2D);

def updateTexture():
	global colors, text_color,background_color

	for y in xrange(32):
		for x in xrange(64):
			if c8.gfx[(y*64)+x]:
				screenData[y][x] = [colors[text_color][0], colors[text_color][1], colors[text_color][2]]
			else:
				screenData[y][x] = [colors[background_color][0], colors[background_color][1], colors[background_color][2]]
	
	glTexSubImage2D(GL_TEXTURE_2D, 0 ,0, 0, 64, 32, GL_RGB, GL_UNSIGNED_BYTE, screenData);

def drawTexture():
	glEnable(GL_TEXTURE_2D);
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
	glDisable(GL_TEXTURE_2D);

def drawDebug():
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
	glEnable( GL_BLEND )
	glBegin(GL_QUADS)
	glColor4d(0.3, 0.0, 0.3, 0.9)
	glVertex2d(gfx_width, 0.0)
	glVertex2d(gfx_width - 150.0, 0.0)
	glVertex2d(gfx_width - 150.0, gfx_height)
	glVertex2d(gfx_width, gfx_height)
	glEnd()
	glDisable(GL_BLEND)

	drawText(gfx_width - 132, gfx_height - 10 , 'Chip 8 Emulator\n     DEBUG')
	drawText(gfx_width - 140, gfx_height - 42 , 'PC: ' + hex(c8.pc) )
	drawText(gfx_width - 140, gfx_height - 58 , 'I:  ' + hex(c8.I) )
	drawText(gfx_width - 140, gfx_height - 74 , 'DT: ' + hex(c8.delay_timer) )
	drawText(gfx_width - 140, gfx_height - 90 , 'ST: ' + hex(c8.sound_timer) )
	drawText(gfx_width - 140, gfx_height - 106 , 'SP: ' + hex(c8.sp) )
	drawText(gfx_width - 140, gfx_height - 122 , 'SV: ' + hex(c8.stack[c8.sp]) )

	drawText(gfx_width - 145, gfx_height - 154 , 'V0: ' + hex(c8.V[0]) )
	drawText(gfx_width - 145, gfx_height - 170 , 'V1: ' + hex(c8.V[1]) )
	drawText(gfx_width - 145, gfx_height - 186 , 'V2: ' + hex(c8.V[2]) )
	drawText(gfx_width - 145, gfx_height - 202 , 'V3: ' + hex(c8.V[3]) )
	drawText(gfx_width - 145, gfx_height - 218 , 'V4: ' + hex(c8.V[4]) )
	drawText(gfx_width - 145, gfx_height - 234 , 'V5: ' + hex(c8.V[5]) )
	drawText(gfx_width - 145, gfx_height - 250 , 'V6: ' + hex(c8.V[6]) )
	drawText(gfx_width - 145, gfx_height - 266 , 'V7: ' + hex(c8.V[7]) )
	drawText(gfx_width - 70, gfx_height - 154 , 'V8: ' + hex(c8.V[8]) )
	drawText(gfx_width - 70, gfx_height - 170 , 'V9: ' + hex(c8.V[9]) )
	drawText(gfx_width - 70, gfx_height - 186 , 'VA: ' + hex(c8.V[10]) )
	drawText(gfx_width - 70, gfx_height - 202 , 'VB: ' + hex(c8.V[11]) )
	drawText(gfx_width - 70, gfx_height - 218 , 'VC: ' + hex(c8.V[12]) )
	drawText(gfx_width - 70, gfx_height - 234 , 'VD: ' + hex(c8.V[13]) )
	drawText(gfx_width - 70, gfx_height - 250 , 'VE: ' + hex(c8.V[14]) )
	drawText(gfx_width - 70, gfx_height - 266 , 'VF: ' + hex(c8.V[15]) )

	global fps
	drawText(gfx_width - 120, gfx_height - 295 , 'FPS: ' + "{0:.2f}".format(fps) )

def drawPaused():
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
	glEnable( GL_BLEND )
	glBegin(GL_QUADS)
	glColor4d(0, 0, 0, 0.7)
	glVertex2d(0, gfx_height)
	glVertex2d(150, gfx_height)
	glVertex2d(150, gfx_height - 16)
	glVertex2d(0, gfx_height - 16)
	glEnd()
	glDisable(GL_BLEND)
	drawText(2, gfx_height - 12, 'Interpreter Paused' )

def drawDisasm():
	y = 16
	j = 7
	if disasm.currentSel < disasm.pageSize:
		y = disasm.currentSel
		j = y / 2 - 1
	if disasm.currentSel > (disasm.maxEntry - disasm.pageSize):
		y = 32 - (disasm.maxEntry - disasm.currentSel + 1)
		j = y / 2 - 1
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
	glEnable( GL_BLEND )
	glBegin(GL_QUADS)
	glColor4d(0, 0, 0, 0.9)
	glVertex2d(0, gfx_height)
	glVertex2d(gfx_width - 150, gfx_height)
	glVertex2d(gfx_width - 150, 0)
	glVertex2d(0, 0)
	glEnd()
	glBegin(GL_QUADS)
	glColor4d(0.5, 1, 0, 0.8)
	glVertex2d(10, gfx_height - 46 - (j * 16))
	glVertex2d(gfx_width - 160, gfx_height - 46 - (j * 16))
	glVertex2d(gfx_width - 160, gfx_height - 46 - ((j + 1) * 16))
	glVertex2d(10, gfx_height - 46 - ((j + 1) * 16))
	glEnd()
	glDisable(GL_BLEND)
	drawText(220, gfx_height - 16, 'DISASSEMBLER')
	for x in xrange(disasm.pageSize):
		if ((disasm.currentSel - y) + (x * 2) + 1) == 4096:
			op = c8.memory[4095]
		else:
			op = c8.memory[(disasm.currentSel - y) + (x * 2)] << 8 | c8.memory[(disasm.currentSel - y) + (x * 2) + 1]
		drawText(20, gfx_height - 42 - (x * 16), '0x{:04x}'.format((disasm.currentSel - y) + (x * 2)).upper() + ':  ' + '{:04x}'.format(op).upper() + '  ' + str(disasm.getOpText(op)))

def drawText(x,y,string):
	glColor3d(1.0, 1.0, 1.0)
	glRasterPos2f(x,y)
	glutBitmapString(GLUT_BITMAP_8_BY_13, string)

def calcFps():
	global frame, timebase, fps

	frame += 1
	time = glutGet( GLUT_ELAPSED_TIME)
	if (time - timebase) > 1000:
		fps = frame * 1000.0 / (time - timebase)
		timebase = time
		frame = 0

def reshape(w, h):
	glutDisplayFunc(lambda: display(w, h))
	glutPostRedisplay();

def keyboardDown(key, x, y):
	global text_color,background_color, paused

	if key is chr(27): sys.exit(1)

	if key is '1': c8.key[0x1] = 1
	elif key is '2': c8.key[0x2] = 1
	elif key is '3': c8.key[0x3] = 1
	elif key is '4': c8.key[0xC] = 1

	elif key is 'q': c8.key[0x4] = 1
	elif key is 'w': c8.key[0x5] = 1	
	elif key is 'e': c8.key[0x6] = 1
	elif key is 'r': c8.key[0xD] = 1

	elif key is 'a': c8.key[0x7] = 1
	elif key is 's': c8.key[0x8] = 1
	elif key is 'd': c8.key[0x9] = 1
	elif key is 'f': c8.key[0xE] = 1

	elif key is 'z': c8.key[0xA] = 1
	elif key is 'e': c8.key[0x0] = 1
	elif key is 'c': c8.key[0xB] = 1
	elif key is 'v': c8.key[0xF] = 1

	elif key is '0': 
		if not disasm.enabled:
			c8.debug ^= 1
	elif key is '9': 
		c8.reset()
		c8.loadApplication(game_path)
	elif key is '8': 
		if text_color is 1 and background_color is 0:
			text_color = 6
		elif text_color is 6: 
			text_color = 1
			background_color = 2
		else:
			background_color += 1
			if background_color > 5:
				background_color = 0
	elif key is '-': 
		if not disasm.enabled:
			paused ^= 1
	elif key is '`':
		if not disasm.enabled:
			paused = True
			c8.debug = True
		else:
			paused = False
			c8.debug = False
		disasm.enabled ^=1
		disasm.currentSel = 0x200
	elif key is chr(13):
		c8.emulateCycle()
		disasm.currentSel = c8.pc
		calcFps()
		if c8.drawFlag:
		#	updateQuards()
			updateTexture()
			c8.drawFlag = False

def keyboardUp(key, x ,y):
	if key is '1': c8.key[0x1] = 0
	elif key is '2': c8.key[0x2] = 0
	elif key is '3': c8.key[0x3] = 0
	elif key is '4': c8.key[0xC] = 0

	elif key is 'q': c8.key[0x4] = 0
	elif key is 'w': c8.key[0x5] = 0
	elif key is 'e': c8.key[0x6] = 0
	elif key is 'r': c8.key[0xD] = 0

	elif key is 'a': c8.key[0x7] = 0
	elif key is 's': c8.key[0x8] = 0
	elif key is 'd': c8.key[0x9] = 0
	elif key is 'f': c8.key[0xE] = 0

	elif key is 'z': c8.key[0xA] = 0
	elif key is 'e': c8.key[0x0] = 0
	elif key is 'c': c8.key[0xB] = 0
	elif key is 'v': c8.key[0xF] = 0

def processSpecialKeys(key, x, y):
	if disasm.enabled:
		if key == GLUT_KEY_HOME:
			if disasm.currentSel != 0x200:
				disasm.currentSel = 0x200
			else:
				disasm.currentSel = 0x000
		elif key == GLUT_KEY_END:
			disasm.currentSel = 0xFFF
		elif key == GLUT_KEY_UP:
			if disasm.currentSel > 0:
				disasm.currentSel -= 2
		elif key == GLUT_KEY_DOWN:
			if disasm.currentSel < disasm.maxEntry:
				disasm.currentSel += 2

if __name__ == "__main__":
	sys.exit(main(sys.argv))