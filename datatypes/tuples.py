
# Tuples: immutable list-like structures.
# Very similar to lists, but being immutable, their semantics, while not
# strictly enforced, can be powerful. (A coordinate on the globe is easily,
# semantically expressed as a simple tuple.)

# Two ways to create an equivalent tuple.
t = (1, 2, 'hello')
t2 = 1, 2, 'hello'
# Python supports shallow comparisons between tuples (and lists).
print "Is t and t2 equal?", t == t2
print "t has {} elements".format(len(t))
# Can read...
print "Item at index 0:", t[0]
# ...but can't write.
try:
    t[0] = 1000
except TypeError as err:
    print "Nope, can't change it. Got error:", err
# Tuples, acting as a semantic package, can be unpacked into equivalent
# number of variable.
a, b, c = t
print "a:", a
print "b:", b
print "c:", c
# Syntax for a single element tuple.
# No.
t3 = ("hello")
# Yes (trailing comma).
t4 = ("hello",)
print "t3 has type:", type(t3)
print "t4 has type:", type(t4)


