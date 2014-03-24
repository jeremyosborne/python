"""Lambdas are single statement functions with implicit returns.

Useful in functional programming where we don't want to make code.
"""

# This...
f = lambda x: x + 1

# ...is equivalent to this.
def g(x):
    return x + 1

assert f(1) == g(1), "f and g are equivalent in this example."

print "f and g must have been equivalent."
