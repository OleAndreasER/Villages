from library.Citizen import Citizen

class Tile:
    def __init__(self, *tileTypes):
        self.tileTypes = list(tileTypes)

    def totalTileCost(self):
        costs = [tile.movementCost for tile in self.tileTypes] + [1]
        return None if None in costs else sum(costs)

    def containsCitizen(self):
        return any(isinstance(tileType, Citizen) for tileType in self.tileTypes)

    def containsNonCitizen(self):
        return any(not isinstance(tileType, Citizen) for tileType in self.tileTypes)

    def getCitizenInTile(self):
        if not self.containsCitizen(): return None
        for tileType in self.tileTypes:
            if isinstance(tileType, Citizen):
                return tileType

    def getNonCitizen(self):
        if not self.containsNonCitizen(): return None
        for tileType in self.tileTypes:
            if not isinstance(tileType, Citizen):
                return tileType

    def popCitizenInTile(self):
        if not self.containsCitizen(): return None
        citizen = self.getCitizenInTile()
        self.tileTypes = [tileType for tileType in self.tileTypes if not isinstance(tileType, Citizen)]
        return citizen

    def endTurn(self):
        for tileType in self.tileTypes:
            tileType.endTurn()

    def spawnCitizen(self):
        self.tileTypes.append(Citizen())

    def info(self):
        tile = [tileType for tileType in self.tileTypes if not isinstance(tileType, Citizen)]
        if len(tile) == 0: return ""
        return tile[0].info()



    
