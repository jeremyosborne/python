import pygame
import pygame.locals
from pygame.locals import *
from random import random

from gameobject import GameObject

class Blob(GameObject):
    backgroundColor = (55, 151, 144)
    
    classification = "blob"

    health = 1000

    speed = 0

    def __init__(self, gameworld, pos):
        super(Blob, self).__init__(gameworld, pos)

        self.speed = random()

    def update(self, gameworld):
        self.eat(gameworld)

        if self.checkhealth(gameworld) == False:
            return

        food = gameworld.getobjsbyclass("food")
        if len(food):
            closest = food[0]
            closestDistance = self.distancebetween(closest) 
            for morsel in food:
                distance = self.distancebetween(morsel)
                if distance < closestDistance:
                    closestDistance = distance
                    closest = morsel
            # MODIFIED CODE
            # Removed test output.
            
            # Now that we know the closest piece of food, let's move to it.
            # Figure out our direction relative from our blob to our target
            # in terms of a unit vector. 
            direction = self.headingfrom(closest)
            
            # Move us towards the food.
            self.pos = (self.pos[0] + direction[0]*self.speed,
                        self.pos[1] + direction[1]*self.speed)
            # Reposition our rectangle. Since our rectangle is already created,
            # we can move it via our position.
            self.rect.center = self.pos

    def checkhealth(self, gameworld):
        self.health -= 1
        if self.health <= 0:
            print "Sad news blob #{0} has passed on.".format(self.uniqueid)
            gameworld.removeobj(self)
            return False
        else:
            return True

    def eat(self, gameworld):
        food = gameworld.getobjsbyclass("food")
        if len(food):
            for morsel in food:
                if self.rect.colliderect(morsel.rect):
                    omnomnom = morsel.providenutrition()
                    self.health += omnomnom
                    print "Blob #{0} has gained {1} nutrition (total health:{2})".format(self.uniqueid, omnomnom, self.health)
                    return            
