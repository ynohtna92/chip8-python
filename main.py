import chip8, sys, os

def main(argv):
	if len(argv) < 2:
		sys.exit('Usage: %s chip8_game' % argv[0])
	if not os.path.exists(argv[1]):
		sys.exit('ERROR: Game %s was not found!' % argv[1])

	game_path = argv[1]

	c8= chip8.Chip8()
	c8.loadApplication(game_path)
	print c8.memory

if __name__ == "__main__":
	sys.exit(main(sys.argv))
