"""Decorators are function wrappers in Python.

Decorators are syntactic sugar.
"""



def increment_by_42(f):
    """A function meant to be a decorator.
    
    @param f The function we are going to wrap. This function is passed
    to us by the intepreter.
    
    @return A wrapped function.
    """
    def incrementor(*args):
        incremented = map(lambda n: n+42, args)
        return f(*incremented)
    
    return incrementor



# Apply our function wrapper.
@increment_by_42
def theanswer(*numbers):
    """Without wrapping, this function would just return the sequence.
    """
    return numbers

# Using a decorator is equivalent to:
#
#theanswer = increment_by_42(theanswer)
# 
# To see the effect, comment out the decorator above and uncomment the line above.



print "Results of our wrapped function:", theanswer(*range(5))
