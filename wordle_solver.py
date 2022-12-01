import string
import math
import itertools
import random
from matplotlib import pyplot as plt
from pattern_distribution_dictionary import patDistDict


#reads in the wordlewords file
with open("wordlewords.txt") as f:
	wordlewords=[word for line in f for word in line.split()]

#reads in the allowable words file
with open("allowable.txt") as f:
	allowablewords=[word for line in f for word in line.split()]


#This is a list of all the possible patterns
possiblePatterns = list(itertools.product([0, 1, 2], repeat=5))


#This functions return all the remaining answers after a guess
def possibleAnswers(List,guess,pattern):

	possibleAnswers = []

	greyList = []
	yellowDict = {}
	greenDict = {}

	for i in range(5):
		if(pattern[i]== 0):
			greyList.append(guess[i])
		elif(pattern[i] == 1):
			yellowDict[i] = guess[i]
		else:
			greenDict[i] = guess[i] 

	
	for x in List:

		originalword = x 

		
		#checks if the yellow letters aren't in their guessed position.
		if(not all([x[e] != yellowDict[e] for e in yellowDict ])):
			continue

		#checks if the green letters are in the correct position.
		if(not all([x[e] == greenDict[e] for e in greenDict ])):
			continue


		#removes the green letters from the word at their current index
		noGreen = []

		for q in range(len(x)):
			if(q not in greenDict.keys()):
				noGreen.append(x[q])


		#remove yellow letters and compare with previous length
		x = noGreen.copy()

		for o in yellowDict.values():
			try : 
				x.remove(o)

			except ValueError:
				pass

		if(not len(x)==len(noGreen)-len(yellowDict)):
			continue

		
		#check if the remaining letters are in the grey list
		if(any([e in greyList for e in x])):
			continue


		#append the orignalword
		possibleAnswers.append(originalword)

	return possibleAnswers

#This function find the expected value of the guesses remaining possible answers
def expectedWordCount(dist,currentWordCount):
	dist = [x**2/currentWordCount for x in dist]
	return sum(dist)

#This function will return the pattern from the guess
def wordleGame(guess,answerWord):

	#this function return the index of letter that is not marked as green
	def indexYellow(guess,pattern,letter):
		for x in range(len(guess)):
			if(guess[x]==letter and pattern[x]==0):
				return x


	pattern = [0,0,0,0,0]


	noGreenGuess = []
	noGreenAnswerWord = []


	#adding greens to pattern
	for i in range(len(guess)):
		if guess[i] == answerWord[i]:
			pattern[i] = 2

	#print("the length of the guess is : ",len(guess))
	#creating guess without the greens and answer word without the greens
	for p in range(len(pattern)):
		if pattern[p] == 0:
			noGreenGuess.append(guess[p])
			noGreenAnswerWord.append(answerWord[p])

	#checking if the any letter in the guess with no greens are in the answer word with no greens
	#then adding those yellows to the pattern
	for e in noGreenGuess:
		if e in noGreenAnswerWord:
			pattern[indexYellow(guess,pattern,e)] = 1
			noGreenAnswerWord.remove(e)

	return pattern 


#This function returns the probabilty that a word is the answer
def probReturn(allowableWord,ewc,wordlewords):
	
	if(allowableWord in wordlewords):
		return  1/len(wordlewords) + 1/ewc
	else:
		return  1/ewc

#This function returns all the possible guesses after a guess
def possibleGuesses(List,guess,pattern):

	possibleGuesses= []

	greyList = []
	yellowDict = {}
	greenDict = {}

	for i in range(5):
		if(pattern[i]== 0):
			greyList.append(guess[i])
		elif(pattern[i] == 1):
			yellowDict[i] = guess[i]
		else:
			greenDict[i] = guess[i] 

	
	for x in List:

		originalword = x 

		
		#checks if the yellow letters aren't in their guessed position.
		if(not all([x[e] != yellowDict[e] for e in yellowDict ])):
			continue


		##check if all the yellow letters are in the word
		if(not all([yellowDict[d] in x for d in yellowDict])):
			continue
		
		#check if the grey letters aren't in the word
		if(not all([f not in x for f in greyList])):
			continue

		#append the orignalword
		possibleGuesses.append(originalword)

	return possibleGuesses

