import pygame
from Parametres import *
import requests

class Player():
    def __init__(self):
        #self.name = name
        self.posX = 0
        self.posY = 0
        self.movesSpritesheet = pygame.image.load("ProjetFinalPython/img/PlayerMovementSpritesheet.png")
        self.img = pygame.transform.scale(pygame.image.load('ProjetFinalPython/img/PlayerBaseSprite.png'), (20, 34))
        self.money = 500
        self.pokemons = []
        inventory = Inventory()
        self.inventory = inventory

        #self.runRightAnimation = [self.getImgFromSpritesheet(16, 46, 14, 21, self.movesSpritesheet),self.getImgFromSpritesheet(16, 23, 14, 21, self.movesSpritesheet),self.getImgFromSpritesheet(16, 0, 14, 21, self.movesSpritesheet)]

    #Extraire une image d'une spritesheet.
    def getImgFromSpritesheet(self, x, y, width, height, spriteSheet):
        image = pygame.Surface([width, height])
        image.blit(spriteSheet, (0, 0), (x, y, width, height))
        image.set_colorkey(GREEN)
        image = pygame.transform.scale(image, (20, 34))
        return image

    def initializePlayerInventory(self):
        pokeball = createPokeballFromAPI("poke-ball")
        greatball = createPokeballFromAPI("great-ball")
        ultraball = createPokeballFromAPI("ultra-ball")
        masterball = createPokeballFromAPI("master-ball")
        self.inventory.pokeballs.append(pokeball)
        self.inventory.pokeballs.append(greatball)
        self.inventory.pokeballs.append(ultraball)
        self.inventory.pokeballs.append(masterball)

"""
Class InvisibleObject (used to create invisible walls and objects).
Parameters:
- posX: position on the X axis of the object.
- posY: position on the Y axis of the object.
- width: the width of the object.
- height: the height of the object.
- gameDisplay: the principal window in which will be drawn the object.
"""
class InvisibleObject():
    def __init__(self, posX, posY, width, height, gameDisplay, color):
        self.rectangleSurface = pygame.Surface((width,height))  # Longueur et hauteur de la surface.
        self.rectangleSurface.set_alpha(0)                # Niveau alpha = transparence. | 0 = invisible | 128 = transparent | 255 = rempli.
        self.rectangleSurface.fill(color)         # Rempli la surface avec la couleur donnée en paramètre (format RVB).
        gameDisplay.blit(self.rectangleSurface, (posX,posY))    # Dessine la surface dans la fenêtre du jeu.

        #Données: 1 arbre = 65px longueur / 75px hauteur.

"""
Class Pokemon.
Parameters:
- id: the identifier of the pokemon.
- name: the name of the pokemon.
- baseHp: number of Health Points of the pokemon.
- attacks(array): an array containing the 4 attacks of the pokemon.
- frontSprite: 
"""
class Pokemon():
    def __init__(self, id, name, baseHp, attacks, frontSprite, backSprite):
        self.id = id
        self.name = name
        self.baseHp = baseHp
        self.currentHp = baseHp
        self.attacks = attacks
        self.frontSprite = frontSprite
        self.backSprite = backSprite


"""
Class Attack.
Parameters:
- id: the identifier of the attack.
- name: the name of the attack.
- power: the damages of the attack.
- pp: number of time this attack can be used.
"""
class Attack():
    def __init__(self, id, name, power, pp):
        self.id = id
        self.name = name
        self.power = power
        self.pp = pp

"""
Class Pokeball.
Parameters:
- id: the identifier of the pokeball.
- name: the name of the pokeball (or type).
- description: brief description of the pokeball.
- catchRate: chances of capturing the targeted pokemon.
- nbrInInventory: number of pokeballs of this type in the player inventory.
"""
class Pokeball():
    def __init__(self, id, name, description, catchRate):
        self.id = id
        self.name = name
        self.description = description
        self.catchRate = catchRate
        self.nbrInInventory = 0

"""
Class Inventory.
Properties:
- player: the player this inventory belongs to.
- pokeballs(array): an array containing all the player's pokeball.
"""
class Inventory():
    def __init__(self):
        self.pokeballs = [createPokeballFromAPI('poke-ball'), createPokeballFromAPI('great-ball'), createPokeballFromAPI('ultra-ball'), createPokeballFromAPI('master-ball')]
        #self.pokeballs = [masterBall, ultraBall.......]



