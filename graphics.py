#!/bin/python3
import pygame
from tiles import tiles

width = 1920-20
height = 1080-20

white = (225,225,225)
grassGreen = (3,160,98)

def drawTileLine(win, startPosition, endPosition):
    black = (0,0,0)
    pygame.draw.line(win, black, startPosition, endPosition, 2) 

tilesideLength = 20 # = hypotenuses/tilesides
tileWidth = tilesideLength/2 * 3**(1/2)

def drawTileOutline(win, x, y):
    #points
    p1 = (x, y - tilesideLength)
    p2 = (x + tileWidth, y-tilesideLength/2)
    p3 = (x + tileWidth, y+tilesideLength/2)
    p4 = (x, y + tilesideLength)
    p5 = (x - tileWidth, y+tilesideLength/2)
    p6 = (x - tileWidth, y-tilesideLength/2)
    
    drawTileLine(win, p1, p2)
    drawTileLine(win, p2, p3)
    drawTileLine(win, p3, p4)
    drawTileLine(win, p4, p5)
    drawTileLine(win, p5, p6)
    drawTileLine(win, p6, p1)

def drawTiles(win, tileList):
    startY = height/2 - 2*tilesideLength*(len(tileList)/2)
    startX = width/2 - 2*tileWidth*(len(tileList[0])/2)
    for y, row in enumerate(tileList):
        for x, tile in enumerate(row):
            drawTileOutline(win,
                startX + 2*x*tileWidth + tileWidth*(y%2),
                startY + 1.5*y*tilesideLength)

def drawGame(win):
    win.fill(grassGreen) 
    drawTiles(win, tiles)

