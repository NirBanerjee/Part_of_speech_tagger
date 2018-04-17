from __future__ import division
from FileIO import readFile, writeToFile
import sys
import numpy as np

#Method to predict tag for each line of input
def predictTags(line, probDist, tagHashMap, reverseTagMap):

	parts = line.split(" ")
	i = 0
	line = ""
	for part in parts:
		wordTagPair = part.split("_")
		word = wordTagPair[0]
		vector = probDist[:,i]
		idx = np.argmax(vector)
		tag = reverseTagMap[idx]
		tag = tag.strip()
		word = word + "_" + tag
		line = line + word + " "
		i = i + 1

	return line

#Method to perform backward Algorithm for a line of input
def backwardAlgo(line, wordHashMap, tagHashMap, transitionMatrix, emissionMatrix, tagIndex):

	parts = line.split(" ")
	beta = np.zeros(shape = (len(tagIndex), len(parts)))

	lastPart = parts[len(parts)-1]
	wordTagPair = lastPart.split("_")
	word = wordTagPair[0]
	wordIdx = wordHashMap.get(word)

	for i in range(len(tagIndex)):
		beta[i, len(parts)-1] = 1

	for i in range(len(parts)-2, -1, -1):
		part = parts[i + 1]
		wordTagPair = part.split("_")
		word = wordTagPair[0]
		wordIdx = wordHashMap.get(word)
		for j in range(len(priorVector)):
			crossSum = 0
			for k in range(len(priorVector)):
			 	crossSum = crossSum + (transitionMatrix[j, k] * emissionMatrix[k, wordIdx] * beta[k, i+1])

			beta[j, i] = crossSum

	return beta

#Method to perform forward Algorithm for a line of input
def forwardAlgo(line, wordHashMap, tagHashMap, priorVector, transitionMatrix, emissionMatrix, tagIndex):

	parts = line.split(" ");
	alpha = np.zeros(shape = (len(tagIndex), len(parts)))

	firstPart = parts[0];
	wordTagPair = firstPart.split("_")
	word = wordTagPair[0]
	wordIdx = wordHashMap.get(word)

	for i in range(len(tagIndex)):
		alpha[i, 0] = priorVector[i] * emissionMatrix[i, wordIdx]

	for i in range(1, len(parts)):
		part = parts[i]
		wordTagPair = part.split("_")
		word = wordTagPair[0]
		wordIdx = wordHashMap.get(word)
		for j in range(len(priorVector)):
			crossSum = 0
			for k in range(len(priorVector)):
				crossSum = crossSum + alpha[k, i-1] * transitionMatrix[k,j]

			alpha[j, i] = emissionMatrix[j, wordIdx] * crossSum

	return alpha

#Method to generate map for index against tag
def generateReverseMap(tagIndex):
	hashMap = {}
	for i in range(len(tagIndex)):
		hashMap[i] = tagIndex[i]
		i = i + 1

	return hashMap

#Method to generate map for tag with index
def generateHashMap(indexList):
	hashMap = {}
	i = 0
	for word in indexList:
		word = word.strip()
		hashMap[word] = i
		i = i + 1

	return hashMap

#Method to predict tags by traversing through test file line by line
def performForwardBackward(testData, wordIndex, tagIndex, priorVector, transitionMatrix, emissionMatrix):

	wordHashMap = generateHashMap(wordIndex)
	tagHashMap = generateHashMap(tagIndex)
	reverseTagMap = generateReverseMap(tagIndex)
	labelList = []

	i = 0
	for line in testData:
		line = line.strip()
		alpha = forwardAlgo(line, wordHashMap, tagHashMap, priorVector, transitionMatrix, emissionMatrix, tagIndex)
		beta  = backwardAlgo(line, wordHashMap, tagHashMap, transitionMatrix, emissionMatrix, tagIndex)
		probDist = alpha * beta
		predictLine = predictTags(line, probDist, tagHashMap, reverseTagMap)
		labelList.append(predictLine)
		i = i + 1
		
	return labelList

if __name__ == '__main__':

	#Get all the command line arguments
	testFile = sys.argv[1]
	indexWordFile = sys.argv[2]
	indexTagFile = sys.argv[3]
	hmmPriorFile = sys.argv[4]
	hmmEmissionFile = sys.argv[5]
	hmmTransitionFile = sys.argv[6]
	predictionFile = sys.argv[7]

	#Read the test data
	testData = readFile(testFile)
	wordIndex = readFile(indexWordFile)
	tagIndex = readFile(indexTagFile)

	#Read all the matrices
	priorVector = np.loadtxt(hmmPriorFile)
	transitionMatrix = np.loadtxt(hmmTransitionFile)
	emissionMatrix = np.loadtxt(hmmEmissionFile)

	#Perform forward backward algorithm to generate labels for data
	labelList = performForwardBackward(testData, wordIndex, tagIndex, priorVector, transitionMatrix, emissionMatrix)
	#Write output result to file
	writeToFile(predictionFile, labelList)
