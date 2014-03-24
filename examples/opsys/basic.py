import os


print "Our OS indicator:", os.name
# What environment variables are set.
print "env:", os.environ
# Value of a specific environment variable.
print "PATH:", os.environ["PATH"]
print "PATH:", os.path.expandvars("$PATH")

print "cwd:", os.getcwd()
# Get directory containing this file, even if executed from elsewhere.
d = os.path.realpath(os.path.dirname(__file__))
print "cwd of script (likely same as above):", d

somedir = os.path.join(d, 'somedir')
os.mkdir(somedir)
print "ls after making a directory", os.listdir(d)
# like rm -r for dirs.
os.removedirs(somedir)
print "ls after removing a directory", os.listdir(d)

