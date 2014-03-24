"""Generator functions return iterators.
"""

def abc():
    """Functions with a yield statement evaluate up to the yield
    when called and return a generator object. Function state is kept
    between iterations.
    """
    yield "a"
    yield "b"
    yield "c"

# The function itself is not iterable and must be called.
print "Iterating over the generator."
for letter in abc():
    print letter

# To see what's happening.
print "Exploring the generator."
letter = abc()
print "The type of the generator is", type(letter)
print "Calling letter.next:", letter.next()
print "Calling letter.next:", letter.next()
print "Calling letter.next:", letter.next()
try:
    print letter.next()
except StopIteration:
    print "Behaves like an iterator."



def make_unicode():
    """Generate some unicode characters.
    """
    for num in range(300, 320):
        yield unichr(num)

print "Printing some unicode characters."
for letter in make_unicode():
    print letter
