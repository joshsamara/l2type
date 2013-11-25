#!/usr/bin/python
import random
import time
import sys
import os
import re
import operator
from mygetch import *

totalWords = 0
totalLetters = 0
sessionLetters = 0
sessionWords = 0
sessionMissed = 0
totalMissed = 0

#average management (faux randoming)
defaultMin = 4
defaultMax = 9
defaultIdeal = 6
averageWrd = 6.0 


def clear():
    os.system('clear')

def leftFormat(wordline, stats):
    return stats + "\n\n" + wordline

def getTextFile():
    clear()
    dirPath = os.path.dirname(os.path.abspath(__file__))
    textPath = dirPath + "/texts"
    print """Use which file as a content source?:
0) A Hitchhikers Guide to the Galaxy
1) The complete works of Shakespeare
2) Monty Python and the Holy Grail
3) More
4) Random"""
    # print dirPath
    menuChoice = getLength(4)
    if menuChoice == 0:
        textName = "hitchhikers_guide.txt"
    elif menuChoice == 1:
        textName = "shakespeare.txt"
    elif menuChoice == 2:
        textName = "monty_python.txt"
    else:
        dirName, subDirs, fileNames = os.walk(textPath).next()
        allTexts = []
        if menuChoice == 4:
            textName = random.choice(fileNames)
        else:
            for textName in fileNames:    
                fileSize = os.stat(textPath + "/" + textName).st_size
                allTexts += [[textName, fileSize]]
            allTexts.sort(key=operator.itemgetter(1), reverse = True)
            print "Choose source to load:".ljust(50)
            for i in range(len(allTexts)):
                nameFrmtd = allTexts[i][0].replace(".txt","").replace("_"," ").title()
                print "%2s)  %30s" % (i, nameFrmtd) + "  %s kb" % allTexts[i][1]
            choice = getLength(len(allTexts))
            textName = allTexts[choice][0]

    filePath = textPath + "/" + textName
    return(textName, filePath)

def loadTextFile():
    global textFile
    global allSents
    global allSentsSmall
    global allWords
    global allWordsGrp
    global defaultMin
    global defaultMax
    textName, filePath = getTextFile()
    textFile = open(filePath, 'r').read()
    open_time = time.time()
    print "Loading words..."
   
    invalids = "[^\(\[\{\}\)\]\.?\n\"]"
    allSents = list(set(re.findall(r'[A-Z][a-z]%s* %s*[a-z]%s*[\.!?]' % (invalids, invalids, invalids), textFile)))
    allSentsSmall = [item.replace("  ", " ") for item in allSents if len(item.replace("  ", " ")) <= 75]
    allWords = [item for item in re.findall(r'\b[a-z]+\b', textFile) if len(item) >= defaultMin]
    allWordsGrp = {}
    for i in range(defaultMin, defaultMax):
        allWordsGrp[i] = list(set([item for item in allWords if len(item) == i])) # remove dupes
    allWordsGrp[defaultMax] = [item for item in allWords if len(item) >= 12]
    #forget about 1,2 or 3 letter words
    processed =  time.time() - open_time
    print "Opened, parsed, %s in %.2f seconds." % (textName, processed)
    print "Press any key to continue..."
    getInput()

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

def getSent():
    global allSents
    global allSentsSmall
    thisSent = random.choice(allSentsSmall)
    return random.choice(allSentsSmall)

def getWord():
    global allWordsGrp
    global averageWrd
    global defaultMin
    global defaultMax
    global defaultIdeal

    minRange = defaultMin
    maxRange = defaultMax
    if averageWrd < defaultIdeal:
        minRange += int(defaultIdeal - averageWrd)
    else:
        maxRange -= int(averageWrd - defaultIdeal)

    rangeChoice = random.randint(minRange, maxRange)
    wordChoice = random.choice(allWordsGrp[rangeChoice])
    averageWrd = (averageWrd + rangeChoice) / 2.0

    return wordChoice

def getAlhpa():
    return "abcdefghijklmnopqrstuvwxyz"

