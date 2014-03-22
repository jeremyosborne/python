"""Python provides tools for most object oriented practices.
"""

class Employee(object):
    """New style classes look like this. They're not really new anymore.
    
    Style note: TitleCase class names to let people know their dealing with
    a class.
    """
    
    title = "Peon"
    """A class attribute. Prototypically referenceable if instance does not
    have its own attr of the same name."""
    
    def __init__(self, name):
        """Constructor method called when a class is called.
        
        All methods, init or otherwise, are implicitly passed the self
        reference argument as the first argument, however we
        must explicitly reference self in our class method signatures.
        When invoking methods, the first argument is bound and we pass in
        n-1 arguments.
        """
        
        # Python objects are dynamic by default. Acceptable way of creating
        # a "property."
        self.name = name

    def talk(self, message="How can I help you?"):
        """Allow our employee to talk.
        """
        return "{} says: {}".format(self, message)
    
    def __str__(self):
        """Python provides interface methods that can be overridden. 
        
        Equivalent to a .toString() type of method.
        """
        return "{} ({})".format(self.name, self.title)
    
    def __eq__(self, other):
        """Operators can be overridden, here the equality operator.
        
        Simple version: when an instance is on the left hand side, this
        method is implicitly called and we are passed a reference to the
        object on the right hand side of the operator.
        """
        # We can compare an instance to a class like so.
        if isinstance(other, Employee):
            return True
        return False



class Boss(Employee):
    """Boss inherits from Employee.
    """
    
    title = "Boss"
    """Override what we want to change.
    """
    
    def __init__(self, name):
        """Subclasses can explicitly call inherited methods.
        When we do explicitly pass self reference (method is unbound, it
        doesn't know).
        """
        Employee.__init__(self, name)
        
        # Stylistically, underscores denote private properties.
        self._bloodpressure = 100
    
    def talk(self, message=None):
        """Override the talk message.
        """
        return Employee.talk(self, "Like a boss.")
    
    @property
    def bloodpressure(self):
        """Computed property, declared with a decorator.
        Access to stress is as an attribute, not as a function.
        """
        # Likely not a good practice to make a getter have side effects,
        # but used here for demonstration.
        self._bloodpressure += 10
        return self._bloodpressure
    

if __name__ == "__main__":
    # No new keyword in Python. Call the class to instantiate.
    grunt = Employee("Idle")
    print "Employee name:", grunt.name
    print "Employee:", grunt
    print grunt.talk()
    print grunt.talk("I want a raise.")

    boss = Boss("Cleese")
    print "Boss Name:", boss.name
    print "Boss:", boss
    print boss.talk()
    print boss.talk("I want a raise.")
    
    print "Are Cleese and Idle equal?", boss == grunt

    print "Boss stress level:", boss.bloodpressure
    print "Boss stress level:", boss.bloodpressure
    print "Hidden props aren't actually hidden:", boss._bloodpressure
