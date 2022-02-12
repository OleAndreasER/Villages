#!/bin/python3
import pygame
import os
from library.tiles import tiles

width = 1920
height = 1080

centerX = width/2
centerY = height/2

zoom = 1

white = (225,225,225)
grassGreen = (3,160,98)

def drawTileLine(win, startPosition, endPosition):
    black = (0,0,0)
    pygame.draw.aaline(win, black, startPosition, endPosition) 

tilesideLength = 30 # = hypotenuses/tilesides
tileWidth = tilesideLength/2 * 3**(1/2)

def drawTileOutline(win, x, y):
    #points
    p1 = (x, y - tilesideLength*zoom)
    p2 = (x + tileWidth*zoom, y-tilesideLength*zoom/2)
    p3 = (x + tileWidth*zoom, y+tilesideLength*zoom/2)
    p4 = (x, y + tilesideLength*zoom)
    p5 = (x - tileWidth*zoom, y+tilesideLength*zoom/2)
    p6 = (x - tileWidth*zoom, y-tilesideLength*zoom/2)
    
    drawTileLine(win, p1, p2)
    drawTileLine(win, p2, p3)
    drawTileLine(win, p3, p4)
    drawTileLine(win, p4, p5)
    drawTileLine(win, p5, p6)
    drawTileLine(win, p6, p1)

def drawImgOnTile(win, x, y, img, size=40):
    win.blit(pygame.transform.scale(img, (size*zoom, size*zoom)), (x-size*zoom/2,y-size*zoom/2))

def drawTiles(win, tileList):
    #Goes through tiles and renders them in aproprate coordinate on the screen.
    for y, row in enumerate(tileList):
        for x, tile in enumerate(row):
            coordX, coordY = indexToCoordinates(x, y, tileList, centerX, centerY, zoom)
            drawTileOutline(win, coordX, coordY)
            if tile != " ":
                img = pygame.image.load(os.path.join("assets", tile.img)).convert_alpha()
                drawImgOnTile(win, coordX, coordY, img)


def indexToCoordinates(x, y, tileList, centerX, centerY, zoom):
    startX = centerX - 2*tileWidth*zoom*(len(tileList[0])/2)
    startY = centerY - 1.5*tilesideLength*zoom*(len(tileList)/2)

    coordX = startX + 2*x*tileWidth*zoom + tileWidth*zoom*(y%2)
    coordY = startY + 1.5*y*tilesideLength*zoom
    return (coordX, coordY)


def drawGame(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)





def drag(pos):
    global centerX
    global centerY
    centerX += pos[0] *0.5
    centerY += pos[1] *0.5

def changeZoom(direction): 
    global zoom
    zoom += 0.15*direction *zoom
    if zoom < 0.6: zoom = 0.6
    elif zoom > 3: zoom = 3


