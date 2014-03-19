import pygame
import pygame.locals
from pygame.locals import *

# We're pushing most of the work off to our GameWorld
# object that we'll create.
from engine import GameWorld

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Petri Dish')

    # Initialize our game application.
    petri = GameWorld()
   
    # Begin the run loop for our game.
    petri.run()
   
    pygame.quit()
