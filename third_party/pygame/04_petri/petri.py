import pygame
import pygame.locals
from pygame.locals import *

from engine import GameWorld

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Petri Dish')

    petri = GameWorld()
   
    petri.run()
   
    pygame.quit()
