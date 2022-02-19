import pygame
import os

class Citizen:
    img = pygame.image.load(os.path.join("assets", "citizen.png"))

    movementCost = None #impassable
    movementPoints = 1
    movement = 1

    hp = 20
    totalHp = 20

    isIdle = False

    def useMovementPoints(self, points):
        self.movementPoints -= points
        if self.movementPoints < 0:
            self.movementPoints = 0

    def resetMovementPoints(self):
        self.movementPoints = self.movement

    def endTurn(self):
        self.resetMovementPoints()

    def isInQueue(self):
        return self.movementPoints > 0 and not self.isIdle

