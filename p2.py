#!/usr/bin/python3
#Mason Kam
#p2.py
#CPSC 3400
#Purpose: To create a hangman game that "cheats"

def main():
    welcome()
    
    play = input('Do you want to play hangman? (y/n): ')
    while(not (play.lower() == 'y' or play.lower() == 'n')):
            play = input('Please enter y or n: ')
    
    while(play == 'y'):
        wordLength, gameDict = makeList('dictionary.txt')
        gameSemantics(wordLength, gameDict)
    
        play = input('Play again? Enter y or n: ')
        while(not (play.lower() == 'y' or play.lower() == 'n')):
            play = input('Please enter y or n: ')

        if(play == 'n'):
            goodbye()
    
    print('Goodbye!')
    print('')
    print('')
    
    
    
#Welcome Message
def welcome():
    print('Hi! Welcome to Hangman!')
    print('There are a few basic rules to this game')
    print('1) You will be able to enter a word length of your choosing. ')
    print('2) You will be able to enter a number of bad guesses you may have. ')
    print('3) You can choose to see the total list or not (evil version of game). ')



#Create word list
def makeList(fileName):
    num = 0
    numWordsFile = 0
    numWordsGame = 0
    words = []
    gameList = []
    gameDict = {}
    fh = open(fileName)
    maxLength = 2   #Will update with list
    minLength = 4   #Will update with list
    
    for line in fh:
        words.append(line.rstrip())     #Make list of entire dictionary
        
        if len(words[num]) > maxLength: #Get max and min word length
            maxLength = len(words[num])       
        if len(words[num]) < minLength:
            minLength = len(words[num])
        
        num = num + 1
        numWordsFile = numWordsFile + 1
    
    val = int(input('Choose a word length between {} and {} to guess: '.format(minLength, maxLength)))
    while(val < minLength or val > maxLength):
            val = int(input('Enter a number between {} and {}: '.format(minLength, maxLength)))
    
    a = 0
    valid = False
    while(not valid):   #Check to make sure there is a word with that length
        while (a < numWordsFile):
            if len(words[a]) == val:
                gameList.append(words[a])
                numWordsGame = numWordsGame + 1
            a = a + 1
        if(numWordsGame == 0):
            val = int(input('Number not valid. Choose another number from {} and {}: '.format(minLength, maxLength)))
            a = 0
        else:
            valid = True

    gameDict['allWords'] = gameList
    
    return(val, gameDict)



#Game Setup and Play
def gameSemantics(wordLength, gameDict):
    lettersUsed = []
    word = wordLength * '_'
    wordDict = gameDict
    key = 'allWords'
    
    numGuesses = int(input('How many lives would you like?: '))
    while(not(numGuesses > 0)):                                                 #Guesses > 0
        numGuesses = int(input('Please enter a number greater than 0: '))
    
    showWords = input('Do you want a running total of the words left? Enter y or n: ')  #Word list view
    while(not (showWords.lower() == 'y' or showWords.lower() == 'n')):
        showWords = input('Please enter y or n: ')
        
    while(numGuesses != 0):
        print('Guesses Left: {}'.format(numGuesses))
        print("Word to guess: {}".format(word))
        print('')
        print('')
        
        letter = input('Enter a single letter guess: ')
        getValidLetter(letter, lettersUsed)
        lettersUsed.append(letter)
        wordDict = partitionDict(wordDict, letter)
        word, numGuesses, key = updateWord(wordDict, word, numGuesses)
        
        if (showWords == 'y'):
            print('Words left: {} '.format(len(wordDict[key])))
            
        if(numGuesses == 0):    #User lose
            print('I got you! You couldn\'t beat me!')
            print('The word was: {}'.format(list(wordDict[key])[0]))
            print('')
            print('')
            
        if(not ('_' in word)):  #User win
            numGuesses = 0
            print('Nice job. You managed to win...somehow')
            print('')
            print('')
        
        
        
#Update word to show player
def updateWord(wordDict, word, numGuesses):
    key = list(wordDict.keys())[0]

    if(key == 'no_Match'):  #No letter match
        print('Woops, that letter is not here...')
        numGuesses -= 1
        
    else:   #match letter and update viewed string
        count = 0
        for i in key:
            if(not(i == '_')):
                word = word[:count] + i + word[count+1:]
            count += 1
        if('_' in word):
            print('Keep it coming...')
    
    return word, numGuesses, key
        


#Get a valid letter from user
def getValidLetter(letter, used):
    validInput = False
    while(not validInput):
        if(len(letter) != 1):   #Make sure input is 1 letter
            letter = input('Please input a single letter: ')
        elif(letter in used):   #Make sure input is new
            letter = input('Letter already used. Guess again: ')
        elif(letter.isalpha() == False):    #Make sure input is an alphabet character
            letter = input('Please input a single \'letter\': ')
        else:
            validInput = True
            
    return letter
        
      
      
#Break down words to dictionaries
def partitionDict(wordDict, letter):
    wordList = wordDict[list(wordDict.keys())[0]]
    newDict = {}
    
    for a in wordList:  #Go through all words
        dashedString = makeString(a, letter)
        if(letter in a):    
            if(dashedString in newDict):    #Add to existing Key
                newDict[dashedString].append(a)
            else:                           #Make new key in dictionary
                newDict[dashedString] = [a]
        else:
            if('no_Match' in newDict):      #Add to existing key
                newDict['no_Match'].append(a)
            else:                           #Make new key in dictionary
                newDict['no_Match'] = [a]   
                
    newDict = findLongestList(newDict)      #Get largest list to make game longer
    
    return newDict



#Choose longest list of all 
def findLongestList(dashedDict):
    largestSection = ''
    largestList = 0
    indices = dashedDict.keys()
    
    for key in indices:
        if (len(dashedDict[key]) > largestList):
            largestSection = key
            largestList = len(dashedDict[key])
            
        if(len(dashedDict[key]) == largestList and key == 'noMatch'):
            largestSection = key
            
    updatedDict = {largestSection : dashedDict[largestSection]}
    
    return updatedDict



#create the key strings
def makeString(word, guessedLetter):
    b =''
    
    for letter in word:
        if letter == guessedLetter:
            b += letter
        else:
            b += '_'
    return b



def goodbye():
    print('Thank you for playing! Have a great day!')



if __name__ == "__main__": main()


