import pygame
import pygame.locals
from pygame.locals import *

from engine import GameWorld

from food import Food
from blob import Blob


def petrimousedown(gameworld, event):
    if event.button == 1:
        Blob(gameworld=gameworld, pos=event.pos)

    elif event.button == 3:
        Food(gameworld=gameworld, pos=event.pos)

def petrikeydown(gameworld, event):
    if event.key == K_ESCAPE:
        print "Erasing the board."

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Petri Dish')

    petri = GameWorld()

    petri.addcallback("mousedown", petrimousedown)
    petri.addcallback("keydown", petrikeydown)
   
    # NEW CODE
    # Load a sound file to play as background music.
    # Change the path separators as appropriate.
    pygame.mixer.music.load('../resources/music.ogg')
    # Play forever, from the zeroth second.
    pygame.mixer.music.play(-1, 0.0)

    petri.run()
   
    pygame.quit()
