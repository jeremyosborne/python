# Samples are small. Prove your answers by printing.

# Call list() on a string.
# How does the list constructor work?
items = list("hello world")
print items

# Call list() on a dict.
# What is the output and why?
l2 = list({"hello": "world", "and": "universe"})
print l2

# Convert this list to a tuple.
l3 = [1, 2, 3]
t = tuple(l3)
print t

# Compare the list [1, 2, 3] with the tuple (1, 2, 3).
# Why are they not equal?
print t == l3

# Compare the following two lists (different addresses in memory).
# Why are they equal?
l4 = [1, 2, 3]
l5 = [1, 2, 3]
print l4 == l5
