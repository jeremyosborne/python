"""Simple localization tool that allows passing of context objects to
the localizer.

Recommend importing this module as follows:

    # For modules that are going to initialize the stringer with dictionaries.
    import stringer
    # For any module that will localize stringer.
    from stringer import Stringer as _

The format for the individual dictionaries is the .ini Config File format.
The first (and only) section tag containing the individual dictionaries should 
be named the name of the DICTIONARY_KEY they correspond to. The remainder
of the file should contain nothing but key=value pairs or comments and nothing
more.

The key in the individiual dictionary correlates to the lookupString in
the stringer objects. The value is the translated string. The individual
dictionary translation strings can be either templates or plain strings,
however the dictionaries have no way of enforcing or informing that they
are template strings or plain strings.

Recommend having the key phrases in each dicitionary stand out in some way,
like having an underscore as the first character, although this, too, is not
enforced in any way.
"""

__version_info__ = (0, 0, 1)
__version__ = '.'.join((str(info) for info in __version_info__))

import ConfigParser

DEBUG = False
"""If true, output debugging statements to sys.stderr. Otherwise, no debugging
statements will be output.
@type: bool
"""

DICTIONARY_KEY = "en"
"""The default, and current, dictionary we are localizing against. The name
of each dictionary is not enforced against any form of language codes.
@type: str
"""

DICTIONARIES = {}
"""Cache of localization dictionaries, keyed by their dictionary key, and
referenced in localization by the currently set DICTIONARY_KEY.
@type: dict
""" 

def debug(message):
    """Write to standard out any debug messages, but only if the module
    is set to debug mode.
    
    @type message: str
    @param message: Debug message to display.
    """
    if DEBUG == True:
        print "stringer debug message: {0}".format(message)



def setkey(key):
    """Sets the DICTIONARY_KEY, which is the suggested interface
    for switching dictionary keys (includes debugging statements).
    
    @type key: str
    @param key: New dictionary key we will work with.
    """
    global DICTIONARY_KEY
    if key not in DICTIONARIES:
        debug("{0} is not a key within DICTIONARIES".format(key))
    DICTIONARY_KEY = key



def deldict(key):
    """Attempts to delete a specific dictionary.
    
    @type key: str
    @param key: Dictionary key to delete.
    """
    try:
        global DICTIONARIES
        del DICTIONARIES[key]
        debug("Deleted the {0} dictionary.".format(key))
    except KeyError:
        debug("Warning: Attempting to delete non-existant dictionary: {0}".format(key))



def deldicts():
    """Frees (deletes) all loaded dictionaries.
    """
    global DICTIONARIES
    DICTIONARIES = {}
    debug("All stringer dictionaries dropped.")



def loaddictionary(path, dictionary_key=None):
    """Read a dictionary file located at path and load into memory.
    By default, the dictionary key for the dictionary is defined in the
    dictionary file.
    
    Will throw an IOError if path does not lead to an existing file.
    
    Will throw a TypeError if the file is invalid or doesn't exist.
    
    @type path: string
    @param path: The full path to the localization dictionary file.
    
    @type dictionary_key: string
    @param dictionary_key: An optional parameter that, if included, will
    override the default dictionary key located within the file.
    """
    c = ConfigParser.ConfigParser()
    # Make things case sensitive
    c.optionxform = str

    debug("Attempting to open dictionary file at: {0}".format(path))

    # This will throw an IOError all by itself.
    f = open(path, "r")

    try:
        c.readfp(f)
        # Done with the file.
        f.close()
        # Only read the first section
        section = c.sections()[0]

        if DEBUG == True:
            debug("Retrieving dictionary for section: {0}".format(section))
            s = c.sections()
            if len(s) > 1:
                debug("Warning, dictionary file contains more than one dictionary.")
                debug("Ignoring the following sections:")
                s.pop(0)
                for ignoredSection in s:
                    debug(ignoredSection)
        
        # Section itself becomes a dictionary in our DICTIONARIES.
        DICTIONARIES[section] = {}
        for phrase, translation in c.items(section):
            DICTIONARIES[section][phrase] = translation
    except (KeyError, ConfigParser.MissingSectionHeaderError):
        raise TypeError("Error reading stringer dictionary file:" + path)
    



def lookup(key):
    """Lookup a particular key in the current dictionary.
    
    @type key: str
    @param key: The key phrase to lookup.
    
    @rtype: str
    @return: The value of the lookup key. The phrase itself will be returned
    if there is no lookup key in the corresponding dictionary.
    """
    try:
        return DICTIONARIES[DICTIONARY_KEY][key]
    except KeyError:
        debug("Warning: no translation for {0} lookup key in {1} DICTIONARY_KEY".format(
              key, DICTIONARY_KEY))
        return key



class Stringer(object):
    """Used for marking strings for localization.
        
    Recommend usage as (using the recommended importing):
    
    # For strings with no context objects (assuming it is used in a context
    # in which __str__ will be called).
    _("_hello world")
    
    # Forcing the localization without a context object, for situations
    # where we can't trust the operator overrides to happen, or when
    # we can't trust the __str__ method to be called.
    _("_hello world").f()
    
    # Example string with one context object, that being a list.
    _("_hello world").f(["hi there"])
    
    # Example string with 2 number of context objects, one a string, and
    # one a labeled dictionary.
    _("_hello world").f("blah", chicken={"dog":"cat"})

    """
    
    lookupString = None
    """The string to be used to lookup the translation string in the
    localization dictionary. The lookup string does not need have any templating
    in it, as it is not used for templating itself.
    @type: str
    """
    
    def __init__(self, lookupString):
        """Initializer.
        
        @type lookupString: str
        @param lookupString: The lookup key to our string localization
        dictionary.
        """
        self.lookupString = lookupString
    
    def f(self, *context, **keyedcontext):
        """Attempt to (f)ormat and translate this string according to the 
        current locale dictionary. This function need not be called if the
        class is going to be coerced into a string format, such as when
        in a print statement, AND if string will not be accepting any
        context arguments.
        
        @type context: mixed
        @param context: An optional set of context arguments that will be 
        dereferenced and passed to the format method on localization. 
        
        @type keyedcontext: mixed
        @param keyedcontext: An optional set of labeled arguments that will
        be dereferenced and passed into the format function.
        """
        if len(context) and not len(keyedcontext):
            return lookup(self.lookupString).format(*context)
        elif len(keyedcontext) and not len(context):
            return lookup(self.lookupString).format(**keyedcontext)
        elif len(context) and len(keyedcontext):
            return lookup(self.lookupString).format(*context, **keyedcontext)
        else:
            # No context, assume no formatting.
            return lookup(self.lookupString)
    
    def __str__(self):
        """Stringers are serialized via a lookup."""
        return lookup(self.lookupString)

    def __add__(self, other):
        """Attempt concatenation as string."""
        return self.__str__() + other
    def __radd__(self, other):
        """Attempt concatenation as string."""
        return self.__str__() + other
    
    def __eq__(self, other):
        """Attempt to compare equality as string."""
        return self.__str__() == other
    def __neq__(self, other):
        """Attempt to compare inequality as string."""
        return self.__str__() != other
