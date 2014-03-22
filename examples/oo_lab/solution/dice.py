""" Die subclasses.
"""

from die import Die


class D6(Die):
    """ Makes a 6 sided die.
    """
    def __init__(self):
        super(D6, self).__init__(6)


class D20(Die):
    """ Makes a 20-sided die.
    """
    def __init__(self):
        super(D20, self).__init__(20)


if __name__ == "__main__":
    d20 = D20()
    d6 = D6()
    print d20 + d6
    print d20.roll()
