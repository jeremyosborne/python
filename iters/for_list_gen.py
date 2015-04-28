"""Syntactic patterns for creating sequences:

* for loop (easy to read, not always optimal)
* list comprehensions for creating a list
* gererator expressions for building a generator/iterator

Three different functions that produce equivalent results (although results
will likely not be equal not due to random character picking).
"""

from random import choice
import string



def genpass_for(length=8, chars=string.letters+string.digits):
    """Generate password using a for loop.
    """
    # The following:
    pw = []
    for _ in range(length):
        pw.append(choice(chars))
    return ''.join(pw)



def genpass_comprehension(length=8, chars=string.letters+string.digits):
    """Generate password using a list comprehension.
    """
    # Can be rewritten as a list comprehension.
    return ''.join([choice(chars) for i in range(length)])



def genpass_generator(length=8, chars=string.letters+string.digits):
    """Generate password using a generator expression.
    """
    return ''.join(choice(chars) for _ in range(length))



if __name__ == "__main__":
    functs = [genpass_for, genpass_comprehension, genpass_generator]
    for f in functs:
        print "%s produced: %s" % (f.__name__, f())
