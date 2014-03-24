# This is an example of the batteries included approach to
# building a 'head' tool in python.
#
#! /usr/bin/env python

# Reads all input as files from sys.argv
import fileinput

# To handle errors, we need to create our iterator vefore our
# loop.
fileiterator = fileinput.input()

while True:
    try:
        # If we put a bad file name in, our iterator will break
        # when retrieving the line.
        for line in fileiterator:
            # We're just making the long string easier to see.
            s = str(fileinput.filelineno())
            s += ": (" + fileinput.filename() + "): "
            s += line.rstrip()
            print s
            if fileinput.filelineno() >= 10:
                fileinput.nextfile()
    except IOError:
        # Bad file name, just skip and try again.
        print "\nERROR: skipping file:", fileinput.filename(), "\n"
    else:
        # Must have been a good file, or no more files.
        # We're done.
        break

# Now try:
# python head2.py head1.py
# cat head.py | python head2.py
