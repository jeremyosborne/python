# Sets: mutable list of distinct items.
# This literal notation is relatively new.
s = {1, 1, 1, 2, 3, 4}
print "What is in my set?", s
# Original set constructor.
s2 = set([4, 5, 6, 7])
print "Intersection of sets:", s & s2
print "Union of sets:", s | s2
# Mutable sets can be added to. Need to pass an iterable in.
s.update([5])
print "Intersection of sets:", s & s2
