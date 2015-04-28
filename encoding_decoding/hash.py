# Can use the hashlib to return the hash value of a string.
#
import hashlib

# File contents
with open("data/example.xml") as f:
    test = f.read()

# To see what hashes we have supported (new in 2.7)
print "What hash algorithms are available:", hashlib.algorithms

# To get the md5 using a hexadecimal system (i.e. no special, non
# printing characters):
md5_atonce = hashlib.md5(test)
print "md5 of file contents:", md5_atonce.hexdigest()

# To get the sha1 using a hexadecimal system (i.e. no special, non
# printing characters):
print "sha1 of file contents:",  hashlib.sha1(test).hexdigest()



# Read data in parts.
print "Reading in example data in parts:"
md5_inparts = hashlib.md5()
with open("data/example.xml") as f:
    for line in f:
        # Add our first string.
        md5_inparts.update(line)

print "md5 for file read in parts:", md5_inparts.hexdigest()

assert md5_atonce.hexdigest() == md5_inparts.hexdigest()
