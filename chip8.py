# -*- coding: utf-8 -*-
import os

chip8_fontset =(
    0xF0, 0x90, 0x90, 0x90, 0xF0,
    0x20, 0x60, 0x20, 0x20, 0x70,
    0xF0, 0x10, 0xF0, 0x80, 0xF0,
    0xF0, 0x10, 0xF0, 0x10, 0xF0,
    0x90, 0x90, 0xF0, 0x10, 0x10,
    0xF0, 0x80, 0xF0, 0x10, 0xF0,
    0xF0, 0x80, 0xF0, 0x90, 0xF0,
    0xF0, 0x10, 0x20, 0x40, 0x40,
    0xF0, 0x90, 0xF0, 0x90, 0xF0,
    0xF0, 0x90, 0xF0, 0x10, 0xF0,
    0xF0, 0x90, 0xF0, 0x90, 0x90,
    0xE0, 0x90, 0xE0, 0x90, 0xE0,
    0xF0, 0x80, 0x80, 0x80, 0xF0,
    0xE0, 0x90, 0x90, 0x90, 0xE0,
    0xF0, 0x80, 0xF0, 0x80, 0xF0,
    0xF0, 0x80, 0xF0, 0x80, 0x80
		)

class Chip8:
	def __init__(self):
		self.pc = 0x200
		self.opcode = 0
		self.I = 0
		self.sp = 0

		self.gfx = [0 for x in range(64*32)]
		self.stack = [0 for x in range(16)]
		self.key = [0 for x in range(16)]
		self.memory = [0 for x in range(4096)]
		self.V = [0 for x in range(16)]

		'''remove this'''
		self.debug_len = 0

		delay_timer = 0
		sound_timer = 0
		
		self.drawFlag = True
		for i in range(len(chip8_fontset)):
			self.memory[i]= chip8_fontset[i]
		
		self.case_main = {
                        0x0000: self.x0NNN,
                        0x1000: self.x1NNN,
                        0x2000: self.x2NNN,
                        0x3000: self.x3NNN,
                        0x4000: self.x4NNN,
                        0x5000: self.x5NNN,
			0x6000: self.x6NNN,
			0x7000: self.x7NNN,
			0x8000: self.x8NNN,
			0x9000: self.x9NNN,
			0xA000: self.xANNN,
			0xB000: self.xBNNN,
			0xC000: self.xCNNN,
			0xD000: self.xDNNN,
			0xE000: self.xENNN,
			0xF000: self.xFNNN,
                }
		self.case_0x0000 = {
			0x0000: self.x00E0,
			0x000E: self.x000E
		}
		self.case_0x8000 = {
			0x0000: self.x8XY0,
			0x0001: self.x8XY1,
			0x0002: self.x8XY2,
			0x0003: self.x8XY3,
			0x0004: self.x8XY4,
			0x0005: self.x8XY5,
			0x0006: self.x8XY6,
			0x0007: self.x8XY7,
			0x000E: self.x8XYE
		}
		self.case_0xE000 = {
                        0x009E: self.xEX9E,
                        0x000A: self.xEXA1
		}
		self.case_0xF000 = {
			0x0007: self.xFX07,
			0x000A: self.xFX0A,
			0x0015: self.xFX15,
			0x0018: self.xFX18,
			0x001E: self.xFX1E,
			0x0029: self.xFX29,
			0x0033: self.xFX33,
			0x0055: self.xFX55,
			0x0065: self.xFX65,
		}

	def emulateCycle(self):
			self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
			print hex(self.opcode), ' ', 
			try:
				self.case_main[self.opcode & 0xF000]()
				self.pc +=2
			except KeyError:
				print 'opcode error'

	def debugRender(self):
		'''for y in range(32):
			for x in range(64):
				if self.gfx[(y*64)+x]:
				   print '0',
				else:
				   print ' ',
			print ''
		print '''
		pass

	def loadApplication(self, file_name):
		buffer_app = []
		app_file = open(file_name,'rb')
		for b in app_file.read():
			buffer_app.append(int(b.encode('hex'), 16))
		self.debug_len = len(buffer_app)
		for i in range(len(buffer_app)):
			self.memory[i+512]=buffer_app[i]
		app_file.close()

	def x0NNN(self):
		try:
			self.case_0x0000[self.opcode & 0x000F]()
		except KeyError:
			print 'opcode error 0x0NNN'
        def x1NNN(self):
                print 'x1NNN'
        def x2NNN(self):
                print 'x2NNN'
        def x3NNN(self):
                print 'x3NNN'
        def x4NNN(self):
                print 'x4NNN'
        def x5NNN(self):
                print 'x5NNN'
        def x6NNN(self):
                print 'x6NNN'
        def x7NNN(self):
                print 'x7NNN'
        def x8NNN(self):
                try:
                        self.case_0x8000[self.opcode & 0x000F]()
                except KeyError:
                        print 'opcode error 0x8NNN'
        def x9NNN(self):
                print 'x9NNN'
        def xANNN(self):
                print 'xANNN'
        def xBNNN(self):
                print 'xBNNN'
        def xCNNN(self):
                print 'xCNNN'
        def xDNNN(self):
                print 'xDNNN'
        def xENNN(self):
                try:
                        self.case_0xE000[self.opcode & 0x00FF]()
                except KeyError:
                        print 'opcode error 0xENNN'
        def xFNNN(self):
                try:
                        self.case_0xF000[self.opcode & 0x00FF]()
                except KeyError:
                        print 'opcode error 0xFNNN'

	'''0NNN case'''
        def x00E0(self):
                print 'x00E0'
        def x000E(self):
                print 'x000E'

	'''x8NNN case'''
        def x8XY0(self):
                print 'x8XY0'
        def x8XY1(self):
                print 'x8XY1'
        def x8XY2(self):
                print 'x8XY2'
        def x8XY3(self):
                print 'x8XY3'
        def x8XY4(self):
                print 'x8XY4'
        def x8XY5(self):
                print 'x8XY5'
        def x8XY6(self):
                print 'x8XY6'
        def x8XY7(self):
                print 'x8XY7'
        def x8XYE(self):
                print 'x8XYE'

	'''xENNN case'''
        def xEX9E(self):
                print 'xEX9E'
        def xEXA1(self):
                print 'xEXA1'

	'''xFNNN case'''
        def xFX07(self):
                print 'xFX07'
        def xFX0A(self):
                print 'xFX0A'
        def xFX15(self):
                print 'xFX15'
        def xFX18(self):
                print 'xFX18'
        def xFX1E(self):
                print 'xFX1E'
        def xFX29(self):
                print 'xFX29'
        def xFX33(self):
                print 'xFX33'
        def xFX55(self):
                print 'xFX55'
        def xFX65(self):
                print 'xFX65'
