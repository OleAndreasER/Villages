import pygame
import os

class House:
    houseImg = pygame.image.load(os.path.join("assets", "house.png")) 
    buildSiteImg = pygame.image.load(os.path.join("assets", "buildingsite.png"))
    img = buildSiteImg
    movementCost = 0
    actionText = None
    buildButton = "houseButton"
    citizenIsSpawned = False
    buildPointsLeft = 5
    isBuilt = False
    cost = {"wood":10} 
    
    def endTurn(self):
        if self.isBuilt and not self.citizenIsSpawned:
            from library.gamelogic import spawnCitizen
            spawnCitizen(self)
            self.citizenIsSpawned = True

    def isOccupied(self):
        return 

    def info(self):
        return "House"

    def build(self):
        self.buildPointsLeft -= 1
        if self.buildPointsLeft == 0:
            self.finish()

    def finish(self):
        self.img = self.houseImg
        isBuilt = True

class SawMill:
    img = pygame.image.load(os.path.join("assets", "sawmill.png"))
    movementCost = 0
    actionText = None
    buildButton = "sawMillButton"

    def endTurn(self):
        return

    def info(self):
        return "Lumber mill"

