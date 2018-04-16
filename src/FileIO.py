import csv

def readFile(fileName):
	dataFrame = []
	with open(fileName, 'r') as csvFile:
		for row in csvFile:
			dataFrame.append(row)

	return dataFrame

def writeToFile(fileName, dataFrame):
	writer = open(fileName, 'w')
	for line in dataFrame:
		writer.write(str(line))
		writer.write('\n')
	writer.close
