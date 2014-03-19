""" Functions do things with things you give them and often return
	results.
	
	Besides the basics we've already seen, here are a few more.
"""



def adder(message, *varargs):
	"""Add any integers passed to us.
	
	There isn't any formal way to document functions, although there are
	various doc tools. The following is an example of epydoc.
	
	@type message string
	@param message Require. What to announce before our sum?
	
	@param *varargs Optional. Numbers to add. Strings will attempt to be
	converted.
	"""
	# varargs is a list of our variable arguments.
	if not len(varargs):
		return

	total = 0
	# Variable args is a list.
	for potential in varargs:
		try:
			total += int(potential)
		except ValueError:
			print "%s cannot be converted to an int." % potential

	print "%s: %d" % (message, total)


adder("nothing")
adder("big money!", 100000, 42, 1)
# Applying an existing list as variable arguments.
things = [42, 1000, "chickens"]
adder("things", *things)



def counter(**keyargs):
	"""Functions can also except a variable list of labeled arguments.
	"""
	# dict is a dict of our variable arguments.
	if not len(keyargs):
		return

	total = 0
	# Variable args is a list.
	for key, val in keyargs.items():
		if type(val) == int:
			total += val
		else:
			print val, "on", key, "is not an int."
	print "counter total: %d" % (total)

counter(dog=1, chickens=3, cat="meow")
# Dictionaries can be applied as labeled arguments.
d = {"dog":1, "chickens":3, "cat":"meow"}
counter(**d)



def tupleized(a, b):
	"""Python supports a single return value.
	
	None by default.
	
	Multiple return values can be packed into a tuple.
	"""
	return b, a

r = tupleized("hi", "there")
print r



def mutator(obj):
	"""Attempt to mutate an object by adding a property.
	"""
	try:
		obj["mutated"] = True
	except:
		# fail silently
		pass

# Non-primitive items are passed by reference into a function.
d = {"hello": "world"}
mutator(d)
print "Are we mutated?", d["mutated"]
