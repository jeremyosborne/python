import pygame
import pygame.locals
from pygame.locals import *
from random import random

# Our parent class.
from gameobject import GameObject

class Blob(GameObject):
    # The color of our blobs (bluish).
    backgroundColor = (55, 151, 144)
    
    # Classification for a blob.
    classification = "blob"

    def __init__(self, gameworld, pos):
        # Most of the work occurs in our parent class.
        # We can use the super function because our classes are new style
        # classes. Note: you cannot always use the super function with
        # frameworks, especially frameworks that don't use newer style
        # classes.
        super(Blob, self).__init__(gameworld, pos)

