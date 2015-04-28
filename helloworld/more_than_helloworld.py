#!/usr/bin/env python

"""This example is designed to go through as much of the basics
of Python as possible to get people up to speed quickly.

This is a multi-line string.

This string, because it is the first string of your module, is also a
docstring. If you `help(thismod)` after importing this, you'll see 
this string.

If your python script is meant to be executed from a UNIX commandline,
you will probably want to put the shebang in your file (the first line
of this file) to make it simpler to `./thisfile.py`
"""

# This is a python comment. There are no multiline comments, only
# single line comments.

# This is an import statement that brings in a module found in the 
# PYTHONPATH, this one being the sys module.
import sys
# This import statement brings in one function from the random module --
# randint. 
from random import randint


# This is a function definition. It takes no arguments.
def test_types():
    # The colon at the end of our function signature is the designation
    # of a block, like { braces } in many other languages.

    # Python relies on indentation to designate nested block level. Each
    # statement must be the same number of whitespace characters.
    # 4 space characters (non-tab) is traditional for each indentation level.

    # The print statement is one of the major differences between Python 2
    # and Python 3. In Python 3, the print statement becomes a function.
    # Don't put parentheses around your Python 2 print arguments, you'll
    # get unexpected results.
    print "Hello World!"
    # Print statements are appended with a newline by default.
    print "Testing types:"
    
    # Python has strongly typed data (although there is data coercion to a 
    # small extent in certain situations).
    # The None type in Python is Python's null. The first letter must be upper
    # cased. Testing (None == None) == True, where True is one of the Boolean
    # types in python.
    print "Is None == None?"
    # Python has the usual logical operators as most other languages.
    # Here we check for equality, which will return a boolean: True or
    # False
    print None == None
    
    print "Some fun equality checks:"
    # You'll likely see a few different ways to format strings. This
    # is an old standard printf style formatting.
    # The modulo operation mod(ifies) the string. (Python does allow custom
    # operation overrides.)
    # Unlike some print implementations, the flags are more customary in 
    # general and most any object should be coercible into a string (for
    # example).
    print "Is None == 0? %s" % None == 0
    # Print statements can also be passed comma delimited values.
    print "False == 0 is", False == 0
    print "True == 1 is", True == 1
    print "True == 2 is", True == 2
    
    # Python has a lot of builtins. A builtin is essentially a global
    # function, object, type, value, etc... that is not a keyword and
    # does not need to be imported.
    print "The type of None is", type(None)
    # int is itself a type.
    print "Is the type(1) == int?", type(1) == int
    # Each type can (attempt to) construct/convert other types.
    print "Is the int('1') == 1?", 1 == int('1')
    # Floats and ints are different types in Python.
    print "Is 1. == 1?", type(1.) == type(1)

# How do we know the function above is done?
# Deindent. Additional lines of whitespace can help as visual cues.

# This is a function definition. Function parameters are untyped.
# This function takes takes one formal argument and one optional argument.
# The optional second argument has a default value.
def roll(faces, times=1):
    
    # Standard Python if statement, forming another block.
    # Python uses the words `and` and `or` as logical conjunctions.
    if type(faces) != int or type(times) != int:
        # Exceptional situation, stop program flow and return control.
        # Many errors are already defined for us as builtins.
        # Python is object oriented and has classes/types, but no new
        # statement. Below we are creating a new error.
        raise TypeError("faces and times must be of type int")
    elif faces < 1 or times < 1:
        raise ValueError("faces and times must each be > 1")

    # Python offers a list as one of its basic data types.
    # Lists can contain mixed types, and are dynamic (the range can be
    # increased or decreased). Lists use a 0-based index.
    rolls = []
    # For loops are simple yet versatile. The builtin range is designed
    # for traditional list iteration.
    for i in range(times):
        rolls.append(randint(1, faces))
    
    # Python has a lot of idioms. The above could have been
    # done with what is known as a list comprehension. See below for
    # reference.
    #rolls = [randint(1, faces) for i in range(times)]

    # When we have a list that has numeric values, sum can iterate the
    # list and return the sum of each element.
    return sum(rolls)



# The following is like an int main(void) statment.
# All modules have a __name__ identifier. Identifiers that begin and end
# with 2 underscores are meant to be used, but they are Python specific;
# developers should not make their own double-underscore identifiers.
# Modules that are run from the commandline by the Python interpreter
# are given the value of "__main__" to their __name__ identifier. Hence,
# the following line is quite literal:
if __name__ == "__main__":
    # All functions have a return value, even if it is not explicit.
    returnvalue = test_types()
    print "test_types returned the value of: %s" % returnvalue

    # Strings can be manipulated in so many ways.
    print "We can also " + "concatenate strings with the add operator."
    # Python exhibits many language behaviors. If there is an exceptional
    # situation, we can wrap the potential situation in a try/except block.
    try:
        print "But we cannot concat a string and a " + 1
    except TypeError as err:
        # Errors can be aliased, and errors are almost always printable.
        print "Got an error:", err
    
    # Python variables are untyped. Declaration and definition is one step.
    faces = 6
    # We use a tuple, an immutable list-like type, when we have multiple
    # replacements to make in an old printf like string. tuples will show
    # up in other natural parts of python.
    print "Rolling a %d sided die once = %s" % (faces, roll(faces))

    times = faces/2
    # Python also offers formatting strings. The format method, and the
    # associated tokens, are extremely powerful. This is a very simplistic
    # use of them.
    print "Rolling a {0} sided die {1} times = {2}".format(faces, times, roll(faces, times))

    # When we import a module but don't alias it, we have access to exposed
    # parts of the module. Here we can take a look at any arguments passed
    # into the script.
    
    # Many items in Python are iterable, like sys.argv which is a list.
    # To get the length of an iterable, we use the builtin len() function.
    print "%d argument%s passed in." % (len(sys.argv),
           # While this is not good style, we can see that things that are
           # not block indents can pretty much be indented anyway we want.
           # The following is a ternary operation in Python to test for
           # pluralization.
           "s" if len(sys.argv) else "")

    print "Arguments passed in:"
    for arg in sys.argv:
        # For loops are used to iterate iterables (circular definition not
        # intended). Lists, tuples, even strings are all iterable.
        # In this way, we get a reference to each element of the list, from
        # index 0 to index N.
        # In the format string the number is not needed if we wish this
        # to behave like the old mod format (first in, first out).
        print "{}".format(arg)
