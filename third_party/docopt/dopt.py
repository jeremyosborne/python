'''
Usage: oparse.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  write report to FILE [default: report.txt]
  -q, --quiet           don't print status messages to stdout [default: False]
  -l LINES, --lines=LINES
                        how many lines to add to the report [default: 10]
'''
# This example requires the third party module [docopt](http://docopt.org).
# 
#     pip install docopt
#     # for validation, something docopt lacks and optparse/argparse has
#     pip install schema
#     
# After installing, to get the best effect of how this module works:
# 
# * finish oparse.py
# * run `python oparse.py -h`
# * copy the help output into the docstring of this module
# * run this file




from docopt import docopt
from schema import Schema, Use

# the --lines parameter should be an integer, everything else is whatever.
schema = Schema({'--lines': Use(int, error='lines should be an int'),
                 object: object})

# Get the options.
options = docopt(__doc__)
# Validate and convert options to specific schema types from plain text.
options = schema.validate(options)

# Testing
#print(options)

# Slightly rewritten program from oparse.py
report_line = "All work and no play makes Jack a dull boy.\n"

if not options["--quiet"]:
    print "Welcome to Report Writer 9000"
    print "Value of options['--quiet']: %s" % options["--quiet"]
    print "Value of options['--lines']: %s" % options["--lines"]
    print "Value of options['--file']: %s" % options["--file"]
    print "Writing report..."
    
with open(options["--file"], "w") as f:
    for i in range(options["--lines"]):
        f.write(report_line)
