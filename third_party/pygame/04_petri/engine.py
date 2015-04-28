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
    
    def __init__(self):    
        self.gameClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.windowWidth, self.windowHeight))

    def run(self):
        while self.keepRunning:
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keepRunning = False

                # we deal with mouse down events.
                if event.type == MOUSEBUTTONDOWN:
                    # TEST
                    print "mousedown:", event
                
                # we deal with key down events
                if event.type == KEYDOWN:
                    # TEST
                    print "keydown:", event

            self.windowSurface.fill(self.backgroundColor)

            pygame.display.update()
            
            self.gameClock.tick(self.fps)
