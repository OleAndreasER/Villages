import pygame
import os
from library.Player import currentPlayer
from library.resourcetiles import Tree, Stone
from library.buildings import House

class Citizen:
    img = pygame.image.load(os.path.join("assets", "citizen.png"))

    acitionPointCost = None #impassable
    actionPoints = 1
    totalActionPoints = 1
    owner = currentPlayer
    knownTechnologies = ["mining", "replanting", "house", "sawMill"]

    def useActionPoints(self, points):
        self.actionPoints -= points
        if self.actionPoints < 0:
            self.actionPoints = 0

    def resetActionPoints(self):
        self.actionPoints = self.totalActionPoints
    
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
            and self.actionPoints > 0
            and self.latestAction != None):
            self.latestAction["action"](*self.latestAction["args"])

        self.resetActionPoints()

    def isInQueue(self):
        return self.actionPoints > 0 and not self.isIdle and not self.isLocked

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

        self.useActionPoints(10)

    def mine(self, stone):
        resource = stone.getResourceType()
        if resource == "stone":
            self.owner.stone += 1
        self.useActionPoints(10)

    def buildHouse(self, tile):
        if tile.containsSpecificTileType(House):
            house = tile.getTileType()
            house.build() 
            self.useActionPoints(10)
            if house.isBuilt: 
                self.wakeUp()
        elif House.cost["wood"] <= self.owner.wood:
            tile.contents.insert(0, House())
            self.owner.wood -= House.cost["wood"]

