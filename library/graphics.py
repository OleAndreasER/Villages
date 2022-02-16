#!/bin/python3
import pygame
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
            if tile != " ":
                img = pygame.image.load(os.path.join("assets", tile.img)).convert_alpha()
                drawImgOnTile(win, screenX, screenY, img, imgSize())

def drawGame(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)

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

def rightClick(win, pos):
    global selected

    
