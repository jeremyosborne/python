import pygame
import pygame.locals
from pygame.locals import *
from random import randint

from gameobject import GameObject

class Food(GameObject):
    backgroundColor = (131, 163, 59)
    
    classification = "food"

    nutrition = 0

    # NEW CODE
    # Image to be shown for each food. Load once.
    # Change the directory slashes to be appropriate to your system.
    image = pygame.image.load("../resources/food.png")
    
    def __init__(self, gameworld, pos):
        super(Food, self).__init__(gameworld, pos)

        self.nutrition = randint(500, 1000)

        # NEW CODE
        # Override the old surface code and use an image.
        self.surface = self.image

    def update(self, gameworld):
        if self.nutrition <= 0:
            print "Morsel of food #{0} has been completely eaten.".format(self.uniqueid)
            gameworld.removeobj(self)

    def providenutrition(self):
        if self.nutrition > 0:
            feed = randint(1, self.nutrition)
            self.nutrition -= feed
            return feed
        else:
            return 0
