def generateInput(inputPath, outputPath):	
	with open(inputPath, 'r') as f, open(outputPath, 'w') as f2:
		for line in f:
			print(line)
			if line[:-1].isdigit():
				f2.write(line)


generateInput('input', 'output')