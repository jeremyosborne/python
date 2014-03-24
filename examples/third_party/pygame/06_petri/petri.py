import pygame
import pygame.locals
from pygame.locals import *

from engine import GameWorld
# TEST our gameobject
from gameobject import GameObject

def petrimousedown(gameworld, event):
    if event.button == 1:
        # MODIFIED CODE
        # TEST AGAIN
        GameObject(gameworld=gameworld, pos=event.pos)

    elif event.button == 3:
        # MODIFIED CODE
        # TEST AGAIN
        GameObject(gameworld=gameworld, pos=event.pos)

def petrikeydown(gameworld, event):
    if event.key == K_ESCAPE:
        print "Erasing the board."

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Petri Dish')

    petri = GameWorld()
   
    petri.addcallback("mousedown", petrimousedown)
    petri.addcallback("keydown", petrikeydown)
   
    petri.run()
   
    pygame.quit()
