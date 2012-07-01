# -*- coding: utf-8 -*-
import os
from random import randint

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

		self.delay_timer = 0
		self.sound_timer = 0
		
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
			except KeyError:
				print 'opcode error'
			if self.delay_timer > 0:
				self.delay_timer-=1
			if self.sound_timer > 0:
				if self.sound_timer is 1:
					print 'beep!'
				self.sound_timer-=1

	def debugRender(self):
		for y in range(32):
			for x in range(64):
				if self.gfx[(y*64)+x]:
				   print '0',
				else:
				   print ' ',
			print ''
		print ''
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
		self.pc = self.opcode & 0x0FFF;
        def x2NNN(self):
                print 'x2NNN'
		self.stack[self.sp] = self.pc
		self.pc+=1
		self.pc = self.opcode & 0x0FFF
        def x3NNN(self):
                print 'x3NNN'
		if self.V[(self.opcode & 0x0F00) >> 8] is (self.opcode & 0x00FF):
			self.pc +=4
		else:
			self.pc +=2
        def x4NNN(self):
                print 'x4NNN'
                if self.V[(self.opcode & 0x0F00) >> 8] is not (self.opcode & 0x00FF):
                        self.pc +=4
                else:
                        self.pc +=2
        def x5NNN(self):
                print 'x5NNN'
                if self.V[(self.opcode & 0x0F00) >> 8] is self.V[(self.opcode & 0x00F0) >> 4]:
                        self.pc +=4
                else:
                        self.pc +=2
        def x6NNN(self):
                print 'x6NNN'
		self.V[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
		self.pc += 2
        def x7NNN(self):
                print 'x7NNN'
                self.V[(self.opcode & 0x0F00) >> 8] += self.opcode & 0x00FF
                self.pc += 2
        def x8NNN(self):
                try:
                        self.case_0x8000[self.opcode & 0x000F]()
                except KeyError:
                        print 'opcode error 0x8NNN'
        def x9NNN(self):
                print 'x9NNN'
		if self.V[(self.opcode & 0x0F00) >> 8] is not self.V[(self.opcode & 0x00F0) >> 4]:
                        self.pc +=4
                else:
                        self.pc +=2
        def xANNN(self):
                print 'xANNN'
		self.I = self.opcode & 0x0FFF
		self.pc +=2
        def xBNNN(self):
                print 'xBNNN'
		self.pc = (self.opcode & 0x0FFF)+self.V[0]
        def xCNNN(self):
                print 'xCNNN'
		self.V[(self.opcode & 0x0F00) >> 8] = (randint(1,32767) % 0xFF) & (self.opcode & 0x00FF)
		self.pc +=2
        def xDNNN(self):
                print 'xDNNN'
		x=self.V[(self.opcode & 0x0F00) >> 8]
		y=self.V[(self.opcode & 0x00F0) >> 4]
		height = self.opcode & 0x000F
		pixel = 0

		self.V[0xF] = 0
		
		for yline in range(height):
			pixel = self.memory[self.I+yline]
			for xline in range(8):
				if (pixel & ( 0x80 >> xline)) is not 0:
					print (x + xline + ((y+yline)*64)), 'nyan', x , xline ,y, yline
					if self.gfx[(x + xline + ((y+yline)*64))]:
						V[0xF] = 1
					self.gfx[(x + xline + ((y+yline)*64))] ^= 1
		self.drawFlag = True;
		self.pc +=2;
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
		self.gfx = [0x0 for x in range(64*32)]
		self.drawFlag=True
		self.pc+=2
        def x000E(self):
                print 'x000E'
		self.sp-=1
		self.pc=self.stack[self.sp]
		self.pc+=2

	'''x8NNN case'''
        def x8XY0(self):
                print 'x8XY0'
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4]
		self.pc +=2
        def x8XY1(self):
                print 'x8XY1'
                self.V[(self.opcode & 0x0F00) >> 8] |= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc +=2
        def x8XY2(self):
                print 'x8XY2'
                self.V[(self.opcode & 0x0F00) >> 8] &= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc +=2
        def x8XY3(self):
                print 'x8XY3'
                self.V[(self.opcode & 0x0F00) >> 8] ^= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc +=2
        def x8XY4(self):
                print 'x8XY4'
		if self.V[(self.opcode & 0x00F0) >> 4] > (0xFF - self.V[(self.opcode & 0x0F00) >> 8]):
			self.V[0xF]=1
		else:
			self.V[0xF]=0
		self.V[(self.opcode & 0x0F00) >> 8] += self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
        def x8XY5(self):
                print 'x8XY5'
                if self.V[(self.opcode & 0x00F0) >> 4] > self.V[(self.opcode & 0x0F00) >> 8]:
                        self.V[0xF]=0
                else:
                        self.V[0xF]=1
                self.V[(self.opcode & 0x0F00) >> 8] -= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2

        def x8XY6(self):
                print 'x8XY6'
		self.V[0xF]=self.V[(self.opcode & 0x0F00) >> 8] & 0x1
		self.V[(self.opcode & 0x0F00) >> 8] >>=1
		self.pc +=2
        def x8XY7(self):
                print 'x8XY7'
		if self.V[(self.opcode & 0x0F00) >> 8] > self.V[(self.opcode & 0x00F0) >> 4]:
			self.V[0xF] = 0
		else:
			self.V[0xF] = 1
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4] - self.V[(self.opcode & 0x0F00) >> 8]
		self.pc+=2
        def x8XYE(self):
                print 'x8XYE'
		self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] >> 7
		self.V[(self.opcode & 0x0F00) >> 8] <<=1
		pc+=2

	'''xENNN case'''
        def xEX9E(self):
                print 'xEX9E'
		if self.key[self.V[(self.opcode & 0x0F00) >> 8]] is not 0:
			self.pc+=4
		else:
			self.pc+=2
        def xEXA1(self):
                print 'xEXA1'
                if self.key[self.V[(self.opcode & 0x0F00) >> 8]] is 0:
                        self.pc+=4
                else:
                        self.pc+=2

	'''xFNNN case'''
        def xFX07(self):
                print 'xFX07'
		self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer
		self.pc+=2
        def xFX0A(self):
                print 'xFX0A'
		keyPress = False

		for i in range(16):
			if self.key[i] is not 0:
				self.V[(self.opcode & 0x0F00) >> 8] = i
				keyPress = True
		if not keyPress:
			return
		self.pc+=2
        def xFX15(self):
                print 'xFX15'
		self.delay_timer = self.V[(self.opcode & 0x0F00) >> 8]
		self.pc+=2
        def xFX18(self):
                print 'xFX18'
                self.sound_timer = self.V[(self.opcode & 0x0F00) >> 8]
                self.pc+=2
        def xFX1E(self):
                print 'xFX1E'
		if (self.I+self.V[(self.opcode & 0x0F00) >> 8]) > 0xFFF:
			self.V[0xF]=1
		else:
			self.V[0xF]=0
		self.I += self.V[(self.opcode & 0x0F00) >> 8]
		self.pc+=2
        def xFX29(self):
                print 'xFX29'
		self.I = self.V[(self.opcode & 0x0F00) >> 8] *0x5
		self.pc+=2
        def xFX33(self):
                print 'xFX33'
		self.memory[I] = self.V[(self.opcode & 0x0F00) >> 8] / 100
		self.memory[I+1] = (self.V[(self.opcode & 0x0F00) >> 8] / 10) % 10
		self.memory[I+2] = (self.V[(self.opcode & 0x0F00) >> 8] % 100) % 10
		self.pc+=2
        def xFX65(self):
                print 'xFX65'
		for i in range(((self.opcode & 0x0F00) >> 8)+1):
			self.V[i] = self.memory[self.I+i]
		self.I += ((self.opcode & 0x0F00) >> 8)+1
		self.pc+=2	
        def xFX55(self):
                print 'xFX55'
                for i in range(((self.opcode & 0x0F00) >> 8)+1):
                        self.memory[self.I+i] = self.V[i]
                self.I += ((self.opcode & 0x0F00) >> 8)+1 
                self.pc+=2
