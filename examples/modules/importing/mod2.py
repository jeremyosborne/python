
# How does python deal with circular references?
import mod1

print "mod2: init"

# Local x.
x = 100

# Part of the experiment, not recommended in general.
mod1.x = 1

print "mod2: local x: %s" % x
print "mod2: mod1.x value: %s" % mod1.x


