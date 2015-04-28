""" Our base Die class.
"""

from random import randint

class Die(object):
    """Makes an n-sided die, default 6 faces.
    """
    def __init__(self, faces=6):
        if type(faces) != int:
            raise TypeError("faces must be an int")
        elif faces <= 0:
            raise ValueError("faces must be than 0")
        self.faces = faces

    def roll(self):
        return randint(1, self.faces)
    
    def __add__(self, other):
        if isinstance(other, Die):
            return self.roll() + other.roll()
        elif type(other) == int:
            return self.roll() + other
        else:
            raise TypeError("Can't add to type:", type(other))


if __name__ == "__main__":
    # Our own tests.
    d = Die()
    print d.roll()
    print d + 1000
    