#!/bin/python3
import pygame
import pygame.gfxdraw
import os
from library.tiles import tiles

width = 1920
height = 1080

#topleft
#TODO: center on player
offsetX = 0
offsetY = 0

zoom = 1

tileSelectColor = (225,229,124)
white = (225,225,225)
grassGreen = (3,160,98)
black = (0,0,0)

#Selected tile's index
selected = None

worldImgSize = 40
worldTileSideLength = 30
worldTileWidth = worldTileSideLength/2 * 3**(1/2)

#Coordinate translation
def imgSize():
    return worldImgSize*zoom

def tileSideLength(): # = hypotenuses/tilesides
    return worldTileSideLength*zoom 

def tileWidth():
    return tileSideLength()/2 * 3**(1/2)

def screenToWorld(x, y):
    return (
        x/zoom + offsetX,
        y/zoom + offsetY)

def worldToScreen(x, y):
    return (
        (x - offsetX)*zoom,
        (y - offsetY)*zoom)

def indexToCoordinates(x, y):
    return (
        2*x*worldTileWidth + (y%2)*worldTileWidth,
        1.5*y*worldTileSideLength)

def coordinatesToIndex(x, y):
    shortestDistance = None
    closestPoint = None
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            worldX, worldY = indexToCoordinates(j, i)
            distance = pointDistance(x, y, worldX, worldY)
            if shortestDistance == None or distance < shortestDistance:
                shortestDistance = distance
                closestPoint = (j, i)

    return closestPoint

def worldFuncWithScreen(func, screenX, screenY):
    return func(*screenToWorld(screenX, screenY))

#Math

def pointDistance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

#Drawing
def drawTileLine(win, startPosition, endPosition, color=black):
    pygame.draw.aaline(win, color, startPosition, endPosition) 

def drawTileOutline(win, x, y, color=black):
    #points
    p1 = (x, y - tileSideLength())
    p2 = (x + tileWidth(), y-tileSideLength()/2)
    p3 = (x + tileWidth(), y+tileSideLength()/2)
    p4 = (x, y + tileSideLength())
    p5 = (x - tileWidth(), y+tileSideLength()/2)
    p6 = (x - tileWidth(), y-tileSideLength()/2)
    
    drawTileLine(win, p1, p2, color)
    drawTileLine(win, p2, p3, color)
    drawTileLine(win, p3, p4, color)
    drawTileLine(win, p4, p5, color)
    drawTileLine(win, p5, p6, color)
    drawTileLine(win, p6, p1, color)

def drawImgOnTile(win, x, y, img, size):
    win.blit(pygame.transform.scale(img, (size, size)), (x-size/2,y-size/2))

def drawTiles(win, tileList):
    #Goes through tiles and renders them in aproprate coordinate on the screen.
    for y, row in enumerate(tileList):
        for x, tile in enumerate(row):
            worldX, worldY = indexToCoordinates(x, y)
            screenX, screenY = worldToScreen(worldX, worldY)
            drawTileOutline(win, screenX, screenY)
            for tileType in tile.tileTypes:
                img = pygame.image.load(os.path.join("assets", tileType.img)).convert_alpha()
                drawImgOnTile(win, screenX, screenY, img, imgSize())

def drawMoves(win, tileIndecies):
    for x, y in tileIndecies:
        screenX, screenY = worldToScreen(*indexToCoordinates(x, y))
        pygame.gfxdraw.aacircle(win, int(screenX), int(screenY), int(7*zoom), tileSelectColor)

def drawGame(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)
    if selected != None:
        drawTileOutline(win, *worldToScreen(*indexToCoordinates(*selected)), tileSelectColor)
        selectedTile = tiles[selected[1]][selected[0]]
        if selectedTile.containsCitizen():
            drawMoves(win, availableTiles(*selected, selectedTile.getCitizenInTile().movementPoints))

#Change camera
def drag(pos):
    global offsetX
    global offsetY

    offsetX -= pos[0]*0.5
    offsetY -= pos[1]*0.5
    

def changeZoom(direction, pos): 
    global offsetX
    global offsetY
    global zoom
    newZoom = zoom + 0.15*direction *zoom
    if newZoom < 0.6: return
    elif newZoom > 3: return
    beforeZoomX, beforeZoomY = screenToWorld(pos[0], pos[1])
    zoom = newZoom
    afterZoomX, afterZoomY = screenToWorld(pos[0], pos[1])
    offsetX += beforeZoomX - afterZoomX
    offsetY += beforeZoomY - afterZoomY

def leftClick(win, pos):
    selectTile(*pos)

def rightClick(win, pos):
    if selected == None: return

    selectedTile = tiles[selected[1]][selected[0]]
    rightClickedTile = worldFuncWithScreen(coordinatesToIndex, *pos)
    citizen = selectedTile.getCitizenInTile()
    if citizen == None: return

    if rightClickedTile in availableTiles(*selected, citizen.movementPoints):
        moveCitizen(selectedTile.popCitizenInTile(), *rightClickedTile)

def selectTile(x, y): #screen coordinates
    global selected
    selected = worldFuncWithScreen(coordinatesToIndex, x, y)

#To be moved

def availableTiles(x, y, movementPoints):
    return [(x + offsetX, y + offsetY)
           for offsetX, offsetY in [(-1, 0), (1,0), ((y%2),1), ((y%2)-1, 1), ((y%2),-1), ((y%2)-1, -1)]
           if (
               tiles[y + offsetY][x + offsetX].totalTileCost() != None and
               tiles[y + offsetY][x + offsetX].totalTileCost() <= movementPoints
           )]

def moveCitizen(citizen, x, y):
    citizen.useMovementPoints(tiles[y][x].totalTileCost())
    tiles[y][x].tileTypes.append(citizen)
    selectTile(x, y)



