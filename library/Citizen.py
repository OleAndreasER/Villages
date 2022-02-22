import pygame
import os
from library.Player import currentPlayer
from library.Tree import Tree
from library.Stone import Stone

class Citizen:
    img = pygame.image.load(os.path.join("assets", "citizen.png"))

    movementCost = None #impassable
    movementPoints = 1
    movement = 1
    owner = currentPlayer
    knownTechnologies = ["mining", "replanting"]

    def useMovementPoints(self, points):
        self.movementPoints -= points
        if self.movementPoints < 0:
            self.movementPoints = 0

    def resetMovementPoints(self):
        self.movementPoints = self.movement
    
    hp = 20
    totalHp = 20

    hungerPoints = 30

    def hungerStatus(self):
        if self.hungerPoints > 20: return "Satiated"
        if self.hungerPoints > 10: return "Hungry"
        return "Starving"

    def increaseHunger(self):
        self.hungerPoints -= 1

    isIdle = False

    def endTurn(self):
        self.resetMovementPoints()
        self.increaseHunger()
        self.isIdle = False

    def isInQueue(self):
        return self.movementPoints > 0 and not self.isIdle

    def actOnTile(self, tile):
        if isinstance(tile, Tree):
            self.chopWood(tile)
        if isinstance(tile, Stone) and "mining" in self.knownTechnologies:
            self.mine(tile)

    def chopWood(self, tree):
        tree.getChopped(1, "replanting" in self.knownTechnologies)
        self.owner.wood += 1
        self.useMovementPoints(10)

    def mine(self, stone):
        resource = stone.getResourceType()
        if resource == "stone":
            self.owner.stone += 1
        self.useMovementPoints(10)

