import pygame
import pygame.locals
from pygame.locals import *

from engine import GameWorld

# What we'll use to add blobs and food to the petri dish.
# Blobs will be added with a left click.
# Food will be added with a right click.
# We make sure to accept the named parameters that we'll be expecting.
# NOTE about the if/elif:
# We don't put an else because there are other button
# combinations that we wish to ignore, like a middle button
# press.
def petrimousedown(gameworld, event):
    # Differentiate between left (1) and right (3).
    # We'll also need to the coordinates for creating our blobs
    # and food treats.
    if event.button == 1:
        # left click
        # TEST
        print "Adding a blob at:", event.pos

    elif event.button == 3:
        # right click
        # TEST
        print "Adding food at:", event.pos

def petrikeydown(gameworld, event):
    # TEST: See what comes through with a key press. The pygame library gives
    # us constants that we can use to help match keys without needing to worry
    # about what system we're on.
    if event.key == K_ESCAPE:
        # TEST
        print "Erasing the board."

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Petri Dish')

    petri = GameWorld()
   
    # Add our interaction callbacks.
    petri.addcallback("mousedown", petrimousedown)
    petri.addcallback("keydown", petrikeydown)
   
    petri.run()
   
    pygame.quit()
