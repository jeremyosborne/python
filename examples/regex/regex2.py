# Regular Expressions are a powerful tool, and are part of the
# Python language.
# The Python regular engine is full featured, but is a bit more
# programmatic than some other languages.

# First, import the regular expression module.
# Regular expressions are not part of the builtin core.
import re

# A major note: this is where raw strings can come in handy
# due to how backslashes work in both strings (for escaping)
# and regular expressions (escaping and special sequences).

# To see the example, let's say we have the following absurd
# test string made up of 1 backslash (two backslashes == 1 backslash
# in the string).
absurdtest = '\\'
# Confirm length
print "Length of absurdtest:", len(absurdtest)

# And we want to match the backslash with a regular expression
# expression. If we did the following, we are actually asking
# to match a single backslash.
# (The backslashes escape themselves in the string, and a double
# backslash gets escaped to a single backslash in the regexpression
# engine.)
print re.search('(\\\\)', absurdtest).group(0)

# Instead, raw strings to the rescue.
# In general, it's a good programming habit to have all regular
# expression pattern strings be raw strings.
# Here we'll match the single backslash correctly.
print re.search(r'(\\)', absurdtest).group(0)

# A test string.
test = "hello cool ROCK 3. The number 42 has 3.1415 liters of cool."

#### Simpler regular expression operations.
# split on a pattern
# \W = Match any non-alphanumeric character,
# equivalent to [^a-zA-Z0-9_]
print re.split(r"\W+", test)

# Find all the matches
# NOTE: This example uses lower-case w and is essentially the
# inverse of the split above (e.g. it's a word counter).
print re.findall(r"\w+", test)

# Replace all pattern matches in a string with the substitute string.
print re.sub(r"\w+", "censored", test)

# Build our own regular expression object that is reusable.
wordfinder = re.compile(r"\w+")
print wordfinder.findall(test)

#### Some other simple regular expression recipes.
# Match a number or decimal number.
# \d means any numeric character.
# + means 1 thru infinite number of matches.
# \. means match an actual dot, not use dot as a special character.
# ? means match 0 or 1.
# NOTE: This correctly skips the 3 in our test string above.
print re.findall(r"\d+\.?\d+", test)
# Match only if the preceding string also matches using a lookbehind.
# Needs a fixed width string.
# This will only match the first cool, not the second.
print re.findall(r"(?<=hello )cool", test)
# This will is the opposite of the above, an anti-match and
# will only match one cool, the second one. 
print re.findall(r"(?<!hello )cool", test)
# Match only the sequence of numbers that contains the values
# of 1, 4, or 5 of any length.
print re.findall(r"[145]+", test)
# Match any sequence of numbers made up of numbers from 0-9.
print re.findall(r"[0-9]+", test)
# Find any four letter words, case insensitive.
print re.findall(r"\b[a-z]{4}\b", test, re.I)

## The Match Object and the match and search methods.
# Difference between match and search:
# Match (which tends to be python specific) must begin matching
# at the very beginning of our target string, otherwise it will fail
# and return none.
# This will fail because the regular expression fails and returns
# None.
m = re.match("rock", test)
print m
# This will pass and return a match object.
m = re.search("rock", test)
print m

# Flags can be passed in, like ignore case.
m = re.search("WORLD", test, re.I)

# Working with Matched groups.
m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
# Return all groups (as a tuple)
print m.groups()
# The entire match
print m.group(0)
# The first parenthesized subgroup.
print m.group(1)
# The second parenthesized subgroup.
print m.group(2)
# The first and second subgroup (return type tuple).
print m.group(1, 2)
# Which index does the entire match start in.
print m.start()
# Which index does the entire match end in.
print m.end()
# Which index does the second group start in.
print m.start(2)
