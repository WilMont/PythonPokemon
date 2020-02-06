import pygame

pygame.init

display_width = 800 #Longueur de la fenêtre.
display_height = 645 #Hauteur de la fenêtre.

# Déclaration des couleurs.
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
DIMGREY = (105,105,105)
SILVER = (192,192,192)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255, 0, 150)
BRIGHT_RED = (200,0,0)
BRIGHT_GREEN = (0,200,0)
 
block_color = (53,115,255)
 
player_width = 14 #Longueur de la hitbox du joueur.
player_height = 21 #Hauteur de la hitbox du joueur.
 
gameDisplay = pygame.display.set_mode((display_width,display_height)) #Prend les valeurs de longueur et largeur et les assigne à la fenêtre.
pygame.display.set_caption('Pykemon') #Titre affiché en haut de la fenêtre.

gameIcon = pygame.image.load('ProjetFinalPython/img/PlayerBaseSprite.png') #Icône de la fenêtre (en haut à gauche).
pygame.display.set_icon(gameIcon)

clock = pygame.time.Clock()
clock.tick(1) 



