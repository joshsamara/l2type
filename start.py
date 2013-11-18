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
sessionWords = 0
sessionMissed = 0
totalMissed = 0

def clear():
    os.system('clear')

def getInput():
    userInput = getch()
    if userInput != '\x1b':
        return userInput
    else:
        # clear()
        print ""
        printStats()
        sys.exit()

def getValid(choices):
    userChoice = getInput()
    if userChoice in choices:
        return userChoice
    else:
        return getValid(choices)

def getWord():
    return random.choice(words.all_words_4 + words.all_words_4 + words.all_words_5)

def getAlhpa():
    return "abcdefghijklmnopqrstuvwxyz"

def typeCorrect(word):
    global totalWords 
    global totalLetters
    global sessionLetters
    global sessionMissed
    global totalMissed
    for letterPos in range(len(word)):
        userInput = getInput()
        sys.stdout.write(userInput)
        if userInput == word[letterPos]:
            totalLetters += 1
            sessionLetters += 1
        else:
            sessionMissed += 1
            totalMissed += 1
            print "\n"+word
            return False
    totalWords +=1
    print "\n"        
    return True

def getWPM(count, time):
    return float(count)/(time/60)

def getAccuracy(place, missed):
    total = place + missed
    return (total - float(missed))/max(total,1) * 100

def typeComplete(wordList):
    global sessionMissed
    global sessionWords 
    clear()
    listLen = len(wordList)
    sessionWords = 0 
    if listLen > 0:
        for i in range(listLen):
            acc = getAccuracy(i, sessionMissed)
            print "%s\t\t\t%d/%d %.2f%%" % (wordList[i], i, listLen, acc)
            while not typeCorrect(wordList[i]):
                pass
            sessionWords += 1
    else:
        i = 0
        start = time.time()
        while True:
            now = time.time()
            elapsed = now - start
            acc = getAccuracy(i, sessionMissed)
            word = getWord()
            print "%s\t\t\t%dwords %.2f%% %.2fWPM %ds"% (word, i, acc, getWPM(i, elapsed),elapsed)
            while not typeCorrect(word):
                pass
            i += 1
            sessionWords = i
    return True

def listGen(listLen):
    if listLen == 0:
        return [getAlhpa()]
    elif listLen == 9:
        return []
    else:
        return [getWord() for i in range(listLen)]

def lenChoice():
    valid = {"0":0 , 
        "1":25, 
        "2":50, 
        "3":100,
        "4":250, 
        "5":500,
        "6":1000, 
        "9":9}
    print """Choose a length:
1) 25   words
2) 50   words
3) 100  words
4) 250  words
5) 500  words
6) 1000 words
9) Unlimited words
0) alphabet"""
    userChoice = valid[getValid(valid.keys())]
    return listGen(int(userChoice))

def playAgain():
    print """Would you like to play again?
(Y or N)"""
    userChoice = getInput().lower()
    return userChoice == "y"

def printStats():
    global totalWords 
    global totalLetters
    global totalMissed
    global sessionWords
    global sessionLetters
    global sessionMissed
    global veryStart
    global sessionStart

    now = time.time()
    sessionTime = now - sessionStart
    totalTime = now - veryStart

    print "-" *20
    print "Done!"
    print "-" *20
    print "-----  Session  -----"
    print "Time    :  %.2f seconds" % sessionTime
    print "Words   :  %d" % sessionWords
    print "Accuracy:  %.2f%%" % getAccuracy(sessionWords, sessionMissed) 
    print "WPM     :  %.2f" % getWPM(sessionWords,sessionTime)
    print "Letters :  %d" % sessionLetters
    print "\n------  Total  -------"
    print "Time    :  %.2f seconds" % totalTime
    print "Words   :  %d" % totalWords
    print "Accuracy:  %.2f%%" % getAccuracy(totalWords, totalMissed) 
    print "WPM     :  %.2f%%" % getWPM(totalWords, totalTime)
    print "Letters :  %d" % totalLetters

    sessionLetters = 0
    sessionMissed = 0


def play():
    global veryStart
    global sessionStart
    playing = True
    veryStart = time.time()
    while playing:
        clear()
        sessionStart = time.time()
        typeComplete(lenChoice())
        clear()
        printStats()
        playing = playAgain()

if __name__ == "__main__":
    play()
