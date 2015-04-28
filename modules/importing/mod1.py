
import mod2

# How many times does this statement show up?
print "mod1: init"

if __name__ == "__main__":
    print "mod1: list of mod2 attrs:", dir(mod2)
    
    # Why does this error out when we set this in mod2?
    try:
        print "mod1: x is:", x
    except NameError as err:
        print "mod1: could not find local x:", err
    
    print "mod1: mod2.x is:", mod2.x
