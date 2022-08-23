NUM_LETTERS = 5;

#fhand = open('used-wordlist-raw.txt')
fhand = open('wordle-nyt-answers-alphabetical.txt')
words = fhand.read().split()
lettercount = dict()
poscount = []
for x in range(NUM_LETTERS):
    poscount.append(dict())

# Go through all the words one by one and char by char
for word in words:
    pos = 0
    for c in word:
        lettercount[c] = lettercount.get(c,0) + 1
        poscount[pos][c] = poscount[pos].get(c,0) + 1
        pos += 1

# Sort the letters and output results
alphalist = list(lettercount.keys())
alphalist.sort()
print("\nTotal number of Wordle words used in analysis:", len(words))
print("\nLetter\tTotal\t|\tPos 1\tPos 2\tPos 3\tPos 4\tPos 5")
print("--------------------------------------------------------------", end='')
for key in alphalist:
    print("\n ", key, "\t", lettercount[key], "\t|\t", end='')
    for x in range(NUM_LETTERS):
        print(" ", poscount[x].get(key,0), "\t", end='')
print("\n")

# TBD: sort descending by total count
