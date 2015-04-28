""" Implementation of working multiple inheritance.
"""



class Particle(object):
    """ A particle in some position in 2d space.
    """
    def __init__(self, **keyargs):
        """ Set the initial position of the particle.
        """
        self.x = 0
        self.y = 0
    def update(self, dt):
        """ Update our particle every second, or fraction thereof, that
        passes.
        """
        pass
    def __str__(self):
        return "%s location: %sx, %sy" % (type(self).__name__, self.x, self.y)



class ParticleGravity(Particle):
    """ Adds the force of gravity to the particle.
    
    Assumes +y is up, and -y is down.
    """
    def __init__(self, **keyargs):
        # Make sure parent gets called, as well as next method in MRO.
        super(ParticleGravity, self).__init__(**keyargs)
    def update(self, dt):
        # Make sure parent gets called, as well as next method in MRO.
        super(ParticleGravity, self).update(dt)
        print "Gravity affecting particle",
        self.vy += -9.8*dt

class ParticleVelocity(Particle):
    """ Adds a 2d velocity to our particle.
    """
    def __init__(self, **keyargs):
        # Make sure parent gets called, as well as next method in MRO.
        super(ParticleVelocity, self).__init__(**keyargs)
        self.vx = keyargs["vx"]
        self.vy = keyargs["vy"]
    def update(self, dt):
        # Make sure parent gets called, as well as next method in MRO.
        super(ParticleVelocity, self).update(dt)
        print "Velocity affecting particle",
        self.x += self.vx * dt
        self.y += self.vy * dt



class FloatingParticle(ParticleVelocity):
    """ A particle that floats at constant velocity.
    """
    def __init__(self):
        # self.__class__ always points to the class of the instance.
        # We can only use self.__class__ in a leaf-node class.
        # Python 3.x has a nicer super() call.
        super(self.__class__, self).__init__(vx=1, vy=1)
    def update(self, dt):
        # What happens, and why, when we comment out the update method?
        super(self.__class__, self).update(dt)



class FallingParticle(ParticleVelocity, ParticleGravity):
    """ A particle that has its initial velocity affected by gravity.
    """
    def __init__(self):
        super(self.__class__, self).__init__(vx=1, vy=1)
    def update(self, dt):
        # What happens, and why, when we comment out the update method?
        super(self.__class__, self).update(dt)



if __name__ == "__main__":
    print "Making two particles, and modifying them over 10 seconds."
    particles = [FloatingParticle(), FallingParticle()]
    for i in range(10):
        for particle in particles:
            particle.update(1)
            print particle

print "\nWhat is the method resolution order for our classes?"
print "FloatingParticle:", FloatingParticle.mro()
print "FallingParticle:", FallingParticle.mro()
