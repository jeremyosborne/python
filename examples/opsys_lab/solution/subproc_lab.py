# Run the ls -lh command and count the number of lines of 
# output from stdout.
# Display the number of lines from ls -lh.
# Count and display the number of directories.

from subprocess import check_output
import os
import re

stdout = check_output(["ls", "-lh"])

print "ls output %s lines." % len(stdout.split("\n"))

print "There are %s dirs." % len(re.findall(r"(?<="+os.linesep+")d", stdout))
