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



