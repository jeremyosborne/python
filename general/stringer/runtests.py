"""
Used to execute the tests from the command line.
"""

# Make sure our test and package paths are available.
import sys
import os
# Setup our python paths to make sure the tests can find everything.
sys.path.append(os.getcwd())
sys.path.append(os.path.realpath('./test/'))

import test.stringer_test

# Run tests.
test.stringer_test.main()
