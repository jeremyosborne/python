'''
Django friendly JSON encoder.

# Basic usage
from jsonencoderdelegator import JSONEncoderDelegator
# Construct
json = JSONEncoderDelegator()
# Encode regular JSON friendly data 
# plus anything that implements a .tojsonobject() method
# plus anything iterable that doesn't get handled by the regular encoder, 
# but will assume that if an iterable is not normal that the objects contained
# must implement the .tojsonobject() method.
json.encode(json)
'''

import json

class JSONEncoderDelegator(json.JSONEncoder):
    """Wrapper for the JSON encoder that attempts to delegate the encoding
    of JSON objects to the object itself prior to attempting to serialize
    the object.
    """
    def default(self, o):
        """Override the default function.
        
        Method called when the JSONEncoder can't decide what to do with
        the object. That object will be passed to this function, and we have
        the option of dealing with it, or throwing an error.
        """
        if hasattr(o, "tojsonobject"):
            return o.tojsonobject()
        else:
            # attempt to process iterable object that might contain 
            # jsonserialize-able objects.
            try:
                items = []
                for item in o:
                    # Just assume, but look for attribute error.
                    # ASSUMPTION: if we get a dictionary like object, we
                    # assume we'll fail as keys shouldn't have a 
                    # .jsonserialize method.
                    items.append(item.tojsonobject())
                return items
            except (TypeError, AttributeError) as err:
                # Fall through, let the native JSONEncoder raise an error.
                pass
        return json.JSONEncoder.default(self, o)
