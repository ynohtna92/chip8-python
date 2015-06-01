#!/usr/bin/env python
# coding: utf8

# Chip8 Emulator
# Authored by ynohtna92

import os, time
from random import randint

chip8_fontset = (
	0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
	0x20, 0x60, 0x20, 0x20, 0x70, # 1
	0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
	0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
	0x90, 0x90, 0xF0, 0x10, 0x10, # 4
	0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
	0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
	0xF0, 0x10, 0x20, 0x40, 0x40, # 7
	0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
	0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
	0xF0, 0x90, 0xF0, 0x90, 0x90, # A
	0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
	0xF0, 0x80, 0x80, 0x80, 0xF0, # C
	0xE0, 0x90, 0x90, 0x90, 0xE0, # D
	0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
	0xF0, 0x80, 0xF0, 0x80, 0x80  # F
	)

TARGET_FPS = 60
CYC_60HZ = 16.67
PC_BEGIN = 0x200

class Chip8:
	def __init__(self):
		# TODO Superchip opcodes
		self.debug = True

		self.pc = PC_BEGIN
		self.opcode = 0
		self.I = 0
		self.V = [0]*16 # 0 -> F
		self.stack = [0]*16
		self.sp = 0

		self.clock = CYC_60HZ
		self.last_time = 0
		self.numOps = 480
		self.numFrames = self.numOps / TARGET_FPS

		self.memory = [0]*4096 # 0x000-0x1FF chip8 interpreter font Set 
							   # 0x050-0x0A0 built in 4x5 pixel font set
							   # 0x200-0xFFF Program ROM and work RAM

		self.gfx = [0]*64*32

		self.delay_timer = 0
		self.sound_timer = 0

		self.key = [0]*16
		self.drawFlag = True
		for i in xrange(len(chip8_fontset)):
			self.memory[i] = chip8_fontset[i]	# Load fontset into memory

		self.opcodes_main = {
			0x0000: self.x0NNN,
			0x1000: self.x1NNN,
			0x2000: self.x2NNN,
			0x3000: self.x3XNN,
			0x4000: self.x4XNN,
			0x5000: self.x5XY0,
			0x6000: self.x6XNN,
			0x7000: self.x7XNN,
			0x8000: self.x8NNN,
			0x9000: self.x9XY0,
			0xA000: self.xANNN,
			0xB000: self.xBNNN,
			0xC000: self.xCXNN,
			0xD000: self.xDXYN,
			0xE000: self.xENNN,
			0xF000: self.xFNNN,
		}

		self.opcodes_0x0000 = {
			0x0000: self.x00E0,
			0x000E: self.x00EE,
		}

		self.opcodes_0x8000 = {
			0x0000: self.x8XY0,
			0x0001: self.x8XY1,
			0x0002: self.x8XY2,
			0x0003: self.x8XY3,
			0x0004: self.x8XY4,
			0x0005: self.x8XY5,
			0x0006: self.x8XY6,
			0x0007: self.x8XY7,
			0x000E: self.x8XYE,
		}

		self.opcodes_0xE000 = {
			0x000E: self.xEX9E,
			0x0001: self.xEXA1,
		}

		self.opcodes_0xF000 = {
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

	def overflowRegister(self): # Overflow registers that exceed 0xFF
		for i in xrange(16):
			if self.V[i] > 255:
				self.V[i] -= 256

	def calcRomChecksum(self):
		chk = 0
		for i in range(0x200,0xFFF):
			chk += self.memory[i]
		if chk > 65535:
			chk -= 65536
		return chk

	def emulateCycle(self):
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1] 	# Fetch Opcode
		#print hex(self.opcode)
		try:
			self.opcodes_main[self.opcode & 0xF000]()
		except KeyError:
			print 'Opcode Error: ' + hex(self.opcode)
			self.pc += 2

		self.overflowRegister()

	def updateTimers(self):
		if self.delay_timer > 0:
			self.delay_timer -= 1
		if self.sound_timer > 0:
			if self.sound_timer is 1:
				print 'Beep!'
			self.sound_timer -= 1

	def reset(self):
		self.pc = PC_BEGIN
		self.opcode = 0
		self.I = 0
		self.V = [0]*16 # 0 -> F
		self.stack = [0]*16
		self.sp = 0

		self.memory = [0]*4096 # 0x000-0x1FF chip8 interpreter font Set 
							   # 0x050-0x0A0 built in 4x5 pixel font set
							   # 0x200-0xFFF Program ROM and work RAM

		self.gfx = [0]*64*32

		self.delay_timer = 0
		self.sound_timer = 0

		self.key = [0]*16
		self.drawFlag = True
		for i in xrange(len(chip8_fontset)):
			self.memory[i] = chip8_fontset[i]	# Load fontset into memory

	def loadApplication(self, file_name):
		buffer_app = []
		app_file = open(file_name,'rb')
		for b in app_file.read():
			buffer_app.append(int(b.encode('hex'), 16))
		for i in xrange(len(buffer_app)):
			self.memory[i+512]=buffer_app[i]
		app_file.close()

		self.setOps(self.calcRomChecksum())

	def setOps(self, chk): # Set ops for the specific Rom detected.
		if chk == 0xE103:
			self.numOps = 1080
		elif chk == 0x689F:
			self.numOps = 480

		self.numFrames = self.numOps / TARGET_FPS

	def gfxGet(self, x, y):
		if x >= 64:
			x = x - 64
		if y >= 32:
			y = y - 32
		return self.gfx[x + (y * 64)]

	def gfxSet(self, x, y):
		if x >= 64:
			x = x - 64
		if y >= 32:
			y = y - 32
		self.gfx[x + (y * 64)] ^= 1

	def x0NNN(self): # Calls RCA 1802 program at address NNN.
		try:
			self.opcodes_0x0000[self.opcode & 0x000F]()
		except KeyError:
			print 'Unknown opcode [0x0NNN]: ' + hex(self.opcode)
			self.pc += 2

	def x1NNN(self): # Jumps to address NNN.
		self.pc = self.opcode & 0x0FFF

	def x2NNN(self): # Calls subroutine at NNN.
		if self.sp < 16:
			self.stack[self.sp] = self.pc
			self.sp += 1
			self.pc = self.opcode & 0x0FFF

	def x3XNN(self): # Skips the next instruction if VX equals NN.
		if self.V[(self.opcode & 0x0F00) >> 8] is (self.opcode & 0x00FF):
			self.pc += 4
		else:
			self.pc += 2

	def x4XNN(self): # Skips the next instruction if VX doesn't equal NN.
		if self.V[(self.opcode & 0x0F00) >> 8] is not (self.opcode & 0x00FF):
			self.pc += 4
		else:
			self.pc += 2

	def x5XY0(self): # Skips the next instruction if VX equals VY.
		if self.V[(self.opcode & 0x0F00) >> 8] is self.V[(self.opcode & 0x00F0) >> 4]:
			self.pc += 4
		else:
			self.pc += 2

	def x6XNN(self): # Sets VX to NN.
		self.V[(self.opcode & 0x0F00) >> 8] = (self.opcode & 0x00FF)
		self.pc += 2

	def x7XNN(self): # Adds NN to VX.
		self.V[(self.opcode & 0x0F00) >> 8] += (self.opcode & 0x00FF)
		self.pc += 2

	def x8NNN(self): # Calls RCA 1802 program at address NNN.
		try:
			self.opcodes_0x8000[self.opcode & 0x000F]()
		except KeyError:
			print 'Unknown opcode [0x8NNN]: ' + hex(self.opcode)
			self.pc += 2

	def x9XY0(self): # Skips the next instruction if VX doesn't equal VY.
		if self.V[(self.opcode & 0x0F00) >> 8] is not self.V[(self.opcode & 0x00F0) >> 4]:
			self.pc += 4
		else:
			self.pc += 2

	def xANNN(self): # Sets I to the address NNN.
		self.I = self.opcode & 0x0FFF
		self.pc += 2

	def xBNNN(self): # Jumps to the address NNN plus V0.
		self.pc = (self.opcode & 0x0FFF) + self.V[0]

	def xCXNN(self): # Sets VX to a random number, masked by NN.
		self.V[(self.opcode & 0x0F00) >> 8] = ((randint(1,2767) % 0xFF) & (self.opcode & 0x00FF))
		self.pc += 2

	def xDXYN(self): # Sprites stored in memory at location in index register (I), maximum 8bits wide. Wraps around the screen. If when drawn, clears a pixel, register VF is set to 1 otherwise it is zero. All drawing is XOR drawing (i.e. it toggles the screen pixels)
		
		y=self.V[(self.opcode & 0x00F0) >> 4]
		height = self.opcode & 0x000F
		self.V[0xF] = 0
		pixel = 0
		I = self.I

		for yline in xrange(height):
			
			# Blitz (CHIP8) Hack
			if y < 0 or y >= 32:
				y += 1
				I += 1
				continue

			x=self.V[(self.opcode & 0x0F00) >> 8]
			pixel = self.memory[I]
			I += 1
			for xline in xrange(8):
				if (pixel & 0x80) == 0x80:
					if self.gfxGet(x,y) == 1:
						self.V[0xF] = 1
					self.gfxSet(x,y)
				pixel <<= 1
				x += 1
			y += 1
		self.drawFlag = True
		self.pc += 2

	def xENNN(self): # Calls RCA 1802 program at address NNN.
		try:
			self.opcodes_0xE000[self.opcode & 0x000F]()
		except KeyError:
			print 'Unknown opcode [0xENNN]: ' + hex(self.opcode)

	def xFNNN(self): # Calls RCA 1802 program at address NNN.
		try:
			self.opcodes_0xF000[self.opcode & 0x00FF]()
		except KeyError:
			print 'Unknown opcode [0xFNNN]: ' + hex(self.opcode)
			self.pc += 2

	'''0x0000 Case'''
	def x00E0(self): # Clears the screen.
		self.gfx = [0]*64*32
		self.drawFlag = True
		self.pc += 2

	def x00EE(self): # Returns from a subroutine.
		if self.sp > 0:
			self.sp -= 1
			self.pc = self.stack[self.sp]
		self.pc += 2

	'''0x8000 Case'''
	def x8XY0(self): # Sets VX to the value of VY.
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY1(self): # Sets VX to VX or VY.
		self.V[(self.opcode & 0x0F00) >> 8] |= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY2(self): # Sets VX to VX and VY.
		self.V[(self.opcode & 0x0F00) >> 8] &= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY3(self): # Sets VX to VX xor VY.
		self.V[(self.opcode & 0x0F00) >> 8] ^= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY4(self): # Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
		if self.V[(self.opcode & 0x00F0) >> 4] > (0xFF - self.V[(self.opcode & 0x0F00) >> 8]):
			self.V[0xF] = 1
		else:
			self.V[0xF] = 0
		self.V[(self.opcode & 0x0F00) >> 8] += self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY5(self): # VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
		if self.V[(self.opcode & 0x00F0) >> 4] > self.V[(self.opcode & 0x0F00) >> 8]:
			self.V[0xF] = 0
		else:
			self.V[0xF] = 1
		self.V[(self.opcode & 0x0F00) >> 8] -= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2

	def x8XY6(self): # Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift
		self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] & 0x1
		self.V[(self.opcode & 0x0F00) >> 8] >>= 1
		self.pc += 2

	def x8XY7(self): # Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
		if self.V[(self.opcode & 0x0F00) >> 8] > self.V[(self.opcode & 0x00F0) >> 4]:
			self.V[0xF] = 0
		else:
			self.V[0xF] = 1
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4] - self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2

	def x8XYE(self): # Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift
		push = (self.opcode & 0x0F00) >> 8
		self.V[0xF] = self.V[push] >> 7
		self.V[push] <<= 1
		self.pc += 2

	'''0xE000 Case'''
	def xEX9E(self): # Skips the next instruction if the key stored in VX is pressed.
		if self.key[self.V[(self.opcode & 0x0F00) >> 8]] is not 0:
			self.pc += 4
		else:
			self.pc += 2

	def xEXA1(self): # Skips the next instruction if the key stored in VX isn't pressed.
		if self.key[self.V[(self.opcode & 0x0F00) >> 8]] == 0:
			self.pc += 4
		else:
			self.pc += 2

	'''0xF000 Case'''
	def xFX07(self): # Sets VX to the value of the delay timer.
		self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer
		self.pc += 2

	def xFX0A(self): # A key press is awaited, and then stored in VX.
		keyPress = False

		for i in xrange(16):
			if self.key[i] != 0:
				self.V[(self.opcode & 0x0F00) >> 8] = i
				keyPress = True
		if not keyPress:
			return
		self.pc += 2

	def xFX15(self): # Sets the delay timer to VX.
		self.delay_timer = self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2

	def xFX18(self): # Sets the sound timer to VX.
		self.sound_timer = self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2

	def xFX1E(self): # Adds VX to I & VF set to 1 if range overflows (I+VX > 0xFFF) * undocumented
		if (self.I + self.V[(self.opcode & 0x0F00) >> 8]) > 0xFFF:
			self.V[0xF] = 1
		else:
			self.V[0xF] = 0
		self.I += self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2

	def xFX29(self): # Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented by a 4x5 font.
		self.I = self.V[(self.opcode & 0x0F00) >> 8] * 0x5
		self.pc += 2

					 # Stores the Binary-coded decimal representation of VX, 
					 # with the most significant of three digits at the address in I, 
					 # the middle digit at I plus 1, and the least significant digit at I plus 2. 
					 # (In other words, take the decimal representation of VX, 
					 # place the hundreds digit in memory at location in I, the tens digit at location I+1, 
	def xFX33(self): # and the ones digit at location I+2.)
		push = self.V[(self.opcode & 0x0F00) >> 8]
		self.memory[self.I] = push / 100
		self.memory[self.I + 1] = (push / 10) % 10
		self.memory[self.I + 2] = (push % 100) % 10
		self.pc += 2

	def xFX55(self): # Stores V0 to VX in memory starting at address I.
		for i in xrange(((self.opcode & 0x0F00) >> 8)+1):
			self.memory[self.I + i] = self.V[i]
		self.I += ((self.opcode & 0x0F00) >> 8)
		self.pc += 2

	def xFX65(self): # Fills V0 to VX with values from memory starting at address I.
		for i in xrange(((self.opcode & 0x0F00) >> 8)+1):
			self.V[i] = self.memory[self.I + i]
		self.I += ((self.opcode & 0x0F00) >> 8)
		self.pc += 2
