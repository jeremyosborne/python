"""Iterator interface.
"""

class HumanFriendlyCounter(object):
    """Class whose instances will be iterable.
    
    Iterate a count from 1 thru max, default 10.
    """
    def __init__(self, maximum=10):
        self.max = maximum

    def __iter__(self):
        """The initialization step for an iterator. Often implicitly
        called, for example, during the initialization of a for loop.
        """
        self.current = 0
        return self
    
    def next(self):
        """Each step of the iteration will respond to a call to next.
        When we are done, raise StopIteration.
        """
        if self.current < self.max:
            self.current += 1
            return self.current
        else:
            raise StopIteration()



c = HumanFriendlyCounter()
# c is an iterable and an iterator.
for number in c:
    print number


