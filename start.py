#!/usr/bin/python
import words
import random
import time
import sys
import os
from mygetch import *

totalWords = 0
totalLetters = 0
sessionLetters = 0

def clear():
    os.system('clear')

def getInput():
    userInput = getch()
    if userInput != '\x1b':
        return userInput
    else:
        # clear()
        print ""
        sys.exit()

def getWord():
    return random.choice(words.all_words_4 + words.all_words_4 + words.all_words_5)

def getAlhpa():
    return "abcdefghijklmnopqrstuvwxyz"

def typeCorrect(word):
    global totalWords 
    global totalLetters
    global sessionLetters
    for letterPos in range(len(word)):
        userInput = getInput()
        sys.stdout.write(userInput)
        if userInput == word[letterPos]:
            totalLetters += 1
            sessionLetters += 1
        else:
            print "\n"+word
            return False
    totalWords +=1
    print "\n"        
    return True

def typeComplete(wordList):
    clear()
    listLen = len(wordList)
    if listLen > 0:
        for i in range(listLen):
            print "%s\t\t\t\t%d/%d" % (wordList[i], i, listLen)
            while not typeCorrect(wordList[i]):
                pass
    else:
        i = 0
        while True:
            word = getWord()
            print "%s\t\t\t\t%d words"% (word, i)
            while not typeCorrect(word):
                pass
            i += 1
    return True

def listGen(listLen):
    if listLen == 0:
        return [getAlhpa()]
    elif listLen == 5:
        return []
    else:
        return [getWord() for i in range(listLen * 25)]

def lenChoice():
    print """Choose a length:
1) 25  words
2) 50  words
3) 75  words
4) 100 words
5) Unlimited words
0) alphabet"""
    userChoice = getInput()
    userChoice = (0, int(userChoice))[userChoice in ["0","1","2","3","4", "5"]]
    return listGen(userChoice)

def playAgain():
    print """Would you like to play again?
(Y or N)"""
    userChoice = getInput().lower()
    return userChoice == "y"

def play():
    global totalWords 
    global totalLetters
    global sessionLetters
    playing = True
    veryStart = time.time()
    while playing:
        clear()
        start = time.time()
        typeComplete(lenChoice())
        now = time.time()
        print "-" *20
        print "Done"
        print "-" *20
        print "Session"
        print "Time   :  %.2f seconds" % (now - start)
        print "Letters:  %d" % sessionLetters
        print "\nTotal"
        print "Time   :  %.2f seconds" % (now - veryStart)
        print "Words  :  %d" % totalWords
        print "Letters:  %d" % totalLetters
        sessionLetters = 0
        playing = playAgain()

if __name__ == "__main__":
    play()
