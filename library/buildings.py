import pygame
import os

class House:
    houseImg = pygame.image.load(os.path.join("assets", "house.png")) 
    buildSiteImg = pygame.image.load(os.path.join("assets", "buildingsite.png"))
    img = buildSiteImg
    movementCost = 0
    actionText = None
    buildButton = "houseButton"
    buildingStr = "house"
    citizenIsSpawned = False
    buildPointsLeft = 5
    isBuilt = False
    cost = {"wood":10} 
    
    def endTurn(self):
        from library.gamelogic import isCitizenInTileOfTileType
        if (self.isBuilt
            and not self.citizenIsSpawned
            and not isCitizenInTileOfTileType(self)):
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
        self.isBuilt = True

class SawMill:
    img = pygame.image.load(os.path.join("assets", "sawmill.png"))
    movementCost = 0
    actionText = None
    buildButton = "sawMillButton"
    isBuilt = True
    buildingStr = "sawMill"

    def endTurn(self):
        return

    def info(self):
        return "Lumber mill"

