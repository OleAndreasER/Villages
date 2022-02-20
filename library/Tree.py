import pygame
import os


class Tree:
    img = pygame.image.load(os.path.join("assets", "tree.png"))
    movementCost = 1
    woodLeft = 4

    def endTurn(self):
        return

    def info(self):
        return "Tree"
    
    def getChopped(self, amount):
        if self.woodLeft > 0:
            self.woodLeft -= amount
        else:
            from library.gamelogic import removeFromTiles
            removeFromTiles(self)
