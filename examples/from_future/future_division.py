# Make use of optional future features.

from __future__ import division
from __future__ import print_function

# print_function
print("this is now a print statement")
print("This is ", end="")
print("a single line print.")
print("Specifiable", "separator", sep=" ** ")
print("Optionally available in:", division.getOptionalRelease())
print("Feature available in:", division.getMandatoryRelease())

# division
print("Should now be 0.5, not 0:", 1/2)
print("Optionally available in:", division.getOptionalRelease())
print("Feature available in:", division.getMandatoryRelease())


