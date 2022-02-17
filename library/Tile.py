
class Tile:
    def __init__(self, *tileTypes):
        self.tileTypes = tileTypes

    def totalTileCost(self):
        costs = [tile.movementCost for tile in self.tileTypes] + [1]
        return None if None in costs else sum(costs)

    
