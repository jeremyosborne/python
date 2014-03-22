""" Very basic unit tests for our module.

    Tests must pass for the lab to be considered complete.
"""

import unittest
import die
import dice



class TestDieClass(unittest.TestCase):
    def setUp(self):
        """All methods beginning with substring 'test' will be executed.
        """
        self.klass = die.Die
        self.d = die.Die()
    
    def tearDown(self):
        self.klass = None
        self.d = None
    
    def test_init(self):
        self.assertRaises(ValueError, self.klass, 0)
        self.assertRaises(TypeError, self.klass, "hello")
    
    def test_attrs(self):
        self.assertEqual(self.d.faces, 6, "Expected default value.")

        d20 = self.klass(20)
        self.assertEqual(d20.faces, 20, "Expected default value.")

    def test_roll(self):
        self.assertEqual(type(self.d.roll()), int, "roll produces an int.")
    
    def test_eq(self):
        self.assertRaises(TypeError, self.d.__add__, "dogs")
        
        # Some functional tests.
        try:
            self.d + 10
        except BaseException as err:
            self.fail(err)
        
        try:
            self.d + self.d
        except BaseException as err:
            self.fail(err)



class TestD6Class(TestDieClass):
    def setUp(self):
        """All methods beginning with substring 'test' will be executed.
        """
        self.klass = dice.D6
        self.d = dice.D6()

    def test_init(self):
        # This will always raise a TypeError since we don't allow args.
        self.assertRaises(TypeError, self.klass, 0)
        self.assertRaises(TypeError, self.klass, "hello")

    def test_attrs(self):
        self.assertEqual(self.d.faces, 6, "Expected default value.")



class TestD20Class(TestDieClass):
    def setUp(self):
        """All methods beginning with substring 'test' will be executed.
        """
        self.klass = dice.D20
        self.d = dice.D20()

    def test_init(self):
        # This will always raise a TypeError since we don't allow args.
        self.assertRaises(TypeError, self.klass, 0)
        self.assertRaises(TypeError, self.klass, "hello")

    def test_attrs(self):
        self.assertEqual(self.d.faces, 20, "Expected default value.")



if __name__ == '__main__':
    # Tests are kicked off using the main static method.
    unittest.main(verbosity=2)
    # Watch the output, should get an "OK" result.