def createPokemonFromAPI(chosenPokemonID):
    pokemonResponse = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(chosenPokemonID) + "/")
    pokemonResponseJson  = pokemonResponse.json()

    # Récupère les informations du pokemon.
    pokemonId = pokemonResponseJson['id']
    pokemonName = pokemonResponseJson['name']
    #pokemonHP = pokemonResponseJson['hp'] - [EN COURS] A trouver 


    # Récupère les informations des attaques du pokemon.
    attack1Name = pokemonResponseJson['moves'][0]['move']['name']
    attack1Response = requests.get("https://pokeapi.co/api/v2/move/" + attack1Name + "/")
    attack1ResponseJson  = attack1Response.json()
    attack1Id = attack1ResponseJson['id']
    attack1Power = attack1ResponseJson['power']
    if attack1Power is None: # Si c'est une attaque qui ne fait pas de dégats, je met les dégats à 0 pour ne pas afficher "None" sur l'UI.
        attack1Power = 0
    attack1PP = attack1ResponseJson['pp']

    attack2Name = pokemonResponseJson['moves'][1]['move']['name']
    attack2Response = requests.get("https://pokeapi.co/api/v2/move/" + attack2Name + "/")
    attack2ResponseJson  = attack2Response.json()
    attack2Id = attack2ResponseJson['id']
    attack2Power = attack2ResponseJson['power']
    if attack2Power is None:
        attack2Power = 0
    attack2PP = attack2ResponseJson['pp']

    attack3Name= pokemonResponseJson['moves'][2]['move']['name']
    attack3Response = requests.get("https://pokeapi.co/api/v2/move/" + attack3Name + "/")
    attack3ResponseJson  = attack3Response.json()
    attack3Id = attack3ResponseJson['id']
    attack3Power = attack3ResponseJson['power']
    if attack3Power is None:
        attack3Power = 0
    attack3PP = attack3ResponseJson['pp']

    attack4Name = pokemonResponseJson['moves'][3]['move']['name']
    attack4Response = requests.get("https://pokeapi.co/api/v2/move/" + attack4Name + "/")
    attack4ResponseJson  = attack4Response.json()
    attack4Id = attack4ResponseJson['id']
    attack4Power = attack4ResponseJson['power']
    if attack4Power is None:
        attack4Power = 0
    attack4PP = attack4ResponseJson['pp']


    # Créé les objets d'attaques pour le Pokemon.
    attack1 = Attack(attack1Id, attack1Name, attack1Power, attack1PP)
    attack2 = Attack(attack2Id, attack2Name, attack2Power, attack2PP)
    attack3 = Attack(attack3Id, attack3Name, attack3Power, attack3PP)
    attack4 = Attack(attack4Id, attack4Name, attack4Power, attack4PP)

    # Récupère le sprite du Pokemon vu de face et de dos.
    pokemonSpriteFront = pokemonResponseJson['sprites']['front_default']
    pokemonSpriteBack = pokemonResponseJson['sprites']['back_default']

    # Créé l'objet du Pokemon correspondant et lui ajoute ses attaques correspondantes.
    return Pokemon(pokemonId, pokemonName, 100, [attack1, attack2, attack3, attack4], pokemonSpriteFront, pokemonSpriteBack)

#Paramètre: type de pokéball [poke-ball, great-ball, ultra-ball, master-ball]
def createPokeballFromAPI(pokeballName):
    pokeballResponse = requests.get("https://pokeapi.co/api/v2/item/" + pokeballName + "/")
    pokeballResponseJson  = pokeballResponse.json()
    pokeballId = pokeballResponseJson['id']
    if pokeballName == "poke-ball":
        pokeballDescription = "A device for catching wild Pokémon. It’s thrown like ball at a Pokémon, comfortably encapsulating its target."
        pokeballCatchRate = 30
    elif pokeballName == "great-ball":
        pokeballDescription = "A good, high-performance Poké Ball that provides higher Pokémon catch rate than a standard Poké Ball."
        pokeballCatchRate = 50
    elif pokeballName == "ultra-ball":
        pokeballDescription = "An ultra-high-performance Poké Ball that provides higher success rate for catching Pokémon than Great Ball."
        pokeballCatchRate = 70
    elif pokeballName == "master-ball":
        pokeballDescription = "The best Poké Ball with the ultimate level of performance. With it, you will catch any wild Pokémon without fail."
        pokeballCatchRate = 100
    return Pokeball(pokeballId, pokeballName, pokeballDescription, pokeballCatchRate)