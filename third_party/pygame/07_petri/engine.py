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

    worldObjects = None

    def __init__(self):    
        self.gameClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
    
        self.mousedownCallbacks = []
        self.keydownCallbacks = []
           
        self.worldObjects = []

    def addcallback(self, event, callback):
        if hasattr(self, event+"Callbacks"):
            getattr(self, event+"Callbacks").append(callback)
    
    def removecallback(self, event, callback):
        if hasattr(self, event+"Callbacks"):
            getattr(self, event+"Callbacks").remove(callback)

    def addobj(self, obj):
        self.worldObjects.append(obj)
        
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

            for obj in self.worldObjects:
                if hasattr(obj, "draw"):
                    obj.draw(self)

            pygame.display.update()
            
            self.gameClock.tick(self.fps)
