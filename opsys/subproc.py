import sys
import os
from subprocess import Popen, PIPE, check_output, CalledProcessError



if __name__ == "__main__":
    if len(sys.argv) > 1:
        # User passed in multiple files to read from the commandline, e.g.
        # python subproc test1.py test2.py
        files = sys.argv[1:]
        for f in files:
            cat = Popen(["cat", f], stdout=PIPE, stderr=PIPE)
            wc = Popen(["wc", "-l"], stdin=cat.stdout, stdout=PIPE, stderr=PIPE)
            wc_out = wc.communicate()
            print "%s has %s lines" % (f, wc_out[0].strip())
    else:
        # A simpler, single file line counter.
        f = raw_input("Which file should I count the lines for? ")
        if not f.strip():
            # Default to this file.
            f = __file__
            print "Defaulting to:", f
        try:
            # A cross platform friendly devnull.
            devnull = open(os.devnull, "w")
            # devnull standard error, not what we always want.
            stdout = check_output(["wc", "-l", f], stderr=devnull)
            # The natural output from wc -l looks like:
            #       24 08a_more_subproc.py
            # So we parse out the number of lines.
            print "%s has %s lines" % (f, stdout.split()[0])
        except CalledProcessError:
            print "Sorry, %s was a bad file." % f
            