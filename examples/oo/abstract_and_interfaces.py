from abc import ABCMeta, abstractmethod, abstractproperty



class User:
    """ An abstract base class that we use to enforce a few things
    and provide a few benefits for free.
    """
    
    # When using the ABCMeta module, we need our base class to have
    # its meta class set to ABCMeta.
    __metaclass__ = ABCMeta

    # Using the long form of property setting, we require subclasses
    # have a permissions property. We don't, and can't easily,
    # define what the permissions property is.
    def getpermissions(self):
        return self.permissions
    def setpermissions(self, permissions):
        self.permissions = permissions
    permissions = abstractproperty(getpermissions, setpermissions)

    def __iter__(self):
        """ Users are iterable.
        
        The permissions set for the user are what get iterated over.
        """
        for k in self.permissions:
            yield (k, self.permissions[k])
    
    def __len__(self):
        """ Users can be len'd.
        
        Return how many permissions a user has set.
        """
        return len(self.permissions)
    
    def __getitem__(self, name):
        """ When accessing the user as a dictionary, pass the check
        to the permissions property.
        """
        return self.permissions.get(name)
    
    def __setitem__(self, name, value):
        """ When setting the user as a dict, pass the assignment
        to the permissions property.
        """
        self.permissions[name] = value
    
    def __getattr__(self, name):
        """ If we attempt to access an attribute of an instance, and
        the attribute does not exist already on the instance, assume
        we are checking for permissions.
        """
        return self.permissions.get(name)

    @abstractmethod
    def __str__(self): 
        """ All subclasses must implement a string method.
        """
        pass



class FailUser(User):
    """ We can create this class, but attempting to instantiate it will
    fail.
    """
    pass



class NormalUser(User):
    """ A regular user.
    """
    def __init__(self, name):
        self.name = name
        # Define permissions as we're assumed to define it.
        self._permissions = { "read": True, "write": False, }
    
    @property
    def permissions(self):
        """Implement the required property.
        
        We are only required to implement, not keep the same signature
        (here we can only get permissions).
        """
        return self._permissions

    def __str__(self):
        """ Name, type, and permissions.
        """
        permissions = ", ".join("%s:%s" % (k, v) for k, v in self._permissions.items())
        return "%s (%s): %s" % (self.name, type(self).__name__, permissions)



class AdminUser(NormalUser):
    """King of all users.
    
    Does not need to implement abstractmethods/abstractproperties because
    parent class already did.
    """
    def __init__(self, name):
        super(AdminUser, self).__init__(name)
        self.title = "BDFL"
        # Make use of the fact that permissions gets set in parent init,
        # and we've inherited the __setitem__ from the base class.
        self["banhammer"] = True

    def __iter__(self):
        """ Iterate properties on the instance.
        
        Overrides inherited method. Not very useful, but interesting.
        """
        # When we need direct access, for getting or setting, attributes
        # on an instance, we can use the __dict__ magic attribute.
        return ((k, self.__dict__[k]) for k in self.__dict__)

    def __len__(self):
        """ Have len for the admin correspond to what would be iterated.
        """
        return len(self.__dict__)



if __name__ == "__main__":
    try:
        fu = FailUser()
    except BaseException as err:
        # As expected.
        print "Failed to create FailUser instance, reason:", err
    
    # NormalUser tests.
    normal = NormalUser("Egon")
    print normal

    print "Iterating normal", normal.name
    for k, v in normal:
        print "\t", k, v
    
    print "normal.name", normal.name
    print "normal.write", normal.write
    print "normal['write']", normal["write"]
    print "normal.banhammer", normal["banhammer"]
    print "len(normal)", len(normal)    

    try:
        # Python doesn't really offer a way to protect things other than
        # what could be called gentleperson agreements. We can, however,
        # provide warnings here and there when someone does something
        # that is in our opinion beyond acceptable.
        normal.permissions = { "banhammer": True }
    except BaseException as err:
        print "Cannot assign permissions to", normal.name

    # AdminUser tests. Different output from NormalUser, as expected.
    admin = AdminUser("Winston")
    print admin
        
    print "Iterating admin", admin.name
    for k, v in admin:
        print "\t", k, v

    print "admin.name", admin.name
    print "admin.write", admin.write
    print "admin['write']", admin["write"]
    print "admin.banhammer", admin.banhammer
    print "len(admin):", len(admin)
