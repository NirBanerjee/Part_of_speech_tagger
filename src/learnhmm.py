from __future__ import division
from FileIO import readFile
import sys
import numpy as np

#Method to generate Emission priorMatrix
def generateEmissionMatrix(trainingInput, tagIndex, wordIndex):
	wordhm = {}
	taghm = {}

	i = 0
	for word in tagIndex:
		word = word.strip()
		taghm[word] = i 
		i = i + 1

	i = 0
	for word in wordIndex:
		word = word.strip()
		wordhm[word] = i
		i = i + 1

	emissionMatrix = np.ones(shape = (len(tagIndex), len(wordIndex)))

	for line in trainingInput:
		line = line.strip()
		lineParts = line.split(" ")
		for part in lineParts:
			exp = part.split("_")
			word = exp[0]
			tag = exp[1]
			wIndex = wordhm[word]
			tIndex = taghm[tag]
			emissionMatrix[tIndex][wIndex] = emissionMatrix[tIndex][wIndex] + 1

	sumArray = np.sum(emissionMatrix, axis = 1)
	for i in range(len(emissionMatrix)):
		for j in range(len(emissionMatrix[0])):
			emissionMatrix[i][j] = emissionMatrix[i][j] / (sumArray[i])

	return emissionMatrix

#Method to generate TransitionMatrix
def generateTransitionMatrix(trainingInput, tagIndex):
	hm = {}
	i = 0
	for word in tagIndex:
		word = word.strip()
		hm[word] = i
		i = i + 1

	transitionMatrix = np.ones(shape = (len(tagIndex), len(tagIndex)))

	for line in trainingInput:
		line = line.strip()
		lineParts = line.split(" ")
		prevW = lineParts[0]
		for k in range(1, len(lineParts)):
			currW = lineParts[k]
			keys = currW.split("_")
			currIdx = hm[keys[1]]
			keys = prevW.split("_")
			prevIdx = hm[keys[1]]
			transitionMatrix[prevIdx][currIdx] = transitionMatrix[prevIdx][currIdx] + 1
			prevW = currW

	sumArray = np.sum(transitionMatrix, axis = 1)
	
	for i in range(len(transitionMatrix)):
		for j in range(len(transitionMatrix[0])):
			transitionMatrix[i][j] = transitionMatrix[i][j] / (sumArray[i])

	return transitionMatrix

#Method to generate Priors for HMM
def generatePriorMatrix(trainingInput, tagIndex):
	hm = {}

	i = 0
	for word in tagIndex:
		word = word.strip()
		hm[word] = i
		i = i + 1

	priorMatrix = np.ones(len(tagIndex))

	for line in trainingInput:
		line = line.strip()
		firstWord = line.split(" ")
		key = firstWord[0][:1]
		keys = firstWord[0].split("_")
		key = keys[1]
		idx = hm[key]
		priorMatrix[idx] = priorMatrix[idx] + 1

	return priorMatrix / np.sum(priorMatrix)


if __name__ == '__main__':

	#Get all the command line arguments
	trainingFile = sys.argv[1]
	indexWordFile = sys.argv[2]
	indexTagFile = sys.argv[3]
	hmmPriorFile = sys.argv[4]
	hmmEmissionFile = sys.argv[5]
	hmmTransitionFile = sys.argv[6]

	#Read the training file
	trainingInput = readFile(trainingFile)
	#Read the word index file
	wordIndex = readFile(indexWordFile)
	#Read the index to word file
	tagIndex = readFile(indexTagFile)

	#Generate Prior Matrix
	priorMatrix = generatePriorMatrix(trainingInput, tagIndex)
	np.savetxt(hmmPriorFile, priorMatrix)

	#Generate Transition Matrix
	transitionMatrix = generateTransitionMatrix(trainingInput, tagIndex)
	np.savetxt(hmmTransitionFile, transitionMatrix)

	#Generate Emission Matrix
	emissionMatrix = generateEmissionMatrix(trainingInput, tagIndex, wordIndex)
	np.savetxt(hmmEmissionFile, emissionMatrix)


	