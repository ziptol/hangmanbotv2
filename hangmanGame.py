import random

class HG():
    def __init__(self, wordList, allowedGuesses):

        # choose a word
        wordlistIndex = random.randint(0,len(wordList))
        self.word = wordList[wordlistIndex]
        self.homeMessage = ""
        self.allowedGuesses = allowedGuesses
        self.numWrongGuesses = 0
        self.gameWon = False
        self.gameLost = False

        # establish variables
        self.guessed = []

    def guess(self, guessLetter):
        if not (len(guessLetter)==1):
            return self.display("Invalid Guess")

        # if letter has already been guessed
        if(guessLetter in self.guessed):
            return self.display("Guess has already been made")
        
        # add letter to guessed list
        self.guessed.append(guessLetter)

        if(guessLetter in self.word):
            # if player has won
            if(set(self.word).issubset(self.guessed)):
                self.gameWon = True
        else:
            # increment number of wrong guesses
            self.numWrongGuesses += 1
            # check for loss 
            if(self.numWrongGuesses>=self.allowedGuesses):
                self.gameLost = True
        
        return self.display()

    # Display hangman game string for user
    def display(self, userMessage=""):
        # info display
        winState = "Won="+str(self.gameWon)+" Loss="+str(self.gameLost)
        guessState = str(self.numWrongGuesses)+"/"+str(self.allowedGuesses)
        
        # word display
        dispWord = ""
        for letter in self.word:
            if(letter in self.guessed):
                dispWord = dispWord+f'{letter}  '
            else:
                dispWord = dispWord+"\_  "

        # full message
        return (winState+"\n"+guessState+"\n"+dispWord+"\n"+userMessage)

    def getWord(self):
        return self.word
    
    def getGameWon(self):
        return self.gameWon

    def getGameLost(self):
        return self.gameLost
    
        
