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

def drawTileLine(win, startPosition, endPosition, color=black):
    pygame.draw.aaline(win, color, startPosition, endPosition) 

tilesideLength = 30 # = hypotenuses/tilesides
tileWidth = tilesideLength/2 * 3**(1/2)

def drawTileOutline(win, x, y, color=black):
    #points
    p1 = (x, y - tilesideLength*zoom)
    p2 = (x + tileWidth*zoom, y-tilesideLength*zoom/2)
    p3 = (x + tileWidth*zoom, y+tilesideLength*zoom/2)
    p4 = (x, y + tilesideLength*zoom)
    p5 = (x - tileWidth*zoom, y+tilesideLength*zoom/2)
    p6 = (x - tileWidth*zoom, y-tilesideLength*zoom/2)
    
    drawTileLine(win, p1, p2, color)
    drawTileLine(win, p2, p3, color)
    drawTileLine(win, p3, p4, color)
    drawTileLine(win, p4, p5, color)
    drawTileLine(win, p5, p6, color)
    drawTileLine(win, p6, p1, color)

def drawImgOnTile(win, x, y, img, size=40):
    win.blit(pygame.transform.scale(img, (size*zoom, size*zoom)), (x-size*zoom/2,y-size*zoom/2))

def drawTiles(win, tileList):
    #Goes through tiles and renders them in aproprate coordinate on the screen.
    for y, row in enumerate(tileList):
        for x, tile in enumerate(row):
            coordX, coordY = indexToCoordinates(x, y, offsetX, offsetY, zoom)
            drawTileOutline(win, coordX, coordY)
            if tile != " ":
                img = pygame.image.load(os.path.join("assets", tile.img)).convert_alpha()
                drawImgOnTile(win, coordX, coordY, img)


def indexToCoordinates(x, y, offsetX, offsetY, zoom):
    coordY = 1.5*y*tilesideLength*zoom + offsetY
    coordX = 2*x*tileWidth*zoom + tileWidth*zoom*(y%2) + offsetX
    return (coordX, coordY)

def distanceBetweenPoints(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def coordinatesToIndex(x, y, offsetX, offsetY, zoom):
    #The center that the point is closest to
    currentClosest = None
    ret = (None, None)
    for indexY in range(len(tiles)):
        for indexX in range(len(tiles[0])):
            centerX, centerY = indexToCoordinates(indexX, indexY, offsetX, offsetY, zoom)
            distance = distanceBetweenPoints(x,y,centerX,centerY)
            if currentClosest == None or distance < currentClosest:
                currentClosest = distance
                ret = (indexX, indexY)
    return ret

def closestCenterPoint(x, y, offsetX, offsetY, zoom):
    indexX, indexY = coordinatesToIndex(x, y, offsetX, offsetY, zoom)
    return indexToCoordinates(indexX, indexY, offsetX, offsetY, zoom)

def drawGame(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)
    if selected != None:
        x, y = indexToCoordinates(selected[0], selected[1], offsetX, offsetY, zoom)
        drawTileOutline(win, x, y, tileSelectColor)



def drag(pos):
    global offsetX
    global offsetY

    offsetX += pos[0]*0.5
    offsetY += pos[1]*0.5
    

def changeZoom(direction): 
    global zoom
    zoom += 0.15*direction *zoom
    if zoom < 0.6: zoom = 0.6
    elif zoom > 3: zoom = 3


def rightClick(win, pos):
    global selected
    selected = coordinatesToIndex(pos[0], pos[1], offsetX, offsetY, zoom)
    
    
