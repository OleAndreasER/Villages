from library.Citizen import Citizen

class Tile:
    def __init__(self, *contents):
        self.contents = list(contents) 
        # Tile has contents (Citizen and/or tileType)

    def totalTileCost(self):
        costs = [content.movementCost for content in self.contents] + [1]
        return None if None in costs else sum(costs)

    def containsCitizen(self):
        return any(isinstance(tileType, Citizen) for tileType in self.contents)

    def containsTileType(self):
        return any(not isinstance(tileType, Citizen) for tileType in self.contents)

    def containsSpecificTileType(self, tileType):
        return any(isinstance(content, tileType) for content in self.contents)

    def getCitizen(self):
        if not self.containsCitizen(): return None
        for content in self.contents:
            if isinstance(content, Citizen):
                return content

    def getTileType(self):
        if not self.containsTileType(): return None
        for content in self.contents:
            if not isinstance(content, Citizen):
                return content

    def popCitizenInTile(self):
        if not self.containsCitizen(): return None
        citizen = self.getCitizen()
        self.contents = [tileType for tileType in self.contents if not isinstance(tileType, Citizen)]
        return citizen

    def endTurn(self):
        for tileType in self.contents:
            tileType.endTurn()

    def spawnCitizen(self):
        self.contents.append(Citizen())

    def info(self):
        if not self.containsTileType(): return ""
        return self.getTileType().info()



    
