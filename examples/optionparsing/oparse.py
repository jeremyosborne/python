'''
If we need to do option parsing for our program, while optparse is
deprecated, it is currently the most widely available parser available
in a standard distribution of Python.
'''

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", 
                  # Where this value ends up.
                  dest="filename",
                  # What is displayed in help.
                  metavar="FILE",
                  default="report.txt",
                  help="write report to FILE [default: %default]")
parser.add_option("-q", "--quiet",
                  dest="quiet",
                  # Equivalent to a boolean.
                  action="store_true",
                  default=False,
                  help="don't print status messages to stdout [default: %default]")
parser.add_option("-l", "--lines", 
                  # Certain type casting is available.
                  type="int", 
                  dest="lines",
                  default=10,
                  help="how many lines to add to the report [default: %default]")

options, args = parser.parse_args()

report_line = "All work and no play makes Jack a dull boy.\n"

if not options.quiet:
    print "Welcome to Report Writer 9000"
    print "Value of options.quiet: %s" % options.quiet
    print "Value of options.lines: %s" % options.lines
    print "Value of options.filename: %s" % options.filename
    print "Writing report..."
    
with open(options.filename, "w") as f:
    for i in range(options.lines):
        f.write(report_line)

# else things are quiet.
