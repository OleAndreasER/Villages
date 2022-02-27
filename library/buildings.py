import pygame
import os

class House:
    img = pygame.image.load(os.path.join("assets", "house.png"))
    movementCost = 0
    actionText = None

    def endTurn(self):
        return

    def info(self):
        return "House"

class SawMill:
    img = pygame.image.load(os.path.join("assets", "sawmill.png"))
    movementCost = 0
    actionText = None

    def endTurn(self):
        return

    def info(self):
        return "Lumber mill"

