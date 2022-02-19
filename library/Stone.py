import pygame
import os

class Stone:
    img = pygame.image.load(os.path.join("assets", "stone.png"))
    movementCost = 2

    def endTurn(self):
        return

    def info(self):
        return "Stone"
