import pygame
from Parametres import *

""" A class containing multiple functions to help manipulate objects or data """

pygame.init

#Extraire une image d'une spritesheet.
def getImgFromSpritesheet(x, y, width, height, spriteSheet, colorToRemove):
    image = pygame.Surface([width, height])
    image.blit(spriteSheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorToRemove)
    image = pygame.transform.scale(image, (20, 34))
    return image