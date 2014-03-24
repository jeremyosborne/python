import pygame
import pygame.locals
from pygame.locals import *
from random import randint

from gameobject import GameObject

class Food(GameObject):
    backgroundColor = (131, 163, 59)
    
    classification = "food"

    nutrition = 0
    
    def __init__(self, gameworld, pos):
        super(Food, self).__init__(gameworld, pos)

        self.nutrition = randint(500, 1000)

    def update(self, gameworld):
        if self.nutrition <= 0:
            print "Morsel of food #{0} has been completely eaten.".format(self.uniqueid)
            gameworld.removeobj(self)

    # Interface for food objects to provide nutrition to other objects.
    # Always returns an integer.
    def providenutrition(self):
        if self.nutrition > 0:
            # Give a random value of nutrition.
            feed = randint(1, self.nutrition)
            self.nutrition -= feed
            return feed
        else:
            return 0
