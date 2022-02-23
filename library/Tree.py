import pygame
import os


class Tree:

    treeImg = pygame.image.load(os.path.join("assets", "tree.png"))
    sapling1Img = pygame.image.load(os.path.join("assets", "sapling1.png")) 
    sapling2Img = pygame.image.load(os.path.join("assets", "sapling2.png")) 
    sapling3Img = pygame.image.load(os.path.join("assets", "sapling3.png")) 
    img = treeImg
    movementCost = 1
    woodLeft = 4
    actionText = "Chop wood"
    turnsUntilTree = 0

    def endTurn(self):
        if self.turnsUntilTree > 1:
            self.turnsUntilTree -= 1
            if self.turnsUntilTree == 20:
                self.img = self.sapling2Img
            elif self.turnsUntilTree == 10: 
                self.img = self.sapling3Img
            elif self.turnsUntilTree == 0:
                self.becomeTree()

    def info(self):
        return "Tree"

    def becomeSapling(self):
        self.img = self.sapling1Img
        self.actionText = None
        self.turnsUntilTree = 30

    def becomeTree(self):
        self.img = self.treeImg
        self.woodLeft = 4
        self.actionText = "Chop wood"
    
    def getChopped(self, amount, knowsReplanting):
        if self.woodLeft > 0:
            wood = min(amount, self.woodLeft)
            self.woodLeft -= wood
            return wood
        elif knowsReplanting:
            self.becomeSapling()
        else:
            from library.gamelogic import removeFromTiles
            removeFromTiles(self)
        return 0
