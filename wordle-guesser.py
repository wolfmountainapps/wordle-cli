# Note that the NYT only uses around 2300 possible 5-letter words as correct answers (whereas there are over 12,000 5-letter words in English). So we use the NYT word list, since we're only looking for correct answers!

#d:\python\wordle>wordle-analyzer.py
#
#Total number of Wordle words used in analysis: 2309
#
#Letter  Total   |       Pos 1   Pos 2   Pos 3   Pos 4   Pos 5
#--------------------------------------------------------------
#  a      975    |        140     304     306     162     63
#  b      280    |        173     16      56      24      11
#  c      475    |        198     40      56      150     31
#  d      393    |        111     20      75      69      118
#  e      1230   |        72      241     177     318     422
#  f      229    |        135     8       25      35      26
#  g      310    |        115     11      67      76      41
#  h      387    |        69      144     9       28      137
#  i      670    |        34      201     266     158     11
#  j      27     |        20      2       3       2       0
#  k      210    |        20      10      12      55      113
#  l      716    |        87      200     112     162     155
#  m      316    |        107     38      61      68      42
#  n      573    |        37      87      137     182     130
#  o      753    |        41      279     243     132     58
#  p      365    |        141     61      57      50      56
#  q      29     |        23      5       1       0       0
#  r      897    |        105     267     163     150     212
#  s      668    |        365     16      80      171     36
#  t      729    |        149     77      111     139     253
#  u      466    |        33      185     165     82      1
#  v      152    |        43      15      49      45      0
#  w      194    |        82      44      26      25      17
#  x      37     |        0       14      12      3       8
#  y      424    |        6       22      29      3       364
#  z      40     |        3       2       11      20      4

import random
import re

NUM_LETTERS = 5
MAX_ATTEMPTS = 6
BEST_GUESS_THRESHOLD = 50 # TBD: refine as needed
MOST_COMMON = ["[abcpst]","[aeiloru]","[aeinoru]","[aceilnrs]","[ehlnrty]"]
INCORRECT_LETTER = 'b' # or there are no more of this letter
CORRECT_LETTER = 'y'
CORRECT_POS = 'g'

def bestguess(greenletters):
    if greenletters is None:
        r = re.compile(MOST_COMMON[0] + MOST_COMMON[1] + MOST_COMMON[2] + MOST_COMMON[3] + MOST_COMMON[4])
    else:
        matchstring = ""
        for x in range(NUM_LETTERS):
            if '.' in greenletters[x]:
                matchstring = matchstring + MOST_COMMON[x]
            else:
                matchstring = matchstring + "[" + greenletters[x] + "]"
        print("\nBest guess filters:")
        print(matchstring)
        r = re.compile(matchstring)
    mostlikelywords = list(filter(r.match, possiblewords))
    print("\nMost likely words:")
    print(mostlikelywords)
    # TBD: handle scenario when there isn't any best guess left
    randomguess = mostlikelywords[random.randint(0, len(mostlikelywords)-1)]
    # Toss a best guess with repeated letters
    repeatedletter = False
    for x in range(NUM_LETTERS-1):
        if repeatedletter:
            break;
        for y in range(x+1, NUM_LETTERS):
            if randomguess[x] in randomguess[y]:
                repeatedletter = True
                print("\nRepeated letter in", randomguess.upper() + ", so toss")
                break;
    if not repeatedletter:
        return randomguess
    else:
        return bestguess(greenletters) # recursive as needed
#end bestguess

fhand = open('wordle-nyt-answers-alphabetical.txt')
originalwords = fhand.read().split()
fhand = open('used-wordlist-raw.txt')
usedwords = fhand.read().split()
possiblewords = list()
for word in originalwords:
    if word.upper() not in usedwords:
        possiblewords.append(word)

