# An iterator is an interface like construct that Python supports.
# Many things are iterable, as we saw above.
# There are some other useful tools in the itertools module.
# In general, don't import * on a library.
from itertools import *
# assuming we still have string from earlier.

# Make an iterator that cycles through a ROT13 alphabet.
def rot13():
    midval = ord('a')+13
    # Python can have functions inside of functions.
    def rotator(letter):
        oval = ord(letter)
        if oval >= midval:
            return chr(oval-13)
        else:
            return chr(oval+13)
    # a lot like map, except returns an iterator.
    return imap(rotator, string.ascii_lowercase)

# We get an iterator back, not a list.
print rot13()
# Simple use.
print "The ROT13 alphabet."
for i, letter in enumerate(rot13()):
    print i+1, letter



# Get the combinations of a poker hand
card_values = list(string.digits[2:])+["10"]+list("JQKA")
card_suits = ["c", "d", "h", "s"]
# Generate a cartesian product of values+suits, then create sequence.
cards = [card+suit for card, suit in product(card_values, card_suits)]
print cards
# Generate all the 5 hand combinations we can.
# There are alot, you will probably want to ctrl-c this....
for fivecards in combinations(cards, 5):
    print fivecards
