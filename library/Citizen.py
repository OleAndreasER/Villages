class Citizen:
    img = "citizen.png"
    movementCost = None
    movementPoints = 1
    movement = 1

    def useMovementPoints(self, points):
        self.movementPoints -= points
        if self.movementPoints < 0:
            self.movementPoints = 0

    def resetMovementPoints(self):
        self.movementPoints = self.movement

    def endTurn(self):
        self.resetMovementPoints()


