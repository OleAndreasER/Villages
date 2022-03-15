import pygame
import os
from library.Player import currentPlayer
from library.resourcetiles import Tree, Stone
from library.buildings import House

class Citizen:
    img = pygame.image.load(os.path.join("assets", "citizen.png"))

    movementCost = None #impassable
    movementPoints = 1
    movement = 1
    owner = currentPlayer
    knownTechnologies = ["mining", "replanting", "house", "sawMill"]

    def useMovementPoints(self, points):
        self.movementPoints -= points
        if self.movementPoints < 0:
            self.movementPoints = 0

    def resetMovementPoints(self):
        self.movementPoints = self.movement
    
    hp = 20
    totalHp = 20

    hungerPoints = 30

    latestAction = None #{method, (args)}
    isLocked = False

    def toggleLock(self):
        self.isLocked = not self.isLocked

    def wakeUp(self):
        self.latestAction = None
        self.isLocked = False

    def hungerStatus(self):
        if self.hungerPoints > 20: return "Satiated"
        if self.hungerPoints > 10: return "Hungry"
        return "Starving"

    def increaseHunger(self):
        self.hungerPoints -= 1

    isIdle = False

    def endTurn(self):
        self.increaseHunger()
        self.isIdle = False

        if (self.isLocked
            and self.movementPoints > 0
            and self.latestAction != None):
            self.latestAction["action"](*self.latestAction["args"])

        self.resetMovementPoints()

    def isInQueue(self):
        return self.movementPoints > 0 and not self.isIdle and not self.isLocked

    def actOnTile(self, tileType):
        if isinstance(tileType, Tree):
            self.chopWood(tileType)
        if isinstance(tileType, Stone) and "mining" in self.knownTechnologies:
            self.mine(tileType)

    def chopWood(self, tree):
        wood = tree.getChopped(1, "replanting" in self.knownTechnologies)
        self.owner.wood += wood

        if tree.woodLeft == 0:
            self.wakeUp()
            return

        self.useMovementPoints(10)

    def mine(self, stone):
        resource = stone.getResourceType()
        if resource == "stone":
            self.owner.stone += 1
        self.useMovementPoints(10)

    def buildHouse(self, tile):
        if any(isinstance(tileType, House) for tileType in tile.tileTypes):
            house = tile.getNonCitizen()
            house.build() 
            self.useMovementPoints(10)
            if house.isBuilt: 
                self.wakeUp()
        elif House.cost["wood"] <= self.owner.wood:
            tile.tileTypes.insert(0, House())
            self.owner.wood -= House.cost["wood"]

