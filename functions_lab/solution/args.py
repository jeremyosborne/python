""" Lab for working with function signatures.

    import sys for using sys.argv.
    import os for using os.path.join.
    Refer to the docs for how to use os.path.join.
    
    Write a commandline script that accepts n number of strings.
    Not including the execution script in sys.argv, combine all of the
    commandline options into a single path using os.path.join.
    print the path out to the screen.
    Your code must allow for a variable number of options/pathparts.
    (The path does not have to be valid.)
    If the user does not pass in any options, print a usage message.
"""

import sys
import os



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: python {} part1 part2 ....".format(sys.argv[0])
    else:
        print os.path.join(*sys.argv[1:])
