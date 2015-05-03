"""
Chicken talk.

A simple morse code translator, designed to turn human speech into chicken
speech. Pass in a string and have it translated out to morse code.

The output should be able to be read literally by a (chicken) morse code
audio translator.
"""

import re
from StringIO import StringIO
import settings

dot = settings.DOT
dash = settings.DASH
element_gap = settings.ELEMENT_GAP
letter_gap = settings.LETTER_GAP
word_gap = settings.WORD_GAP

mcodehash = settings.MORSECODEHASH.copy()

# The reverse hash, used for translation from chicken back into human.
reverse_mcodehash = {}
for key, value in mcodehash.items(): 
    # For decoding, translate the keys up front.
    translated_key = value.replace(".", dot+element_gap).replace("-", dash+element_gap)
    # For our translation, any trailing element_gaps need to be trimmed.
    reverse_mcodehash[translated_key.rstrip()] = key

# Regular hash, for translation into chicken language. 
# Do this second since we'll overwrite the original.
for key, value in mcodehash.items():
    mcodehash[key] = value.replace(".", dot+element_gap).replace("-", dash+element_gap)



def encode(to_translate):
    """Encode a message into chicken.
    
    to_translate {string} To be translated into chicken.
    
    returns {string} A chicken translation of the dialog.
    """
    out = StringIO()
    for word in re.split(r"\s", to_translate):
        # Only letters that can be mapped will be translated, if they can't
        # they get dropped through.
        for letter in word:
            if letter.lower() in mcodehash:
                translated_letter = mcodehash[letter.lower()]
                if letter.isupper():
                    # Capitalize the chicken letter.
                    translated_letter = translated_letter.upper()
                out.write(translated_letter + letter_gap + element_gap)
            else:
                out.write(letter + element_gap + letter_gap + element_gap)
        # Add a word gap
        out.write(word_gap+element_gap)
    
    # Laziness. Remove any final gaps. Assume some punctuation
    # ends the sentence, or that we have a fragment.
    end_of_sentence_pattern = "("+element_gap+"|"+letter_gap+"|"+word_gap+")*$"

    return re.sub(end_of_sentence_pattern, "", out.getvalue())



def decode(to_translate):
    """Decode a message from chicken back into human.
    
    to_translate {string} To be translated into human.
    
    returns {string} A human translation of the dialog.
    """
    out = StringIO()
    # Due to how splitting works, we might, or might not, have spaces
    # remaining on either side of a word or letter gap.
    word_split_pattern = element_gap+"?"+word_gap+element_gap+"?"
    letter_split_pattern = element_gap+"?"+letter_gap+element_gap+"?"
    for word in re.split(word_split_pattern, to_translate):
        for letter in re.split(letter_split_pattern, word):

            print letter.__repr__()
            
            if letter.lower() in reverse_mcodehash:
                if letter.islower():
                    out.write(reverse_mcodehash[letter])
                else:
                    # upper case letter with lower case lookup key.
                    letter = letter.lower()
                    out.write(reverse_mcodehash[letter].upper())
            else:
                # Allow for debugging, or punctuation.
                out.write(letter)
        # Word separator for humans.
        out.write(" ")

    return out.getvalue()
            


if __name__ == "__main__":
    # Test code.
    decision = raw_input("Would you like to encode a message? [Y/n] ")
    if not decision or (decision and decision[0].lower() == "y"):
        to_translate = raw_input("Message to encode: ")
        print "Encoded message:"
        print encode(to_translate)
    else:
        to_translate = raw_input("Message to decode: ")
        print "Decoded message:"
        print decode(to_translate)
