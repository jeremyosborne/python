""" Basic I/O handling in python.
"""

# For script arguments.
import sys
import os
# For random dates.
from random import randint
from datetime import datetime, timedelta



def random_date():
    """Generate a random date.
    """
    # Randomized date into the past.
    now = datetime.now()
    delta = timedelta(days=randint(1, 365))
    return now - delta



if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Assume user passed us a filename from commandline.
        fpath = sys.argv[1]
    else:
        # Prompt for a file name.
        fpath = raw_input("Please provide a filename: ")

    # Opening files can be error prone...
    try:
        if os.path.exists(fpath):
            raise IOError("No overwriting existing files.")
        
        # datetime formatting string. Need a newline when calling write.
        output = "{:%Y-%m-%d %H:%M:%S}: Something Happened\n"
        # Will close the file when we're done with the with loop for us.
        with open(fpath, "w") as f:
            for i in range(10):
                f.write(output.format(random_date()))
        # If we didn't use with, we should clean up with.
        # f.close()
        
        with open(fpath, "r") as f:
            # Files are iterable.
            for line in f:
                # Get rid of extra newlines.
                print line.rstrip()

        # Remove our testfile, and we're done.
        print "Removing test file:", fpath
        os.remove(fpath)
    except IOError as err:
        print "File error {}, {}".format(fpath, err)

