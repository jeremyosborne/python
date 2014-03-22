Lab
===

* Make a Die class in the die.py file.
* Die instances can be constructed with a faces argument, defaults to 6, that is stored in the faces attribute on the instance.
* Die will throw a TypeError during init if faces is not an int.
* Die will throw a ValueError during init if faces is not > 0.
* Die implements a roll method that returns a random number between 1 and self.faces.
* Die will implement the __add__ operator. It should allow adding of a self.roll with either an integer or another Die instance. If other instance is a Die, call other.roll.
* Die will throw a TypeError from the __add__ override if other is not an int or Die instance.
* You might want to test your code in an if __name__ == "__main__" statement.



* Make a D6 class and a D20 class in dice.py.
* Both D6 and D20 inherit from Die (import die.py).
* D6 and D20 should not allow arguments to __init__.
* D6 should call it's parent init and pass faces=6 (or just assume default value).
* D20 should call it's parent init and pass faces=20.
* You might want to test your code in an if __name__ == "__main__" statement.



* When you think you are done, or as you are working, run tests.py. You are done when test.py passes and you have no more questions about your code.
