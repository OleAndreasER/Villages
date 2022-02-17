from library.tiles import tiles

#Selected tile's index
selected = None

def getSelected():
    return selected

def selectTile(x, y): #screen coordinates
    global selected
    selected = (x, y) 

def availableTiles(x, y):
    return [(x + offsetX, y + offsetY)
           for offsetX, offsetY in [(-1, 0), (1,0), ((y%2),1), ((y%2)-1, 1), ((y%2),-1), ((y%2)-1, -1)]
           if tiles[y + offsetY][x + offsetX].totalTileCost() != None]

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
