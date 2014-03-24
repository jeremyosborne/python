import pygame
import pygame.locals
from pygame.locals import *
from random import random

from gameobject import GameObject

class Blob(GameObject):
    backgroundColor = (55, 151, 144)
    
    classification = "blob"

    # The life of a blob is determined by its health. The blob loses one
    # health every frame (essentially every update) and gains health when
    # it eats food.
    # Some blobs are faster than others, but every blob starts out with the
    # same health.
    health = 1000

    def __init__(self, gameworld, pos):
        super(Blob, self).__init__(gameworld, pos)

    # The update function will be called each frame to allow our
    # objects to update themselves.
    def update(self, gameworld):

        # The first thing we check is whether or not the blob is dead.
        if self.checkhealth(gameworld) == False:
            # Quick exit, we're dead.
            return

    # Checks the health of our blob and, if we are dead (health <= 0)
    # we remove ourselves from the world object.
    # We return a boolean, True if still alive, False if dead.
    def checkhealth(self, gameworld):
        # Update our health every frame.
        self.health -= 1
        if self.health <= 0:
            # Poor dead blobby.
            print "Sad news blob #{0} has passed on.".format(self.uniqueid)
            gameworld.removeobj(self)
            return False
        else:
            # We're still alive!
            return True
