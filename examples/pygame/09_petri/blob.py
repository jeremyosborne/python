import pygame
import pygame.locals
from pygame.locals import *
from random import random

from gameobject import GameObject

class Blob(GameObject):
    backgroundColor = (55, 151, 144)
    
    classification = "blob"

    health = 1000

    def __init__(self, gameworld, pos):
        super(Blob, self).__init__(gameworld, pos)

    def update(self, gameworld):
        # In our game, even starving blobs get a chance to eat before we
        # check on their health.
        self.eat(gameworld)

        if self.checkhealth(gameworld) == False:
            return

    def checkhealth(self, gameworld):
        self.health -= 1
        if self.health <= 0:
            print "Sad news blob #{0} has passed on.".format(self.uniqueid)
            gameworld.removeobj(self)
            return False
        else:
            return True

    # Blobs like to eat. See if there are any edible morsels in the gameworld.
    def eat(self, gameworld):
        food = gameworld.getobjsbyclass("food")
        if len(food):
            # Test for collisions, we'll eat whatever is the first morsel of
            # food we find.
            for morsel in food:
                if self.rect.colliderect(morsel.rect):
                    # Om nom nom.
                    omnomnom = morsel.providenutrition()
                    self.health += omnomnom
                    # TEST
                    print "Blob #{0} has gained {1} nutrition (total health:{2})".format(self.uniqueid, omnomnom, self.health)
                    # No need to check for more food.
                    return            
