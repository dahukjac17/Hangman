# Hangman game
import requests
import random

#basic instructions for the user to understand how the game works
def instructions():
	print("You will be given a random word to find by guessing the letter or solving.")
	input()
	print("There is three difficulties in this game:")
	print("Easy: 			can guess 4 spaces in a word and allowed 15 mistakes")
	print("Intermediate: 		can guess 3 spaces in a word and allowed 12 mistakes")
	print("hard: 			can guess 2 spaces in a word and allowed 10 mistakes")
	input("Please press enter to start")
	print("\n")

#ask user difficulty level and return answer
def difficulty():
	
	check = False

	while check == False:
		userDiff = input("Enter your difficulty: Easy (e), Intermediate (i), or Hard (h): ")
		check = checkInput(userDiff)

	return userDiff


#check all letters either e, i , or h
def all_equal(userAnswer, letter):
	for x in range(0, len(userAnswer)):
		if userAnswer[x] != letter:
			return False
		
	return True

#checking user input to make sure it is one of the three allowed letters
def checkInput(userInput):
	if userInput == "e" or userInput == "i" or userInput == "h":
		return True
	elif all_equal(userInput, "e") or all_equal(userInput, "i") or all_equal(userInput, "h"):
		return True
	else:
		print("invalid difficulty. Try Again...")
		return False

#if this is test run of the code it will display the answer ahead of time
def testRun(word):
	correctInput = False
	while correctInput == False:
		test = input("is this a test run? Yes(y) or No(n): ")
		if test == "y":
			print("the secret word is: %s" %(word))
			correctInput = True
		elif test == "n":
			correctInput = True
		else:
			print("incorrect input")

#practice word instead of calling URL
def testWord():
	word = "idea"

	return word

#get a word and print it out. Must be at least 4 letters long
def secretWord(words):

	word = random.choice(words)
	word = word.decode()

	while len(word) < 4:
		word = random.choice(words)
		word = word.decode()

	testRun(word)

	return word

#get the dashed version of the word
def dashes(secretWord):
	wordDashed = ""
	for x in range(0,len(secretWord)):
		wordDashed = wordDashed + "-"

	print("the word is: %s" %(wordDashed))
	print("length of word is: " + str(len(wordDashed)))
	return wordDashed


#user will guess a letter or try to solve
def userGuess():
	correctInput = False

	while correctInput == False:
		letter = input("Please enter the letter you want to guess or type solve to answer: ")

		if len(letter) == 1 and letter.isalpha():
			correctInput = True
		elif letter == "solve":
			return letter
		else:
			print("incorrect input")
			
	return letter


#goes through spaces and makes sure none are greater than word length and no duplicates
def validSpaces(arr, wordLength):
	a = -1

	for x in arr:
		if x > wordLength or x == a:
			return False
		a = x

	return True

#turns array into int array
def arrayInt(intArray):
	for x in range(0,len(intArray)):
		 	intArray[x] = int(intArray[x])

	return intArray

#check that spaces guessed are valid
def validPosition(arr,level,word):
	if "e" in level and len(arr) == 4:
		return validSpaces(arr,len(word))
	elif "i" in level and len(arr) == 3:
		return validSpaces(arr,len(word))
	elif "h" in level and len(arr) == 2:
		return validSpaces(arr,len(word))
	else:
		print("mistake in valid position")
		return False


#returns true if all items in array are integers
def isInt(userArray):
	for x in userArray:
		if x.isdigit == False:
			return False
		elif int(x) < 0:
			return False
	return True

#ask user for spaces they want checked in the word for guessed letter
def spotCheck(difficulty, secretWord):

	checkPassed = False


	while checkPassed == False:
		spot = input("Please enter the spaces you want to check (separated by spaces): ")

		spotArray = spot.split( )

		if isInt(spotArray) == True:
			intArr = arrayInt(spotArray)
			if validPosition(intArr,difficulty,secretWord) == True:
				return intArr
		

		print("Incorrect guess. Please try again")
		
#total guesses allowed is recorded
def guessTotal(level):
	if "e" in level:
		return 15
	elif "i" in level:
		return 12
	else:
		return 10

#recursive function to determine if guess by user is correct
def guessResult(word,spaces,guess):
	if spaces == []:
		return False
	elif word[spaces[0]-1] == guess:
		return True
	else:
		spaces.pop(0)
		return guessResult(word,spaces,guess)

#update dashedWord with user's guess
def updateWord(word,dashedWord,spaces,guess):
	listWord = list(word)
	listDash = list(dashedWord)
	for x in range(0,len(spaces)):
		if listWord[spaces[x]-1] == guess:
			listDash[spaces[x]-1] = guess

	return ''.join(listDash)	

#if user wants to guess word they can and it will determine if they correct
def solvepuzzle(secretWord):
	userInput = input("Please enter the word you want to guess: ")
	if secretWord == userInput:
		return True
	else:
		return False

#code for playing a round of the game
def playGame(total_guesses, secretWord, dashedWord, diff):

	while total_guesses > 0:
		guess = userGuess()
		if guess == "solve":
			solved = solvepuzzle(secretWord)
			if solved == True:
				print("you have guessed the word. Congratulations!")
				return None
			else:
				total_guesses = total_guesses - 1
				print("your guess is incorrect")
		else:
					
			spotsArray = spotCheck(diff,secretWord)
			result = guessResult(secretWord,spotsArray,guess)
			if result == True:
				print("Your guess is in the word!")
				dashedWord = updateWord(secretWord,dashedWord,spotsArray,guess)
				if secretWord == dashedWord:
					print("you have guessed the word. Congratulations!")
					return None
				else:
					print("the updated word is: " + dashedWord)	
			else:
				total_guesses = total_guesses - 1
				print("your guess is incorrect")
				print("current word is: " + dashedWord)

		print("guesses remaining: " + str(total_guesses))
		print("\n")

	print("you have failed to guess the word :(")
	print("the word was " + secretWord)

def main():
	print("Welcome to hangman!")
	input()

	word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
	#getting words from URL
	#comment out response variable and words variable if using testWord instead
	response = requests.get(word_url)
	words = response.content.splitlines()
	games = 1
	instructions()
	#looping the game 20 times as long as user wants to keep playing
	while games < 21:
		if games > 1:
			instructionInput = False
			while instructionInput == False:
				seeInstructions = input("would you like to see the instructions again? Yes(y) or No(n) ")
				if seeInstructions == "y":
					instructions()
					instructionInput = True
				elif seeInstructions == "n":
					instructionInput = True
				else:
					print("incorrect input")

		#setting up game functions
		diff = difficulty()
		totalguesses = guessTotal(diff)
		word = secretWord(words)
		#use testWord instead of secretWord if you don't want to use URL
		#word = testWord()
		dashedWord = dashes(word)

		#starting game
		playGame(totalguesses, word, dashedWord, diff)
		response = False
		while response == False:
			anotherGame = input("would you like to play again? Yes(y) or No(n) ")
			if anotherGame == "y":
				games = games + 1
				response = True
			elif anotherGame == "n":
				games = 21
				response = True
			else:
				print("incorrect input")

	


if __name__ == "__main__":
	main()