def typeCorrect(word):
    global totalWords 
    global totalLetters
    global sessionLetters
    global sessionMissed
    global sessionWords
    global totalMissed
    global progress
    for letterPos in range(len(progress), len(word)):
        userInput = getInput()
        sys.stdout.write(userInput)
        if userInput == word[letterPos]:
            if userInput == " ":
                progress = word[:(letterPos+1)]
                sessionWords += 1
                totalWords += 1
            totalLetters += 1
            sessionLetters += 1
        elif userInput == "\t":
            print "\n"
            return True
        else:
            sessionMissed += 1
            totalMissed += 1
            time.sleep(.2)
            width = int(os.popen('tput cols', 'r').read())
            sys.stdout.write("\r" + " "* width + "\r" + progress)
            # print "\n"+word
            return False
    sessionWords += 1
    totalWords +=1
    print "\n"        
    return True

def getWPM(count, time):
    return float(count)/(time/60)

def getAccuracy(place, missed):
    total = place + missed
    return (total - float(missed))/max(total,1) * 100

def getFirst(mode, limit = 4):
    generators = {"0": getSent, "1": getWord, "2": getAlhpa} 
    words = [generators[mode]() for i in range(limit)]
    words = words + ["     " for x in range(4-len(words))]
    return words

def getNext(mode):
    generators = {"0": getSent, "1": getWord, "2": getAlhpa} 
    return generators[mode]()

def typeComplete(listLen, mode):
    global sessionMissed
    global defaultMax
    global sessionWords
    global progress
    clear()
    sessionWords = 0 
    if listLen > 0:
        limit = (listLen, 4)[listLen >= 4]
        w1,w2,w3,w4 = [getNext(mode) for i in range(4)]
        while listLen > sessionWords:
            acc = getAccuracy(sessionWords, sessionMissed)
            if mode == "1":
                printWords = ("%s  %s  %s  %s" % (w1, w2, w3, w4))
            else:
                printWords = w1
            printData = "Stats:    %4d/%-4d    %.2f%%" % (sessionWords, listLen, acc)
            printLine = leftFormat(printWords, printData)
            print printLine
            progress = ""
            while not typeCorrect(w1):
                pass
            sys.stdout.write("\x1b[2J\x1b[H")
            w1,w2,w3 = w2,w3,w4
            w4 = getNext(mode)
            # clear()
    else:
        i = 0
        start = time.time()
        w1, w2, w3, w4 = [getNext(mode) for x in range(4)]
        while True:
            now = time.time()
            elapsed = now - start
            acc = getAccuracy(sessionWords, sessionMissed)
            if mode == "1":
                printWords = ("%s  %s  %s  %s" %(w1, w2, w3, w4))
            else:
                printWords = w1
            printData = "Stats:    %4dwords    %.2f%%    %.2fWPM    %4ds"% (sessionWords, acc, getWPM(sessionWords, elapsed),elapsed)
            printLine = leftFormat(printWords, printData)
            print printLine
            progress = ""
            while not typeCorrect(w1):
                pass
            i += 1
            sys.stdout.write("\x1b[2J\x1b[H")
            w1,w2,w3,w4 = [w2,w3,w4,getNext(mode)]
    return True

def getLength(maxVal = None):
    value = raw_input("Choice: ")
    if value.lower() == "exit":
        print ""
        printStats()
        sys.exit()
    else:
        try:
            value = int(value)
            if maxVal is None:
                return max(-1*value, value)
            elif value <= maxVal:
                return max(-1*value, value)
            else:
                raise Exception("Value too large")
        except:
            print "invalid"
            return getLength(maxVal)


def modeChoice():
    print """Choose mode:
0) Sentences
1) Words
2) Alphabet"""
    userChoice = getLength(2)
    print "\nEnter number of instances"
    print "Choose 0 for unlimited:"
    lenChoice = getLength()
    return lenChoice, str(userChoice)

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
    print "WPM     :  %.2f" % getWPM(totalWords, totalTime)
    print "Letters :  %d" % totalLetters

    sessionLetters = 0
    sessionMissed = 0


def play():
    global veryStart
    global sessionStart
    veryStart = time.time() # incase exit before start
    sessionStart = time.time()
    playing = True
    loadTextFile()
    veryStart = time.time()
    while playing:
        clear()
        sessionStart = time.time()
        typeComplete(*modeChoice())
        clear()
        printStats()
        playing = playAgain()

if __name__ == "__main__":
    play()
