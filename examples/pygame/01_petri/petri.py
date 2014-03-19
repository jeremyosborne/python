# This will be our main loop.
# In this first example, we'll build a very basic game world that does
# nothing but show a screen.

# NOTE: pygame is not a canonical package. If you attempt to run this game
# on a python distribution of your own, you'll need to make sure pygame is
# installed.
# The following are basic modules necessary to running a pygame.
# Modules necessary to run the game
import pygame
import pygame.locals
# Pygame places "top level" constants and objects in the pygame.locals.
# This module is intended to be imported as is.
from pygame.locals import *

if __name__ == "__main__":
    # In a few lines of code, we'll get the general flow of our game.
    # As with all frameworks, we this will also give us a general idea of
    # what pygame helps us with, along with where we need to do our own
    # coding.
    
    # Initialize everything. This is a requirement before using any pygame
    # code.
    pygame.init()
    # Name our game window.
    pygame.display.set_caption('Petri Dish')
    
    # The clock is used to keep our game moving at the correct speed.
    gameClock = pygame.time.Clock()
    # Surfaces in pygame act as either background, which is what the window
    # surface is (a display surface) or as ways of displaying our game objects
    # (such as blobs and food).
    windowSurface = pygame.display.set_mode((600, 600))

    # We have a single run loop that manages everything.
    # Pygame tends to be pretty fast.
    # Each iteration of the run loop represents a single frame of the game.
    keepRunning = True
    while keepRunning:
        # Pygame listens for and detects user events, like mouse clicks
        # and keypresses. The only thing we're going to do is listen for
        # a quit event (which for us means hitting alt-f4 or clicking the
        # red X close button).
        for event in pygame.event.get():
            # Handle general quit events
            if event.type == QUIT:
                # It is up to the game application to clean up when we quit.
                keepRunning = False
        
        # Along with processing events, which will likely produce things that
        # need to be handled, we will also process our game element logic:
        # determining where blobs move to, how hungry they are, etc.
        
        # After processing all of the logic, there will be a draw phase where
        # Colors in pygame are passed as tuples of (Red, Green, Blue) values
        windowSurface.fill((0, 0, 0))
        # This causes all drawn surfaces to be rendered.
        pygame.display.update()
        # We check to make sure the game isn't running too fast or too slow.
        gameClock.tick(40)
        
    # Because pygame is resource heavy, whenever we're really done using it
    # it is good to clean up.
    pygame.quit()
