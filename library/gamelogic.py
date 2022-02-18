from library.tiles import tiles

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

def actionButton():
    if len(actionQueue()) == 0:
        endTurn()
    else:
        selectTile(*actionQueue()[0])

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

