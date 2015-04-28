""" Python has the concept of truthy and falsey, as in some things can
	pass a truth check, and some things will fail a truth check besides
	True and False.
"""

# Not truthy.
falsehoods = [None, False, 0, 0L, 0.0, 0j, "", (), [], {}]

while len(falsehoods):
	truthcheck = falsehoods.pop()
	if not truthcheck:
		print "%s is not truthy." % repr(truthcheck)

