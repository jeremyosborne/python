import pygame
import pygame.locals
from pygame.locals import *
import math
import time

class GameObject(object):
    height = 10
    width = 10
    backgroundColor = (0, 0, 0)
        
    pos = None
    rect = None
    surface = None
    
    classification = None
    uniqueid = None

    def __init__(self, gameworld, pos):
    
        self.pos = pos
        
        self.uniqueid = time.time()
        
        self.rect = pygame.Rect(pos[0]-self.width/2, 
                pos[1]-self.height/2,
                self.width, 
                self.height)
                
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.backgroundColor)
        
        gameworld.addobj(self)
        
    def draw(self, gameworld):
        gameworld.windowSurface.blit(self.surface, self.rect)

    def distancebetween(self, target):
        return math.hypot(target.pos[0] - self.pos[0], target.pos[1] - self.pos[1])

    # Math is a big part of video games.
    # We need a unit vector, which is merely the heading our blob will move
    # in to find food.
    # Just like the distancebetween function, our arguments will be iterables of
    # the format (x, y).
    # What is different here is that while distance the order isn't important,
    # for our heading it is.
    # NOTE: For the math nerds, we are computing a unit vector between our blob
    # and our food target.
    def headingfrom(self, target):
        # Our slope will help us compute our magnitude
        direction = (target.pos[0] - self.pos[0], target.pos[1] - self.pos[1])
        # What is the magnitude of change, used for normalization?
        magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
        # Return a position tuple that matches the defintion of a unit vector:
        # where the magnitude of a unit vector == 1
        return (direction[0] / magnitude, direction[1] / magnitude)