guess = input("\nEnter the guess you will enter into Wordle, or hit Enter to randomly select a guess: ")
guess = guess.lower()
if (len(guess) != NUM_LETTERS or not guess.isalpha()) : guess = bestguess(None)
print("\nEnter this word into Wordle:", guess.upper())
if guess in possiblewords:
    # since user can enter the first guess, it might not actually be in the list of possible words
    possiblewords.remove(guess)#

count = 1
while True:
    result = input("\nNow enter the result in this format: one letter per position, with 'b' (wrong), 'y' (correct letter, but wrong position), or 'g' (correct letter and correct position): ").lower()
    if len(result) != NUM_LETTERS:
        continue
    for x in range(NUM_LETTERS):
        if (INCORRECT_LETTER not in result[x]) and (CORRECT_LETTER not in result[x]) and (CORRECT_POS not in result[x]): continue # TBD: could use regular expression instead, and actually need more error checking because something like "tatty" causes an error later below

    if "ggggg" in result:
        print("\nGreat! Today's Wordle was solved in", count, end='')
        if count == 1:
            print(" guess.")
        else:
            print(" guesses.")
        fin = open('used-wordlist-raw.txt', 'r')
        usedwordlist = fin.read()
        fout = open('used-wordlist-raw.txt', 'w')
        fout.write(guess.upper() + " ")
        fout.write(usedwordlist)
        fout.close()
        break
    elif count == MAX_ATTEMPTS:
        print("\nSorry, the maximum number of 6 attempts has been reached! Try again tomorrow. :)")
        break
    count += 1

    greens = ['.', '.', '.', '.', '.']
    yellows = ['.', '.', '.', '.', '.']
    blacks = ['', '', '', '', '']

    greenfound = False
    for x in range(NUM_LETTERS):
        if CORRECT_POS in result[x]:
            greenfound = True
            greens[x] = guess[x]
    if greenfound:
        r = re.compile(''.join(greens))
        possiblewords = list(filter(r.match, possiblewords))
        print("\nGreens:")
        print(greens)
        print(possiblewords)

    for x in range(NUM_LETTERS):
        if CORRECT_LETTER in result[x]:
            yellows[x] = "[^" + guess[x] + "]"
    r = re.compile(''.join(yellows))
    possiblewords = list(filter(r.match, possiblewords))
    print("\nYellows:")
    print(yellows)
    print(possiblewords)

    for x in range(NUM_LETTERS):
        if INCORRECT_LETTER in result[x]:
            for y in range(NUM_LETTERS):
                if (guess[x] not in ''.join(greens)) and (guess[x] not in ''.join(yellows)):
                    # this is needed in case that while letter does exist elsewhere, there isn't another
                    blacks[y] = blacks[y] + guess[x]
    for z in range(NUM_LETTERS):
        if blacks[z] != '':
            blacks[z] = "[^" + blacks[z] + "]"
        else:
            blacks[z] = '.'
    r = re.compile(''.join(blacks))
    possiblewords = list(filter(r.match, possiblewords))
    print("\nBlacks:")
    print(blacks)
    print(possiblewords)

    removewords = list()
    correctletters = ""
    for x in range(NUM_LETTERS):
        if CORRECT_LETTER in result[x]:
            correctletters = correctletters + guess[x]
            for word in possiblewords:
                if guess[x] not in word:
                    if word not in removewords:
                        removewords.append(word)
    for word in removewords:
        possiblewords.remove(word)
    print("\nFinal words", end="")
    if (correctletters != ""):
        print(" with letter(s)", correctletters + ":")
    else:
        print(":")
    print(possiblewords)

    # TBD: handle empty possiblewords, though that shouldn't happen in reality unless there's a bug or the NYT sublist we use doesn't actually reflect their implemented set of words

    if len(possiblewords) > BEST_GUESS_THRESHOLD:
        guess = bestguess(''.join(greens))
        # TBD: handle empty guess
    else:
        guess = possiblewords[random.randint(0, len(possiblewords)-1)]
    print("\nEnter this word into Wordle:", guess.upper()) #
    possiblewords.remove(guess)
