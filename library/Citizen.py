class Citizen:
    img = "citizen.png"
    movementCost = None
    movementPoints = 2

    def useMovementPoints(self, points):
        self.movementPoints -= points
        if self.movementPoints < 0:
            self.movementPoints = 0


