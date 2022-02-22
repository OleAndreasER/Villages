import pygame
import os


class Tree:
    #todo
    saplingImg = pygame.image.load(os.path.join("assets", "stone.png")) 
    treeImg = pygame.image.load(os.path.join("assets", "tree.png"))
    img = treeImg
    movementCost = 1
    woodLeft = 4
    actionText = "Chop wood"
    turnsUntilTree = 0

    def endTurn(self):
        if self.turnsUntilTree > 1:
            self.turnsUntilTree -= 1
            if self.turnsUntilTree == 0:
                self.becomeTree()

    def info(self):
        return "Tree"

    def becomeSapling(self):
        self.img = self.saplingImg
        actionText = None
        turnsUntilTree = 35

    def becomeTree(self):
        self.img = self.treeImg
        woodLeft = 4
        actionText = "Chop wood"
    
    def getChopped(self, amount, knowsReplanting):
        if self.woodLeft > 0:
            self.woodLeft -= amount
        elif knowsReplanting:
            self.becomeSapling()
        else:
            from library.gamelogic import removeFromTiles
            removeFromTiles(self)
