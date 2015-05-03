"""
File used to test the scraping ability of the regular
expressions.
"""

# Setting up our fake functions and objects.
_ = lambda x: x
f = lambda x: x

class C(object):
    pass
obj = C()
obj.blah = lambda x: x

# A single letter function that we don't want
f("_key")

# Simple function call.
_("_key")

# The chained function call, in the simplest format (no args).
_("_key").f()

# The chained function call with simple arguments.
_("_key").f("hello", 1337)

# The chained function call with possible, more complex arguments
_("_key").f(obj.blah(), {"dog":"cat"})

# And then the possibility for long function calls to extend over one line
_("_key").f(
            "dogs",
            "cats",
            {"living":"together"})
