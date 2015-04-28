# Lists: mutable, mixedtype arrays.
# Semantics: lists are (often) more powerful when the data contained within
# are homogeneous.
l = [1, 2, 3]
# How many items?
print len(l)
# 0-based index.
print l[0]
# Mutable, but array boundaries enforced.
try:
    l[3] = "hi there"
except IndexError as err:
    print "oops, error:", err
# Can construct lists from any iterable, including strings.
letters = list("abc")
# We can enumerate a list as well as just iterate over it.
# The following technique also demonstrates unpacking. We'll see more 
# packing/unpacking as time goes on.
for i, letter in enumerate(letters):
    print i, letter
# Push an item onto our list.
l.append(4)
# Insert (index, value).
l.insert(0, 0)
print "Our list l:", l
# Remove items from our list.
print "Pop last item:", l.pop()
print "Shift first item:", l.pop(0)
print "Our list now has length:", len(l)
# We can check for the presence of items:
print "Is the number 2 in our list?", 2 in l
# Another way to remove items at a particular index: the del keyword
del l[1]
print "Is the number 2 in our list?", 2 in l
print "How many items are left?", len(l)
print "Our list:", l



