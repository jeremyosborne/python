import pygame
import pygame.locals
from pygame.locals import *
from random import random

from gameobject import GameObject

class Blob(GameObject):
    backgroundColor = (55, 151, 144)
    
    classification = "blob"

    health = 1000

    # Since blobs can move, they have a speed (think pixels per frame).
    # We'll randomize the speed during initialization. The number here is
    # so things don't explode.
    speed = 0

    def __init__(self, gameworld, pos):
        super(Blob, self).__init__(gameworld, pos)

        # We'll use a fractional value for speed. Some blobs will be faster
        # than others, that's a fact of life.
        self.speed = random()

    def update(self, gameworld):
        self.eat(gameworld)

        if self.checkhealth(gameworld) == False:
            return

        # The primary job of a blob is to eat.
        # Find the closest bit of food and go after it,
        # but first we need to get a list of all of the objects.
        food = gameworld.getobjsbyclass("food")
        # If there is any food lying around:
        if len(food):
            # Loop through each one and figure out which food is the closest 
            # using the good old Pythagorean Theorem.
            # We'll assume that before the loop, our baseline is the first
            # food in the list.
            closest = food[0]
            closestDistance = self.distancebetween(closest) 
            for morsel in food:
                distance = self.distancebetween(morsel)
                # If this morsel is closer than the other, move towards it
                # instead.
                if distance < closestDistance:
                    closestDistance = distance
                    closest = morsel
            # TEST
            print "Blob #{0} is closest to Food #{1}.".format(self.uniqueid, 
                                                              closest.uniqueid)

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
