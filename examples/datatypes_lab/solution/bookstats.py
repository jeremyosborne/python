"""
Lab:
----

Use data/TaleOfTwoCities.txt.



Start:

* Count the number words in the book by calling split.
* Figure out the top ten most used words using a dictionary and sorted.



Experiment 1:

* Use a regular expression instead of calling split. Simple or complex is fine.



Experiment 2:

* use filter to get rid of words that contain numbers.
* use map to make all the words the same case.



Experiment 3:

* Use the collections.Counter to replace the work done with the dictionary and sorted.
"""

import re
from collections import Counter



print "Words in Tale of Two Cities."

with open("../data/TaleOfTwoCities.txt", "r") as f:
    book = f.read()



words = book.split()
# Experiment 1.
# words = re.findall(r"\w+", book)

# Experiment 2.
# words = filter(lambda s: s.isalpha(), words)
# words = map(lambda s: s.lower(), words)

print "Total number of words counted:", len(words)



wordcounts = {}
for word in words:
    if word in wordcounts:
        wordcounts[word] += 1
    else:
        wordcounts[word] = 1
 
most_common = sorted(wordcounts.items(), key=lambda word: word[1], reverse=True)
most_common = most_common[:10]

# Experiment 3
#wordcounts = Counter(words)
#most_common = wordcounts.most_common(10)

print "Top 10 most used words:"
for word, count in most_common:
    print word, count

