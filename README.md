l2type
======

A simple typing testing game by Josh Samara

Basics
------
This game is to help practice typings
It uses standard python libraries and can be run with
    FILEPATH/python start.py
from any terminal window. (Subsitute FILEPATH for the path to this directory)
It uses .txt files in the 'texts/' directory to generate sentences and words
It keeps track of your typing stats over an entire session
This includes Words, Letters, Accuracy, and Words per Minute Words (WPM)


Controls
--------
The program has 2 types of input: Waiting and Live input
All input waits for an enter key to be pressed during the options.
The program waits for you to hit enter after entering any input before processing it.
This is used for the only game options (see next section)
During this mode you can type "exit" to quit

As soon as the game starts, it will track live input. 
This means as soon as you hit a key it is tracked as the given input.
You can hit the "esc" key to quit at any point during this

Options
-------
You are presented with a few options at the start of the game.
At every section the recommended options are 0

#### Source File ####
0. A Hitchhikers Guide to the galaxy (Recommended)
1. The complete works of Shakespeare
2. Monty Python and the Holy Grail
3. More
4. Random

Before this game starts, it parses a text file to define possible words and sentences.
You choose the text file to parse at this screen.
0-2 are 3 default texts to use as they have the most consistent valid sentences.
0 is recommended because most sentences are modern and familiar.
1 tends to take longer to load (~5s) and has antiquated words and sentences
2 tends to have more emotive words and sentences (eg. AHHHHHH, NI! NI! NI!)

Option 3 lets you select from the entirety of the texts folder.
Here it lists the the choice #, file name, an file size
The text files here have much testing and may provide less 'proper' sentences
You can feel free to add a custom .txt file to the 'texts/' directory and select this option
to use a custom file.

Option 4 picks a file from the 'texts/' directory at random


#### Difficulty ####
0. Easy (Recommended)
1. Hard

The differences in difficult directly affect the gameplay 
During this game, you type words as seen on the screen.
On Easy, if you make a mistake during a word, your mistake will be automatically erased
and you will continue from the last correct letter typed
On Hard, if you make a mistake during a word, your mistake will be automatically erased
and you will continue from the very start of the previously typed word
(Hard can get frustrating)

#### Mode ####
0. Sentences (Recommended)
1. Words
2. Alphabet

Option 0 will give you randomly generated sentences to type.
Option 1 will give you randomly generated words to type
Option 2 will give you the entire alphabet (a-z) to type (as singele words)
One big difference between option 0 and 1/2 is that in option 0 you must type spaces (" ")
between words whereas the other options you do NOT need to type spaces.

#### Instances ####
Any number (0 for unlimited)

Enter 0 here to do an unlimited amount of your previously selected value.
Enter a valid integer and you will have to type the given number of values
If you anter a non 0 value, you get sent back to the _Mode_ option after completion


Other Important Information
---------------------------
### PRESS TAB ### to skip any words or sentences
If you find any issues with this game, please report them to me at joshsamara@gmail.com


