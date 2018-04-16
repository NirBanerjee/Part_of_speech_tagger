from __future__ import division
from FileIO import readFile, writeToFile
import sys
import numpy as np

def generateEmissionMatrix(traininInput, wordIndex, indexToWord):
	hm = {}

	for word in wordIndex:
		word = word.strip()
		hm[word] = i
		i = i + 1


	return 0

def generatePriorMatrix(trainingInput, wordIndex):
	hm = {}
	total = 0

	i = 0
	for word in wordIndex:
		word = word.strip()
		hm[word] = i
		i = i + 1

	priorMatrix = np.ones(len(wordIndex))

	for line in trainingInput:
		line = line.strip()
		firstWord = line.split(" ")
		key = firstWord[0][:1]
		keys = firstWord[0].split("_")
		key = keys[1]
		idx = hm[key]
		priorMatrix[idx] = priorMatrix[idx] + 1
		total = total + 1

	return priorMatrix / total


if __name__ == '__main__':

	#Get all the command line arguments
	trainingFile = sys.argv[1]
	indexWordFile = sys.argv[2]
	indexTagFile = sys.argv[3]
	hmmPriorFile = sys.argv[4]
	hmmEmissionFile = sys.argv[5]
	#hmmTransitionFile = sys.argv[6]

	#Read the training file
	trainingInput = readFile(trainingFile)
	#Read the word index file
	wordIndex = readFile(indexWordFile)
	#Read the index to word file
	indexToWord = readFile(indexTagFile)

	#Generate Prior Matric
	priorMatrix = generatePriorMatrix(trainingInput, wordIndex)
	writeToFile(hmmPriorFile, priorMatrix)

	#Generate Emission Matrix
	emissionMatrix = generateEmissionMatrix(trainingInput, wordIndex, indexToWord)
	writeToFile(hmmEmissionFile, emissionMatrix)

	#Generate Transition Matrix


	