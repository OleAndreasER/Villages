import pygame
import os

class Tree:
    img = pygame.image.load(os.path.join("assets", "tree.png"))
    movementCost = 1

    def endTurn(self):
        return
