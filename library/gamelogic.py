from library.tiles import tiles
from library.buildings import House, SawMill

#Selected tile's index
selected = None
turn = 1

def getTurn():
    return turn

def getSelected():
    return selected

def selectTile(x, y):
    global selected
    selected = (x, y) 

def isCitizenSelected():
    if selected == None: return False
    if not tiles[selected[1]][selected[0]].containsCitizen(): return False
    return True

def isNonCitizenSelected():
    if selected == None: return False
    if not tiles[selected[1]][selected[0]].containsNonCitizen(): return False
    return True

def availableTiles(x, y):
    return [(x + offsetX, y + offsetY)
           for offsetX, offsetY in [(-1, 0), (1,0), ((y%2),1), ((y%2)-1, 1), ((y%2),-1), ((y%2)-1, -1)]
           if tiles[y + offsetY][x + offsetX].totalTileCost() != None]

def selectedCitizen():
    if selected == None: return None
    x, y = selected
    selectedTile = tiles[y][x]
    return selectedTile.getCitizenInTile()

def selectedTileType():
    if selected == None: return None
    x, y = selected
    selectedTile = tiles[y][x]
    return selectedTile.getNonCitizen()

def moveCitizen(x, y, toX, toY):
    selectedTile = tiles[y][x]

    citizen = selectedTile.getCitizenInTile()
    
    if citizen == None: return
    if citizen.movementPoints == 0: return
    if not (toX, toY) in availableTiles(x, y): return

    selectedTile.popCitizenInTile()

    citizen.useMovementPoints(tiles[toY][toX].totalTileCost())

    tiles[toY][toX].tileTypes.append(citizen)

    selectTile(toX, toY)

def nextSelection():
    return None if len(actionQueue()) == 0 else actionQueue()[0]


#Actions tied to keybinds/mouse clicks
def actionButton():
    if len(actionQueue()) == 0:
        endTurn()
    else:
        selectTile(*actionQueue()[0])

def idle():
    global selected
    if not isCitizenSelected(): return
    citizen = tiles[selected[1]][selected[0]].getCitizenInTile()
    citizen.isIdle = True
    selected = nextSelection()

def endTurn():
    global turn
    turn += 1
    for row in tiles:
        for tile in row:
            tile.endTurn()

def actionQueue():
    return [(x,y)
            for x in range(len(tiles[0]))
            for y in range(len(tiles))
            if tiles[y][x].containsCitizen()
            if tiles[y][x].getCitizenInTile().isInQueue()]

def selectedCitizenAction():
    global selected
    if not isCitizenSelected(): return
    tile = tiles[selected[1]][selected[0]]
    if (not tile.containsCitizen()
        or not tile.containsNonCitizen()
        or tile.getCitizenInTile().movementPoints == 0):
        return
    if (tile.getNonCitizen().actionText == None): return

    citizenAction(tile.getCitizenInTile(), tile)
    selected = nextSelection()

def lockAction():
    if not isCitizenSelected(): return
    citizen = tiles[selected[1]][selected[0]].getCitizenInTile()
    citizen.toggleLock()

def buildHouse():
    if not isCitizenSelected(): return
    tile = tiles[selected[1]][selected[0]]
    citizen = tile.getCitizenInTile()
    tile.buildHouse(citizen)
    

def buildSawMill():
    return

#

def removeFromTiles(targetTileType):
    for row in tiles:
        for tile in row:
            tile.tileTypes = [tileType
                              for tileType in tile.tileTypes
                              if not tileType is targetTileType]

def tileContainingTileType(targetTileType):
    for row in tiles:
        for tile in row:
            if any(tileType is targetTileType for tileType in tile.tileTypes):
                return tile
    return None

def citizenAction(citizen, tile):
    citizen.latestAction = {"action": citizenAction, "args": (citizen, tile)}
    citizen.actOnTile(tile.getNonCitizen())

techToBuilding = {
    "house": House,
    "sawMill": SawMill
}

def knownBuildings(citizen):
    return [techToBuilding[tech]
            for tech in citizen.knownTechnologies
            if tech in techToBuilding.keys()]

def spawnCitizen(house):
    tileContainingTileType(house).spawnCitizen()

#Text elements
def actionButtonText():
    return "Next Turn" if len(actionQueue()) == 0 else "Next Citizen"

def actionPointTxt():
    citizen = selectedCitizen()
    return f"Action points: {citizen.movementPoints}/{citizen.movement}"

def healthPointTxt():
    citizen = selectedCitizen()
    return f"Health points: {citizen.hp}/{citizen.totalHp}"

def hungerStatusTxt():
    citizen = selectedCitizen()
    return f"Hunger status: {citizen.hungerPoints} ({citizen.hungerStatus()})"

def citizenActionButtonTxt():
    return selectedTileType().actionText


