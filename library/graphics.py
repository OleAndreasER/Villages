#!/bin/python3
import pygame
import pygame.gfxdraw
import os
from library.gamelogic import availableTiles, moveCitizen, getSelected, selectTile, actionButton, actionQueue, getTurn, knownBuildings, selectedCitizen, isCitizenSelected, isCitizenOnUnfinishedBuilding
from library.tiles import tiles
from library.UI import UIComponents, UIComponent, textSurface, buildButtonComponents, citizenMenuComponents
from library.settings import width, height, tileSelectColor, white, grassGreen, black
from library.Player import Player, currentPlayer
from library.buildings import House

#TODO: center on player
#Camera
offsetX = 0
offsetY = 0
zoom = 1

worldImgSize = 40
worldTileSideLength = 30
worldTileWidth = worldTileSideLength/2 * 3**(1/2)

hovered = None

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
    for y, row in enumerate(tileList):
        for x, tile in enumerate(row):
            worldX, worldY = indexToCoordinates(x, y)
            screenX, screenY = worldToScreen(worldX, worldY)
            drawTileOutline(win, screenX, screenY)
            for tileType in tile.contents:
                drawImgOnTile(win, screenX, screenY, tileType.img.convert_alpha(), imgSize())

def drawMoves(win, tileIndecies):
    for x, y in tileIndecies:
        screenX, screenY = worldToScreen(*indexToCoordinates(x, y))
        pygame.gfxdraw.aacircle(win, int(screenX), int(screenY), int(7*zoom), tileSelectColor)

def drawWorld(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)

    if getSelected() != None:
        #Draw selected tile
        drawTileOutline(win, *worldToScreen(*indexToCoordinates(*getSelected())), tileSelectColor)
       
        #Available tiles for citizen      
        selectedTile = tiles[getSelected()[1]][getSelected()[0]]
        
        if not selectedTile.containsCitizen(): return
        if selectedTile.getCitizen().actionPoints == 0: return

        drawMoves(win, availableTiles(*getSelected()))

def drawUI(win, x, y):
    #Hovered is for tile info UI
    global hovered
    hovered = worldFuncWithScreen(coordinatesToIndex, x, y)

    #Update UI
    if isCitizenSelected():
        UIComponent("lockButton").setImg(1 if selectedCitizen().isLocked else 0)
        updateBuildButtonPositions()

    #Render UI
    for ui in UIComponents():
        ui.render(win)

def updateBuildButtonPositions():
    for i, building in enumerate(knownBuildings(selectedCitizen())):
        button = UIComponent(building.buildButton)
        if isCitizenOnUnfinishedBuilding(building.buildingStr):
            button.imgRect.topleft = (193, height-421+300)
        else:
            button.imgRect.topleft = (269, height-401+49*i)

def resetToggles():
    for ui in UIComponents():
        ui.isPressed = False

#Input response
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
    for ui in reversed(UIComponents()):
        #Reverse because components render bottom up, while clickable areas should be checked top down.
        if ui.isHidden(): continue

        isClicked = ui.click(*pos)
        if isClicked:
            if not ui.isToggle:
                ui.setImg(1)
            return

    resetToggles()

    selectTile(worldFuncWithScreen(coordinatesToIndex, *pos))

def leftClickRelease(win, pos):
    for ui in UIComponents():
        if not ui.isToggle:
            ui.setImg(0)

def rightClick(win, pos):
    if getSelected() == None: return
    rightClickedTile = worldFuncWithScreen(coordinatesToIndex, *pos)
    moveCitizen(*getSelected(), *rightClickedTile)

#MISC

def hoveredTileInfo():
    if hovered == None: return ""
    hoveredX, hoveredY = hovered
    return tiles[hoveredY][hoveredX].info()

