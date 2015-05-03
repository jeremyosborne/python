import unittest
import stringer
import os

# What directory is this test located in? We assume test
# files are relative to this directory.
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ENGLISH_TEST_PATH = os.path.join(THIS_DIR, "test_files", "en.ini")
DEUTSCH_TEST_PATH = os.path.join(THIS_DIR, "test_files", "de.ini")
NOSECTION_TEST_PATH = os.path.join(THIS_DIR, "test_files", "bad_nosection.ini")
# Non-existant file, restricting it here just to make sure
# it really doesn't exist.
NOEXIST_TEST_PATH = os.path.join(THIS_DIR, "test_files", "does_not_exist")


# Remember the default setting for the DICTIONARY_KEY
default_dictionary_key = stringer.DICTIONARY_KEY

# For the sake of tests, turn on the debug statements
stringer.DEBUG = True

class TestStringer(unittest.TestCase):
    def tearDown(self):
        stringer.DICTIONARY_KEY = default_dictionary_key
        stringer.deldicts()
        
    def testDelDicts(self):
        # This is a simple test to make sure our function works before
        # proceeding, as we use this in tearDown.
        # This will only work as long as DICTIONARIES is a simple dictionary.
        stringer.DICTIONARIES = {"dog": "cats"}
        stringer.deldicts()
        self.assertEqual(len(stringer.DICTIONARIES),
                         0,
                         "deldicts deletes all dictionaries..")

    def testDelDict(self):
        stringer.DICTIONARIES = {"dog": "cats"}
        stringer.deldict("dog")
        self.assertEqual(len(stringer.DICTIONARIES),
                         0,
                         "deldict deletes a single dictionary.")

    def testSetKey(self):
        stringer.setkey("de")
        self.assertEqual(stringer.DICTIONARY_KEY,
                         "de",
                         "setkey changes the DICTIONARY_KEY.")


    def testBadLoadDictionary(self):
        self.assertRaises(IOError,
                          stringer.loaddictionary, 
                          NOEXIST_TEST_PATH)
        self.assertRaises(TypeError,
                          stringer.loaddictionary,
                          NOSECTION_TEST_PATH)
        self.assertEqual(len(stringer.DICTIONARIES), 
                         0,
                         "Dictionary count not changed for bad files.")
    
    def testLoadDictionary(self):
        stringer.loaddictionary(ENGLISH_TEST_PATH)
        
        self.assertEqual(len(stringer.DICTIONARIES), 1,
                         "1 Dictionary should have been loaded.")
        
    def testStringer(self):
        stringer.loaddictionary(ENGLISH_TEST_PATH)
        
        _ = stringer.Stringer
        
        self.assertEqual(_("_dogs and cats blah blah blah"),
                         "_dogs and cats blah blah blah",
                         "Unmatched keys returned as is.")
        
        self.assertEqual(_("_hello world"), 
                         "hello world",
                         "Direct translation works.")
                
        self.assertEqual(_("_ACTOR hits TARGET"), 
                         "{actor} hits {target}",
                         "Formatting characters are not munged.")

        self.assertEqual(_("_ACTOR[NAME] hits TARGET[NAME]"),
                         "{actor[name]} hits {target[name]}",
                         "Formatting characters are not munged.")

        self.assertEqual(_("_ACTOR.NAME hits TARGET.NAME"),
                         "{actor.name} hits {target.name}.",
                         "Formatting characters are not munged.")

        self.assertEqual(_("_ACTOR hits TARGET").f(actor='chicken', target='cat'), 
                         "chicken hits cat",
                         "Formatting is performed.")
        
    def testMultipleDictionaries(self):
        stringer.loaddictionary(ENGLISH_TEST_PATH)
        stringer.loaddictionary(DEUTSCH_TEST_PATH)
        
        _ = stringer.Stringer
        
        self.assertEqual(_("_hello world"),
                         "hello world",
                         "'en' is our default language key.")
        
        stringer.setkey("de")
        
        self.assertEqual(_("_hello world"),
                         "Hallo Welt",
                         "Can change language keys and keep more than one dictionary in memory.")

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringer)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
if __name__ == '__main__':
    main()

