# Regular Expressions are powerful.
# Unlike some languages, Regular Expressions are not builtins and need
# be imported before using.
import re
# Since regex does not allow for native patterns, we make patterns with
# strings. The following example demonstrates why raw strings are great.
test = "\\"
print "We have {} backslash.".format(len(test))
# Without raw strings, how many backslashes do we need? Lots.
# Because: backslashes are meaningful to the regex engine and the string.
print "Matches:", re.findall("\\\\", test)
print "Matches:", re.findall(r"\\", test)

# A test string.
test = """Kris Kringle, 
34th Miracle St., 
North Pole, 
3rd Rock,
kris@kringle.com"""
# Split on consecutive non-word characters.
print re.split(r"\W+", test)
# Replace consecutive numbers in a string.
print re.sub(r"\d+", "###", test)
# Replace only the first number.
print re.sub(r"\d+", "###", test, 1)
# Find consecutive word characters.
print re.findall(r"\w+", test)
# Escape special characters (make a pattern literal).
print re.escape("St.")
# Find cardinal directions, case-insensitive.
print re.findall(r"north|south|east|west", test, re.IGNORECASE) # or re.I
# Find the first word of a string.
print re.findall(r"^[^\W]+", test)
# Find the first word of each line of a multiline string.
print re.findall(r"^[^\W]+", test, re.MULTILINE) # or re.M
# Work with match objects with .match and .search.
# match must start matching on the first byte (even with multiline flag).
print re.match(r"^[\d]+", test, re.M)
# search will scan for the first match.
print re.search(r"^[\d]+", test, re.M)
# match objects make working with groups programmatically easier.
# Find a first and last name as named groups.
matches = re.search(r"^(?P<first>\w+) (?P<last>\w+)", test)
# Display our matches.
print matches.groups()
# Display the first match group.
print matches.group(1)
# Also display the first matched group.
print matches.group("first")
# Build a pattern.
pattern = "{}@{}\.com".format(matches.group("first"), 
                              matches.group("last"))
# Make it reusable and use it.
simple_email = re.compile(pattern, re.I) 
print simple_email.findall(test)
# Understand your regular expressions tomorrow morning.
print re.findall(r"""
                 [Kk]ris    # Sometimes he forgets to capitalize.
                 \          # whitespace must be explicit.
                 [Kk]ringle # Sometimes he forgets to capitalize.
                 """, test, re.VERBOSE) # or re.X
