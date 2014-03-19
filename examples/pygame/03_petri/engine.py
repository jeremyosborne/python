import pygame
import pygame.locals
from pygame.locals import *

class GameWorld(object):
    # Default Constants
    # The following are the dimensions of our window.
    windowWidth = 600
    windowHeight = 600
    # The following is a good color for our petri dish.
    backgroundColor = (254, 184, 188)
    fps = 40
    # Determines whether or not we should quit
    keepRunning = True
    # Property declarations, for no other reason than to keep things
    # organized.
    # These will be created during the __init__
    gameClock = None
    # The main viewport
    windowSurface = None
    
    def __init__(self):    
        # Create dynamic properties
        self.gameClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.windowWidth, self.windowHeight))

    # Call to run the game
    def run(self):
        # Loop until we get a quit signal of somekind
        while self.keepRunning:
        
            # Deal with events
            for event in pygame.event.get():
                # Handle general quit events
                if event.type == QUIT:
                    # It is up the game application to clean up when we quit.
                    self.keepRunning = False
                
            # clear the window surface
            self.windowSurface.fill(self.backgroundColor)

            # Update everything
            pygame.display.update()
            
            # Wait or speed up according to pygames timer.
            self.gameClock.tick(self.fps)
