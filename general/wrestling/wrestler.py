"""Class describing the wrestler.
"""

import db



def get_wrestlers():
    """Grabs a list of all of the wrestlers from the database.
    
    @return A list of Wrestler objects, or an empty list if no 
    wrestlers have been created.
    """
    wrestlers = db.get_wrestlers()
    return map(lambda w: Wrestler(**w), wrestlers)



class Wrestler(object):
    """A wrestler.
    """
    
    def __init__(self, **stats):
        # Bypass __getattr__, __setattr__
        self.__dict__["attrs"] = {
            "name": "NOBODY",
            "brawn": 5,
            "finesse": 5,
            "wins": 0,
            "losses": 0,
        }
        # Override via whatever is passed in.
        for name, value in stats.items():
            self.attrs[name] = value

    def __getattr__(self, attr):
        return self.attrs[attr]
    
    def __setattr__(self, attr, value):
        self.attrs[attr] = value
        
    def attrs_as_dict(self):
        """Returns a copy of our base attributes as a dictionary.
        """
        return self.attrs.copy()

    def save(self):
        """Attempt to persist the wrestler in the database.
        
        First attempt to create the wrestler. If this fails, attempt to
        update wrestler, assuming that a failure means wrestler already
        exists in the database.
        """
        # Try to create ourselves in the database first.
        try:
            db.create_wrestler(**self.attrs_as_dict())
        except ValueError as err:
            # If we throw an error here, let it float up.
            # It's something we want to debug.
            db.update_wrestler(**self.attrs_as_dict())
