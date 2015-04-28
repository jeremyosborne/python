import pygame
import pygame.locals
from pygame.locals import *
from random import randint

# Our parent class.
from gameobject import GameObject

class Food(GameObject):
    # The color of our food supply (greenish).
    backgroundColor = (131, 163, 59)
    
    # Classification for food.
    classification = "food"

    def __init__(self, gameworld, pos):
        # Most of the work occurs in our parent class.
        # We can use the super function because our classes are new style
        # classes. Note: you cannot always use the super function with
        # frameworks, especially frameworks that don't use newer style
        # classes.
        super(Food, self).__init__(gameworld, pos)
