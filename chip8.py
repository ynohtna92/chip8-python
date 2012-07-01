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

	def emulateCycle(self):
			self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
			print self.opcode, ' ' , self.pc
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
		print 'x0NNN'
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
                print 'x8NNN'
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
                print 'xENNN'
        def xFNNN(self):
                print 'xFNNN'
