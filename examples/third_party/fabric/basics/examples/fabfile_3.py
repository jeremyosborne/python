"""
A contrived example: passing arguments to a fab task.
"""

# We aren't invoking anything fab-ish, it's plain Python code.

def hello(name="world"):
    print "Hello %s!" % name

def arg_type(name="world"):
    print "You gave me a:", type(name)
