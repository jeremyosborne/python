""" 
    Lab
    ---
    
    Using the iterutils, figure out the number of permutations possible when
    rolling two 6-sided dice. (Hint: Think cartesian product, not the
    permutations function.)
    
    Print the total number of permutations.
    
    Make a simple ascii chart that displays the count of permutations for
    a particular combination (i.e. sum of a permutation).
    
    Example:
    
    3 *
    4 **
    ... etc...
"""

from itertools import product
from collections import Counter



rolls = Counter()
for roll in product(range(1, 7), repeat=2):
    rolls[sum(roll)] += 1

print "Total permutations:", sum(rolls.values())

print "Distribution of rolls"
# Since the dataset is small, we don't normalize.
for total, numperms in rolls.items():
    print "{:2}".format(total), "*" * numperms
