""" Various string based mini labs.
"""



# Print out a checkerboard -- 8x8 grid with alternating light and dark
# squares -- and make use of the .format method on a string.
for i in range(8):
    if i % 2:
        print "{0}{1}".format("X", " ") * 4
    else:
        print "{0}{1}".format(" ", "X") * 4



# Break a string into (assumed) word chunks and print the words in reverse
# order, one on each line. Use either a regex or the .split method.
test = "hello world how are you?"
words = test.split()
words.reverse()
for word in words:
    print word

