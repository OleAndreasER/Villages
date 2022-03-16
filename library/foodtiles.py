import pygame
import os

class BlueberryBush:
    img = pygame.image.load(os.path.join("assets", "blueberrybush.png"))
    movementCost = 1
    actionText = "Eat blueberries"
    saturation = 15

    def endTurn(self):
        return

    def info(self):
        return "Blueberries"

    def getEaten(self):
        from library.gamelogic import removeFromTiles
        removeFromTiles(self)

