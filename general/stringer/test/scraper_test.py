'''
Test out the file scraper.

See a better, long term solution in:
http://stackoverflow.com/a/8484835/193558
'''

import re

f = open("test_files/fakefile.py", "r")
data = f.read()
f.close()

funcfinder = re.compile(r"""
[^.]                 # Make sure the underscore is not a method call
_\([^\)]+\)          # Match our underscore stringer function
[^.]                 # when it is by itself
|                    # or
[^.]                 # Make sure the underscore is not a method call
_\([^\)]+\)          # Match our underscore stringer function
\.f\([^\)]*\)?       # followed by a call to the .f()rmat method.
""", re.VERBOSE)
funcs = funcfinder.findall(data)

print "Found {0} functions that match our criteria.".format(len(funcs))
for func in funcs:
    print func.rstrip()

# Extract the keys from the functions
lookupKeys = {}
for func in funcs:
    # When it is all said and done, we use find all and
    # grab the first match because the key will always be the argument
    # passed to the Stringer.
    key = re.findall(r"""
(?:_\([\"\']+)     # Match, but don't capture, our stringer call.
([^\"\']+)         # Match, and capture, the key string.
(?:[\"\']+\))      # Match, but don't capture, and string end.
""", func, re.VERBOSE)[0]
    # Collect all the unique keys
    lookupKeys[key] = True

print "Found these unique translation lookup keys:"
print lookupKeys
