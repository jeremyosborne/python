import pygame
import pygame.locals
from pygame.locals import *
from random import randint

from gameobject import GameObject

class Food(GameObject):
    backgroundColor = (131, 163, 59)
    
    classification = "food"

    # Food will also offer nutrition for our blobs that eat them.
    nutrition = 0
    
    def __init__(self, gameworld, pos):
        super(Food, self).__init__(gameworld, pos)

        # Randomize the nutrition that each piece of food offers.
        self.nutrition = randint(500, 1000)

    # When a morsel of food has had its nutrition reduced to zero,
    # it will be removed from play (it has been eaten).
    def update(self, gameworld):
        if self.nutrition <= 0:
            print "Morsel of food #{0} has been completely eaten.".format(self.uniqueid)
            gameworld.removeobj(self)
