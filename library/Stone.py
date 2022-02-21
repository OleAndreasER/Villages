import pygame
import os

class Stone:
    img = pygame.image.load(os.path.join("assets", "stone.png"))
    movementCost = 2
    actionText = "Mine stone"

    def endTurn(self):
        return

    def info(self):
        return "Stone"

    def getResourceType(self):
        return "stone" #Could be coal, iron etc later on



