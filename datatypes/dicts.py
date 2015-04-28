# Python mutable dictionary types provide unique key access.
# Keys can be any immutable type.
# Values can be any Python type.
d = {"chickens": 2, "cats": 5, None: 1000}
# Access.
print "How many have cats:", d["cats"]
print "How many have None:", d[None]
# Mutate on the fly.
d["dogs"] = 10
# dictionaries are iterable.
print "How many items in our dict?", len(d)
# Can iterate on the key in the dictionary.
for k in d:
    print k, d[k]
# dictionaries have a nice iterator helper.
for k, v in d.items():
    print k, v
# Tests against keys, not values.
print "Is cats in our dict?", "cats" in d


