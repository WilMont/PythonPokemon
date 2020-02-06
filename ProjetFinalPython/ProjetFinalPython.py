import pygame
import time
import random
import os
from Classes import *
from Parametres import *
from Tools import *
from urllib.request import urlopen
import io


 
pygame.init()
 
background_image = pygame.image.load('ProjetFinalPython/img/BackgroundCity3.png').convert()
spriteSheet = pygame.image.load("ProjetFinalPython/img/PlayerMovementSpritesheet.png")


 
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
    
#Fonction pour afficher l'écran lorsque l'on a perdu.
def perdre():
    
    
    largeText = pygame.font.SysFont("courier",115)
    TextSurf, TextRect = text_objects("Perdu", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        button("Rejouer",150,450,100,50,BRIGHT_GREEN,GREEN,game_loop)
        button("Quitter",550,450,100,50,BRIGHT_RED,RED,quitgame)

        pygame.display.update()
        clock.tick(15) 

# Fonction pour afficher des boutons.
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("courier",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    
# Fonction pour quitter le jeu.
def quitgame():
    pygame.quit()

# Fonction pour fermer l'inventaire.
def closeInventory():
    global inventoryIsOpen
    inventoryIsOpen = False
    
# Fonction pour ouvrir l'inventaire.
def openInventory():
    global inventoryIsOpen
    inventoryIsOpen = True

    largeText = pygame.font.SysFont("courier",20)
    TextSurf, TextRect = text_objects("Backpack", largeText)
    TextRect.center = (200,15)
    gameDisplay.blit(TextSurf, TextRect)
    backpackSpritesheet = pygame.image.load("ProjetFinalPython/img/BagSprites/BackpackSpritesheetPINK.png")
    backpackImage = getImgFromSpritesheet(0, 186, 46, 64, backpackSpritesheet, PINK)
    backpackImage = pygame.transform.scale(backpackImage, (138, 192))
    bagInterfaceImage = pygame.image.load("ProjetFinalPython/img/BlueInventoryInterface.png")
    bagInterfaceImage = pygame.transform.scale(bagInterfaceImage, (display_width, display_height))
    gameDisplay.blit(bagInterfaceImage, [0,0])
    gameDisplay.blit(backpackImage, [175, 190])
    gameDisplay.blit(TextSurf, TextRect)

    pokeballCategoryFont = pygame.font.SysFont("courier",20)
    pokeballCategoryText = pokeballCategoryFont.render("Pokeballs", True, BLACK)
    gameDisplay.blit(pokeballCategoryText, [150,55])

    pokeballAndQuantity = str("- " + player1.inventory.pokeballs[0].name + " x" + str(player1.inventory.pokeballs[0].nbrInInventory))
    greatballAndQuantity = str("- " + player1.inventory.pokeballs[1].name + " x" + str(player1.inventory.pokeballs[1].nbrInInventory))
    ultraballAndQuantity = str("- " + player1.inventory.pokeballs[2].name + " x" + str(player1.inventory.pokeballs[2].nbrInInventory))
    masterballAndQuantity = str("- " + player1.inventory.pokeballs[3].name + " x" + str(player1.inventory.pokeballs[3].nbrInInventory))
    inventoryItemsFont = pygame.font.SysFont("courier",20)
    inventoryItemsText = inventoryItemsFont.render(pokeballAndQuantity, True, BLACK)
    gameDisplay.blit(inventoryItemsText, [400,100])
    inventoryItemsText = inventoryItemsFont.render(greatballAndQuantity, True, BLACK)
    gameDisplay.blit(inventoryItemsText, [400,130])
    inventoryItemsText = inventoryItemsFont.render(ultraballAndQuantity, True, BLACK)
    gameDisplay.blit(inventoryItemsText, [400,160])
    inventoryItemsText = inventoryItemsFont.render(masterballAndQuantity, True, BLACK)
    gameDisplay.blit(inventoryItemsText, [400,190])


    

    while inventoryIsOpen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    closeInventory()
        

        button("Close",700,600,100,45,BRIGHT_GREEN,GREEN,closeInventory)

        pygame.display.update()
        clock.tick(15) 
        

# Fonction pour fermer un combat.
def closeWildCombat():
    global wildCombatIsRunning
    wildCombatIsRunning = False
    
# Fonction pour démarrer un combat.
def openWildCombat():
    global wildCombatIsRunning
    wildCombatIsRunning = True

    # Variable turn=1 si tour du joueur1, turn=2 si tour du pokemon sauvage.
    turn = 1

    global wildPokemonFighting
    wildPokemonFighting = True

    gameDisplay.fill(WHITE)
    randomID = random.randint(1,10)
    wildPokemon = createPokemonFromAPI(randomID)

    # Va chercher l'url de l'image du pokémon du joueur 1 et convertit en image pour pygame.
    player1PokemonBackSpriteURL = player1.pokemons[0].backSprite
    player1PokemonBackSpriteSTR = urlopen(player1PokemonBackSpriteURL).read()
    player1PokemonBackSpriteFile = io.BytesIO(player1PokemonBackSpriteSTR)
    player1PokemonBackSpriteImage = pygame.image.load(player1PokemonBackSpriteFile)
    gameDisplay.blit(player1PokemonBackSpriteImage, [75,350])
    # Barre de vie du pokémon du joueur 1.
    healthbarPokemonPlayer1 = pygame.Surface((100,10))
    healthbarPokemonPlayer1.fill(GREEN)
    gameDisplay.blit(healthbarPokemonPlayer1, [70,340])
    pygame.draw.rect(gameDisplay, BLACK, (70, 340, 100, 10), 2)

    # Va chercher l'url de l'image du pokémon du sauvage et convertit en image pour pygame.
    wildPokemonFrontSpriteURL = wildPokemon.frontSprite
    wildPokemonFrontSpriteSTR = urlopen(wildPokemonFrontSpriteURL).read()
    wildPokemonFrontSpriteFile = io.BytesIO(wildPokemonFrontSpriteSTR)
    wildPokemonFrontSpriteImage = pygame.image.load(wildPokemonFrontSpriteFile)
    gameDisplay.blit(wildPokemonFrontSpriteImage, [600,100])
    # Barre de vie du pokémon sauvage.
    healthbarWildPokemon = pygame.Surface((100,10))
    healthbarWildPokemon.fill(GREEN)
    gameDisplay.blit(healthbarWildPokemon, [595,90])
    pygame.draw.rect(gameDisplay, BLACK, (595, 90, 100, 10), 2)

    # Interface grise en bas de l'écran.
    pygame.draw.rect(gameDisplay, GREY, (0, 445, 800, 200), 5)
    pygame.draw.rect(gameDisplay, GREY, (0, 445, 700, 200), 5) # Rectangle de gauche contenant les attaques du pokémon ou les pokeballs.
    pygame.draw.rect(gameDisplay, GREY, (0, 445, 500, 200), 5)
    pygame.draw.rect(gameDisplay, GREY, (500, 345, 300, 100), 5) # Rectangle contenant les informations sur le combat (tour de quel joueur, efficacité d'une attaque...).


    while wildCombatIsRunning == True:
        # Déroulement du combat.
        combatTextFont = pygame.font.SysFont("courier",20)
        informationText = combatTextFont.render("It's player 1 turn", True, BLACK)
        gameDisplay.blit(informationText, [510,350])

        button("Attack",700,505,100,45,GREY,SILVER,attackSystem)
        #button("Bag",700,505,100,45,GREY,SILVER,openInventory)
        button("Catch",700,550,100,45,GREY,SILVER,closeWildCombat)
        button("Run",700,595,100,45,GREY,SILVER,closeWildCombat)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    closeWildCombat()



        pygame.display.update()
        clock.tick(15)  
    

def startScreen():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        startScreen = pygame.image.load("ProjetFinalPython/img/StartScreen.png")
        startScreen = pygame.transform.scale(startScreen, (800, 645))
        gameDisplay.blit(startScreen, [0,0])

        button("C'est parti !",150,450,200,50,BRIGHT_GREEN,GREEN,game_loop)
        button("Quitter",550,450,100,50,BRIGHT_RED,RED,quitgame)

        pygame.display.update()
        clock.tick(15)
        
    
    

    
def game_loop():
    global inventoryIsOpen
    inventoryIsOpen = False
    global wildCombatIsRunning
    wildCombatIsRunning = False

    #Initialisation des joueurs.
    global player1
    player1 = Player()
    player1.initializePlayerInventory()
    player1BasePokemonPikachu = createPokemonFromAPI("pikachu")
    player1.pokemons.append(player1BasePokemonPikachu)
    global player2
    player2 = Player()
    player2.initializePlayerInventory()

    #Point d'apparition du joueur 1.
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0
    y_change = 0
 
 
    gameExit = False
 
    while not gameExit:

        gameDisplay.blit(background_image, [0,0])
        gameDisplay.blit(player1.img, [player1.posX,player1.posY])
        
        # Hitbox des arbres (pour ne pas marcher dessus).
        hitboxArbresHautGauche1 = InvisibleObject(0, 0, 130, 145, gameDisplay, YELLOW)
        hitboxArbresGauche1 = InvisibleObject(0, 0, 65, 645, gameDisplay, YELLOW)
        hitboxArbresBasGauche1 = InvisibleObject(0, 520, 130, 150, gameDisplay, YELLOW)
        hitboxArbresHaut1 = InvisibleObject(0, 0, 800, 80, gameDisplay, YELLOW)
        hitboxArbresHautDroite1 = InvisibleObject(580, 0, 155, 275, gameDisplay, YELLOW)
        hitboxArbresHautDroite2 = InvisibleObject(515, 70, 65, 75, gameDisplay, YELLOW)
        hitboxArbresDroite1 = InvisibleObject(645, 0, 155, 645, gameDisplay, YELLOW)
        hitboxArbresBasDroite1 = InvisibleObject(582, 390, 218, 255, gameDisplay, YELLOW)
        hitboxArbresBasDroite2 = InvisibleObject(517, 585, 283, 60, gameDisplay, YELLOW)
        #Zone de rencontre de pokémons sauvages (hautes herbes).
        zoneCapturePokemon = InvisibleObject(200, 585, 283, 60, gameDisplay, RED)

        
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            #Evènements lors d'appui sur les touches.
            if event.type == pygame.KEYDOWN:
                #Déplacements
                if event.key == pygame.K_LEFT:
                    x_change = -2
                    player1.img = pygame.transform.flip(player1.getImgFromSpritesheet(16, 46, 14, 21, spriteSheet), True, False)
                if event.key == pygame.K_RIGHT:
                    x_change = 2
                    player1.img = player1.getImgFromSpritesheet(16, 46, 14, 21, spriteSheet)
                if event.key == pygame.K_UP:
                    y_change = -2
                    player1.img = player1.getImgFromSpritesheet(16, 69, 14, 21, spriteSheet)
                if event.key == pygame.K_DOWN:
                    y_change = 2
                    player1.img = player1.getImgFromSpritesheet(0, 23, 14, 21, spriteSheet)
                #Ouverture et fermeture de l'inventaire.
                if event.key == pygame.K_q and inventoryIsOpen == False:
                    openInventory()
                #Déclenchement d'un combat contre Pokemon sauvage.
                if event.key == pygame.K_e and wildCombatIsRunning == False:
                    openWildCombat()
 
            #Faire en sorte que le personnage ne bouge plus quand on lâche la touche.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
 
        x += x_change
        y += y_change
 

        player1.posX = x
        player1.posY = y
 
        if x > display_width - player_width or x < 0:
            perdre()

        
        pygame.display.update()
        clock.tick(30)

startScreen()
game_loop()

pygame.quit()
quit()