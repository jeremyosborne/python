import pygame
import pygame.locals
from pygame.locals import *

class GameWorld(object):
    windowWidth = 600
    windowHeight = 600
    backgroundColor = (254, 184, 188)
    fps = 40
    keepRunning = True
    gameClock = None
    windowSurface = None
    
    mousedownCallbacks = None
    keydownCallbacks = None
    #
    # This will end up being the list of participants in our little
    # petri dish.
    worldObjects = None

    def __init__(self):    
        self.gameClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
    
        self.mousedownCallbacks = []
        self.keydownCallbacks = []
    
        # Create our object list.       
        self.worldObjects = []

    def addcallback(self, event, callback):
        if hasattr(self, event+"Callbacks"):
            getattr(self, event+"Callbacks").append(callback)
    
    def removecallback(self, event, callback):
        if hasattr(self, event+"Callbacks"):
            getattr(self, event+"Callbacks").remove(callback)

    # This will add an object to the gameworld.
    def addobj(self, obj):
        # NOTE: We might want to check if the object exists first, but for
        # our simple example, we should only ever be adding objects that
        # don't yet exist in our world.
        self.worldObjects.append(obj)
        
    # For when we want to remove an object. (Food gets eaten, blob dies, etc.)
    def removeobj(self, obj):
        self.worldObjects.remove(obj)

    def run(self):
        while self.keepRunning:
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keepRunning = False

                if event.type == MOUSEBUTTONDOWN:
                    for callback in self.mousedownCallbacks:
                        callback(gameworld=self, event=event)

                if event.type == KEYDOWN:
                    for callback in self.keydownCallbacks:
                        callback(gameworld=self, event=event)

            self.windowSurface.fill(self.backgroundColor)

            # Loop through all objects in the game world and draw them.
            for obj in self.worldObjects:
                # We'll be over cautious and check to see if the object
                # has a draw item on it.
                if hasattr(obj, "draw"):
                    # We need to give the object access to gameworld.
                    obj.draw(self)

            pygame.display.update()
            
            self.gameClock.tick(self.fps)