#In the case where 4 greens are known this function will return a word
#that eliminates the most words from the wordleWords list
def elimination(wordlewords,allowablewords):
	position = -1
	for p in range(len(wordlewords[0])):
		if(wordlewords[0][p] != wordlewords[1][p]):
			position = p

	differentLetters = []

	for m in wordlewords:
		differentLetters.append(m[position])


	ogDifferentLetters = differentLetters.copy()
	bestGuess = ""
	highestCount = 0

	for c in allowablewords:

		count = 0 
		differentLetters = ogDifferentLetters.copy()

		for letters in c:

			#print(letters, " : ", differentLetters ," : ", letters in differentLetters)
			
			if(letters in differentLetters):
				count += 1
				differentLetters.remove(letters)




		if count>highestCount:
			highestCount = count 
			bestGuess = c


		if(highestCount == 5):
			break

	return bestGuess

#This function return the next guess
def guess(allowableWords,wordlewords,possiblePatterns,ogAllowablewords,numGreens):

	if(len(wordlewords) == 2):
		return wordlewords[0]


	if(numGreens == 4):
		return elimination(wordlewords,ogAllowablewords)

	else:

		bestguess = ['',0]

		for words in allowableWords:

			dist = []
			for patterns in possiblePatterns:
				dist.append(len(possibleAnswers(wordlewords,words,patterns)))


			ewc = expectedWordCount(dist,len(wordlewords))

			if(ewc == 0):
				continue

			pr = probReturn(words,ewc,wordlewords)

			#print("current word is :", words, "probReturn is : ", pr)

			if(pr>bestguess[1]):

				bestguess[0] = words
				bestguess[1] = pr

			#print("This is the current best guess : ", bestguess)

		return bestguess[0]



#answerWord = "start"

#bestWords = {}

#for words in patDistDict:
#	bestWords[words] = expectedWordCount(patDistDict[words],len(wordlewords))



#bestWordList = list(sorted(bestWords.items(), key=lambda x:x[1]))
#bestWord = bestWordList[0][0]



#print("The answer word is : " , answerWord)


bestWord = "roate"

ogWordlewords = wordlewords
ogAllowablewords = allowablewords
ogBestWord = bestWord
OgPossiblePatterns = possiblePatterns


returnList = []

for answer in wordlewords:
#for answer in random.sample(wordlewords, 100):
#for answer in ["vaunt"]:
	count = 1 

	numGreens = 0

	greensPattern = [0,0,0,0,0]

	guesses = []

	while(True):
		#print("The answerWord is : ", answer)
		#print("The guess is : ",bestWord)

		
		guesses.append(bestWord)
		pattern = wordleGame(bestWord,answer)



		if(pattern == [2,2,2,2,2]):
			break

		for j in range(len(pattern)):
			if(pattern[j] == 2):
				greensPattern[j] = 2


		wordlewords = possibleAnswers(wordlewords,bestWord,pattern)


		if(len(wordlewords) == 1):
			count+=1
			break


		allowablewords = possibleGuesses(allowablewords,bestWord,pattern)

		#possiblePatterns = rpPatterns(possiblePatterns,pattern)
		#print("This is the guess it makes :",bestWord)

		#print("These are the wordleWords : ", wordlewords)

		#print("These are the allowablewords : ", allowablewords)

		#print("These are the possiblePatterns :" , possiblePatterns)

		numGreens = greensPattern.count(2)

		bestWord = guess(allowablewords,wordlewords,possiblePatterns,ogAllowablewords,numGreens)

		count += 1

	returnList.append(count)

	print("The answerWord is : ", answer, "The amount of guesses is : " ,count, " : ", guesses)

	wordlewords = ogWordlewords
	allowablewords = ogAllowablewords
	bestWord = ogBestWord
	possiblePatterns = OgPossiblePatterns
	guesses = []

	

	
print(returnList)
print("This is the average amount of guesses : ",sum(returnList)/len(returnList), " Congratulations!!")
 


