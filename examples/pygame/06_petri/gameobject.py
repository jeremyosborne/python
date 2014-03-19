import pygame
import pygame.locals
from pygame.locals import *
import math
import time

# We'll build a basic object that our other gameworld objects can inherit
# from. Since we have a simple world, it is easy to find relationships
# between our objects: they're all square, they don't have images,
# they'll all be drawn on the game world, etc.
# In real life, there will often be multiple ways of relating objects and
# sharing code, the trick there is the same as here: find and force ways
# to make your objects share code.
class GameObject(object):
    # How tall our basic object is in pixels.
    height = 10
    # How wide our basic object is in pixels.
    width = 10
    # The color of our basic object (black).
    backgroundColor = (0, 0, 0)
        
    # The center point position for our object.
    # This will be a tuple.
    pos = None
    # The rectangle used to enclose our object. Used for
    # drawing (blitting) and collision tests in the gameworld.
    rect = None
    # The image, known as surface, that will be displayed within our
    # rectangle. For various reasons, the collision rectangle (our rect param)
    # and our image (surface) might need to be of different sizes or shapes.
    # That is why we store two different objects instead of just one.
    surface = None
    
    # We'll categorize each of our objects.
    # Default objects are not classified.
    classification = None
    
    # A (hopefully) unique id for each game object.
    uniqueid = None
    
    # Our initialization will take a gameworld object and
    # the initial position where the food will be located at.
    # We'll use the gameworld to add ourselves to the run loop,
    # and the pos will be used to locate our initial position in
    # the world.
    def __init__(self, gameworld, pos):
    
        # Remember our center position
        self.pos = pos
        
        # Give ourselves a (hopefully) unique identifier
        self.uniqueid = time.time()
        
        # Build our encompassing rectangle based on where we clicked.
        # We build our objects based on the fact that the mouse
        # click should be the center point of the object creation,
        # but that rectangles are stored according to upper-left
        # coordinates.
        self.rect = pygame.Rect(pos[0]-self.width/2, 
                pos[1]-self.height/2,
                self.width, 
                self.height)
                
        # Create our surface. This is the visual piece of our object.
        # The argument must be a tuple.
        self.surface = pygame.Surface((self.width, self.height))
        # Color our surface.
        self.surface.fill(self.backgroundColor)
        
        # We need to add ourselves to the list of gameworld objects so that
        # we can draw and update ourselves.
        gameworld.addobj(self)
        
    # We are required to implement this method if we want to display
    # ourselves each frame.
    def draw(self, gameworld):
        # Here we use our rectangle to position our surface on the world.
        # The update function will be used to change our position. In our
        # simple example, we should be able to keep our draw function
        # as is.
        gameworld.windowSurface.blit(self.surface, self.rect)
