import random

HANGMANPICS = ['''
  +----+
  |    |
       |
       |
       |
       |
=========''', '''
  +----+
  |    |
  O    |
       |
       |
       |
=========''', '''
  +----+
  |    |
  O    |
  |    |
       |
       |
=========''', '''
  +----+
  |    |
  O    |
 /|    |
       |
       |
=========''', '''
  +----+
  |    |
  O    |
 /|\   |
       |
       |
=========''', '''
  +----+
  |    |
  O    |
 /|\   | 
 /     |
       |
=========''', '''
  +----+
  |    |
  O    |
 /|\   |
 / \   |
       |
=========''']

class HG():
    def __init__(self, wordList, allowedGuesses):

        # choose a word
        wordlistIndex = random.randint(0,len(wordList))
        self.word = wordList[wordlistIndex][:-1]

        # setup variables
        self.homeMessage = ""
        self.allowedGuesses = allowedGuesses
        self.numWrongGuesses = 0
        # Active = 0, Won = 1, Lost = 2
        self.gameState = 0 
        self.guessed = []
        

    def guess(self, guessLetter):
        # if guess is greater than 1 letter, count as multiguess
        if len(guessLetter)>1:
            # player guesses word, full win
            if(guessLetter==self.word):
                self.gameState = 1
                for x in guessLetter: 
                    self.guessed.append(x)
                    
            
            else:
                self.numWrongGuesses+=1
                return self.display("Multiletter guess, WRONG!")

        else:
            # if letter has already been guessed
            if(guessLetter in self.guessed):
                return self.display("Guess has already been made")
            
            # add letter to guessed list
            self.guessed.append(guessLetter)

            if(guessLetter in self.word):
                # if player has won
                if(set(self.word).issubset(self.guessed)):
                    self.gameState = 1
            else:
                # increment number of wrong guesses
                self.numWrongGuesses += 1
                # check for loss 
                if(self.numWrongGuesses>=self.allowedGuesses):
                    self.gameState = 2
        
        if(self.gameState == 1):
            return self.display("GAME OVER YOU WIN")
        
        if(self.gameState == 2):
            return self.display("GAME OVER YOU LOSE\nThe word was: "+self.getWord())
        
        return self.display()

    # Display hangman game string for user
    def display(self, userMessage=""):
        # Info display for debug, will be replaced
        winState = "Game state = "+str(self.gameState)
        guessState = str(self.numWrongGuesses)+"/"+str(self.allowedGuesses)
        
        # Concatinate word display
        dispWord = ""
        for letter in self.word:
            if(letter in self.guessed):
                dispWord = dispWord+f'{letter}  '
            else:
                dispWord = dispWord+"\_  "

        # full message
        displayMessage = (HANGMANPICS[self.numWrongGuesses]+"\n"+dispWord+"\n"+userMessage)
        return ([self.gameState, displayMessage])
 

    def getWord(self):
        return self.word
    
    def setHomeMessage(self, messageID):
        self.homeMessage = messageID
    
    def getHomeMessage(self):
        return self.homeMessage
    
    
        
