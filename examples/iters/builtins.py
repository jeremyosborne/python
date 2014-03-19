""" Python provides quite a few utilities, as builtins and as part of the
    standard library, to work with sequences.
"""

import string

# Make a list of all of the ascii_letters and numbers.
l = list(string.ascii_letters) + [i for i in range(10)]



# Test if all values are truthy.
print all(l)



# Are any values truthy?.
print any(l)



# Can we call the identifier (as a function)?
print callable(l)



# Construct a new list with reference to each element that passes our
# test. 
# Functions can be passed into other functions in Python without fanfare.
def oddnumbers(x):
    return type(x) == int and x % 2 == 1

l2 = filter(oddnumbers, l)
print l2

# People seem to hate on lambdas. I don't have a problem with them.
# The following is equivalent to the above, as a single line expression
# using a Python lambda (i.e. anonymous function).
l2 = filter(lambda x: type(x) == int and x % 2 == 1, l)
print l2



# Maximum value of a sequence.
# On a heterogeneous list, this can be arbitrary and shouldn't be trusted.
print max(l)
# Maximum of only the numbers in our list.
print max(filter(lambda x: type(x) == int, l))



# Minimum value of a sequence.
print min(l)



# Apply function to each element in sequence, return new list with results.
def identifier(x):
    if type(x) == str:
        # Be careful of the above going forward. Python 3 works in unicode.
        return "letter"
    elif type(x) == int:
        return "number"
    else:
        return "wtf?"

print map(identifier, l)



# Return sum of a sequence (mainly for numbers).
# Using a generator to just get the numbers out.
print sum(x if type(x) == int else 0 for x in l)



# Like sum, more useful on complex sequences.
def reducer(subtotal, nextitem):
    if type(subtotal) == str:
        subtotal = 0
    if type(nextitem) == str:
        nextitem = 0
    return subtotal + nextitem

print reduce(reducer, l)



# Sort a sequence, returning a new sequence. 
# (Arbitrary for heterogeneous list.)
print sorted(l)
# Descending order.
print sorted(l, reverse=True)
# Treat upper and lowercase letters as equals.
def sorter(x):
    if type(x) == str:
        return ord(x.lower())
    return x
print sorted(l, key=sorter, reverse=True)



# There are multiple ways of sorting a dict by value. This is one.
d = { "dog": 40, "pig": 54, "horse": 5 }
sorted(d.items(), key=lambda x: x[1], reverse=True)



# Group two+ sequences together into a list of tuples.
print zip(d.keys(), d.values())
# This of course is much what .items() does.
print d.items()
