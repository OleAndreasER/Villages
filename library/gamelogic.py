from library.tiles import tiles
from library.buildings import House, SawMill

#Turn
turn = 1
def getTurn():
    return turn

#Selected
selected = None #selected tile index
def getSelected():
    return selected

def selectedTile():
    if selected == None: return None
    x, y = selected
    return tiles[y][x]

def selectTile(newSelection):
    global selected
    selected = newSelection

def isCitizenSelected():
    if selected == None: return False
    if not selectedTile().containsCitizen(): return False
    return True

def selectedCitizen():
    if selected == None: return None
    return selectedTile().getCitizen()

def selectedTileType():
    if selected == None: return None
    return selectedTile().getTileType()

def isTileTypeSelected():
    if selected == None: return False
    if not selectedTile().containsTileType(): return False
    return True

def nextSelection():
    return None if len(actionQueue()) == 0 else actionQueue()[0]

#Citizen movement
def availableTiles(x, y): #Available for citizen to move to
    return [(x + offsetX, y + offsetY)
           for offsetX, offsetY in [(-1, 0), (1,0), ((y%2),1), ((y%2)-1, 1), ((y%2),-1), ((y%2)-1, -1)]
           if tiles[y + offsetY][x + offsetX].totalTileCost() != None]

def moveCitizen(x, y, toX, toY):
    selectedTile = tiles[y][x]
    citizen = selectedTile.getCitizen()
    
    if citizen == None: return
    if citizen.actionPoints == 0: return
    if not (toX, toY) in availableTiles(x, y): return

    selectedTile.popCitizenInTile()
    citizen.useActionPoints(tiles[toY][toX].totalTileCost())
    tiles[toY][toX].contents.append(citizen)
    selectTile((toX, toY))

#Actions tied to keybinds/mouse clicks
def actionButton(): #Next turn/Next citizen
    if len(actionQueue()) == 0:
        endTurn()
    else:
        selectTile(actionQueue()[0])

def idle():
    global selected
    if not isCitizenSelected(): return
    selectedCitizen().isIdle = True
    selectTile(nextSelection())

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
            if tiles[y][x].getCitizen().isInQueue()]

def selectedCitizenAction():
    global selected
    if not isCitizenSelected(): return
    tile = tiles[selected[1]][selected[0]]
    if (not tile.containsCitizen()
        or not tile.containsTileType()
        or tile.getCitizen().actionPoints == 0):
        return
    if (tile.getTileType().actionText == None): return

    citizenAction(tile.getCitizen(), tile)
    selected = nextSelection()

def lockAction():
    if not isCitizenSelected(): return
    citizen = tiles[selected[1]][selected[0]].getCitizen()
    citizen.toggleLock()

def buildHouse():
    if not isCitizenSelected(): return
    selectedCitizen().latestAction = {"action": selectedCitizen().buildHouse, "args": [selectedTile()]}
    selectedCitizen().buildHouse(selectedTile())

def buildSawMill():
    return

#Text elements
def actionButtonText():
    return "Next Turn" if len(actionQueue()) == 0 else "Next Citizen"

def actionPointTxt():
    citizen = selectedCitizen()
    return f"Action points: {citizen.actionPoints}/{citizen.totalActionPoints}"

def healthPointTxt():
    citizen = selectedCitizen()
    return f"Health points: {citizen.hp}/{citizen.totalHp}"

def hungerStatusTxt():
    citizen = selectedCitizen()
    return f"Hunger status: {citizen.hungerPoints} ({citizen.hungerStatus()})"

def citizenActionButtonTxt():
    return selectedTileType().actionText

#UI visibility
def isCitizenMenuHidden():
    return not isCitizenSelected()

def isCitizenActionButtonHidden():
    return (isCitizenMenuHidden()
            or not isTileTypeSelected()
            or selectedTileType().actionText == None)

def isBuildMenuButtonHidden():
    return (isCitizenMenuHidden()
            or isTileTypeSelected())

def isBuildingKnown(buildingStr):
    return buildingStr in selectedCitizen().knownTechnologies

def isCitizenOnUnfinishedBuilding(buildingStr):
    return (isCitizenSelected()
            and isinstance(selectedTileType(), techToBuilding[buildingStr])
            and not selectedTileType().isBuilt)

#

def removeFromTiles(targetTileType):
    for row in tiles:
        for tile in row:
            tile.contents = [tileType
                              for tileType in tile.contents
                              if not tileType is targetTileType]

def tileContainingTileType(targetTileType):
    for row in tiles:
        for tile in row:
            if any(tileType is targetTileType for tileType in tile.contents):
                return tile
    return None

def isCitizenInTileOfTileType(tileType):
    return tileContainingTileType(tileType).containsCitizen()

def citizenAction(citizen, tile):
    citizen.latestAction = {"action": citizenAction, "args": (citizen, tile)}
    citizen.actOnTile(tile.getTileType())

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
