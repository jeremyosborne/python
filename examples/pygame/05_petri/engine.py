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
    
    # The lists of event handlers.
    # This will end up being a list of callback functions.
    mousedownCallbacks = None
    # This will also end up being a list of callback functions.
    keydownCallbacks = None

    def __init__(self):    
        self.gameClock = pygame.time.Clock()
        self.windowSurface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
    
        # Create our callback lists.
        self.mousedownCallbacks = []
        self.keydownCallbacks = []

    # We need an ability to add callback functions, but we will use some
    # functional programming tricks to make a single function do multiple
    # tasks.
    # This is where our callback lists having common naming conventions will
    # aid us.
    # Properties
    # event {str} The base name of the event: "mousedown" or "keydown".
    # callback {func} The function to call during the event.
    # The callback itself must accept two parameters, and their names
    # must be "gameworld" and "event". The gameworld will be a reference
    # to this object. The event will be a reference to the event object
    # that was triggered.
    def addcallback(self, event, callback):
        # First check to see if we have a callback for this particular
        # event type.
        if hasattr(self, event+"Callbacks"):
            # If we do, add the callback to our list of callbacks to
            # iterate through when the event happens.
            getattr(self, event+"Callbacks").append(callback)
    
    # We'll include the ability to remove callbacks, although we won't use
    # it in our code. Note that why we need to pass the original function
    # in for this to work is because the remove list function will only
    # work if the memory address is the same.
    def removecallback(self, event, callback):
        if hasattr(self, event+"Callbacks"):
            getattr(self, event+"Callbacks").remove(callback)

    def run(self):
        while self.keepRunning:
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keepRunning = False

                if event.type == MOUSEBUTTONDOWN:
                    # MODIFIED CODE
                    # Go through each of the mousedown handlers and pass
                    # the event object.
                    # Event event should have a pos and a button to determine
                    # what happens.
                    for callback in self.mousedownCallbacks:
                        # Execute the callback via the variable reference to
                        # the function.
                        # We name the parameters to give the callback function
                        # freedom to organize their parameters as they wish,
                        # but at the same time keeping a uniform interface.
                        callback(gameworld=self, event=event)

                if event.type == KEYDOWN:
                    # MODIFIED CODE
                    # Go through each key down event in the keydown callbacks
                    # and pass the event object.
                    # Each keydown will have the following props:
                    # unicode, key, mod
                    for callback in self.keydownCallbacks:
                        # Execute the callback via the variable reference to
                        # the function.
                        # We name the parameters to give the callback function
                        # freedom to organize their parameters as they wish,
                        # but at the same time keeping a uniform interface.
                        callback(gameworld=self, event=event)

            self.windowSurface.fill(self.backgroundColor)

            pygame.display.update()
            
            self.gameClock.tick(self.fps)
