class Disasm:
	def __init__(self):
		self.enabled = False
		self.basePC = 0
		self.currentSel = 0
		self.pageSize = 17
		self.minEntry = 0
		self.maxEntry = 4094

	def getOpText(self, op):
		main = op & 0xF000
		last = op & 0x000F
		NNN = op & 0x0FFF
		NN = op & 0x00FF
		x = (op & 0x0F00) >> 8
		y = (op & 0x00F0) >> 4

		if main == 0x0000:
			if last == 0x0000:
				return 'CLS'
			elif last == 0x000E:
				return 'RET'
		elif main == 0x1000:
			return 'JP 0x' + '{:04x}'.format(NNN).upper()
		elif main == 0x2000:
			return 'CALL 0x' + '{:04x}'.format(NNN).upper()
		elif main == 0x3000:
			return 'SE ' + 'V{:1x}'.format(x).upper() + ', 0x' + '{:02x}'.format(NN).upper()
		elif main == 0x4000:
			return 'SNE ' + 'V{:1x}'.format(x).upper() + ', 0x' + '{:02x}'.format(NN).upper()
		elif main == 0x5000:
			return 'SE ' + 'V{:1x}'.format(x).upper() + ', ' + 'V{:1x}'.format(y).upper()
		elif main == 0x6000:
			return 'LD ' + 'V{:1x}'.format(x).upper() + ', 0x' + '{:02x}'.format(NN).upper()
		elif main == 0x7000:
			return 'ADD ' + 'V{:1x}'.format(x).upper() + ', 0x' + '{:02x}'.format(NN).upper()
		elif main == 0x8000:
			if last == 0x0000:
				return 'LD V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0001:
				return 'OR V'+ '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0002:
				return 'AND V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0003:
				return 'XOR V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0004:
				return 'ADD V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0005:
				return 'SUB V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0006:
				return 'SHR V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x0007:
				return 'SUBN V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
			elif last == 0x000E:
				return 'SHL V' + '{:1x}'.format(x).upper() + ', V' + '{:1x}'.format(y).upper()
		elif main == 0x9000:
			return 'SNE ' + '{:1x}'.format(x).upper() + ', ' + '{:1x}'.format(y).upper()
		elif main == 0xA000:
			return 'LD I, 0x' + '{:04x}'.format(NNN).upper()
		elif main == 0xB000:
			return 'JP V0, 0x' + '{:04x}'.format(NNN).upper()
		elif main == 0xC000:
			return 'RND ' + 'V{:1x}'.format(x).upper() + ', 0x' + '{:02x}'.format(NN).upper()
		elif main == 0xD000:
			return 'DRW ' + 'V{:1x}'.format(x).upper() + ', ' + 'V{:1x}'.format(y).upper() + ', ' + '{:1x}'.format(last).upper()
		elif main == 0xE000:
			if NN == 0x009E:
				return 'SKP V' + '{:1x}'.format(x).upper()
			elif NN == 0x00A1:
				return 'SKPN V' + '{:1x}'.format(x).upper()
		elif main == 0xF000:
			if NN == 0x0007:
				return 'LD V' + '{:1x}'.format(x).upper() + ', DT'
			elif NN == 0x000A:
				return 'LD V' + '{:1x}'.format(x).upper() + ', K'
			elif NN == 0x0015:
				return 'LD DT, V' + '{:1x}'.format(x).upper()
			elif NN == 0x0018:
				return 'LD ST, V' + '{:1x}'.format(x).upper()
			elif NN == 0x001E:
				return 'ADD I, V' + '{:1x}'.format(x).upper()
			elif NN == 0x0029:
				return 'LD F, V' + '{:1x}'.format(x).upper()
			elif NN == 0x0033:
				return 'LD B, V' + '{:1x}'.format(x).upper()
			elif NN == 0x0055:
				return 'LD [I], V' + '{:1x}'.format(x).upper()
			elif NN == 0x0065:
				return 'LD V' + '{:1x}'.format(x).upper() + ', [I]'
			elif NN == 0x0075:
				return 'LD R, V' + '{:1x}'.format(x).upper()
			elif NN == 0x0085:
				return 'LD V' + '{:1x}'.format(x).upper() + ', R'
		else:
			return ''