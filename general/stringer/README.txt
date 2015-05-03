stringer
A small localization helper module
by Jeremy Osborne



REQUIREMENTS
============
* Python 2.x (development started with 2.7.2).



TODO
====
* Write a script that will scrape all of the code for calls to
  the assumed Stringer aliasing, sort of like gettext, for building a
  blank dictionary from all available files. (Starter code available in the
  scraper_teset file.)



USAGE
=====

    # For modules that are going to initialize the stringer with dictionaries.
    import stringer
    # For any module that will localize stringer.
    from stringer import Stringer as _

    # Load the dictionary file.
    stringer.loaddictionary("lang/en.ini")
    
    # Translate a simple key (when we know the object will be
    # serialized)
    _("_hello world")
    # or when we aren't sure
    _("_hello world").f()
    # We can also pass in arguments, labeled or not,
    # to be passed to .format() on the resulting translation.
    _("_hello world").f("dogs", cat="likes chicken")



RUNNING THE TESTS
=================
From this directory, execute:

    python runtests.py
