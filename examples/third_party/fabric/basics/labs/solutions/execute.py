
# Allow easy importing from examples.
import sys
import os
this_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, "..", "examples"))

from fabfile_3 import hello, arg_type

def execute(*args, **kwargs):
    try:
        hello(*args, **kwargs)
    except:
        print "You haz error in hello"
    
    try:
        arg_type(*args, **kwargs)
    except:
        print "You haz error in arg_type"

