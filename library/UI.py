import pygame
import os
from library.gamelogic import actionButton

width = 1920
height = 1080

eggWhite = (239,234,231)

class UI:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(os.path.join("assets", img)).convert_alpha()
        self.imgVersions = [self.img]
        self.imgRect = self.img.get_rect(topleft = (x, y))

    clickableRects = []

    def addClickableRect(self, rect, func):
        self.clickableRects.append((rect, func))
        
    textSurfaces = []

    def addText(self, textSurface, x, y):
        self.textSurfaces.append((textSurface, (x, y)))

    def addImg(self, imgPath):
        self.imgVersions.append(pygame.image.load(os.path.join("assets", imgPath)).convert_alpha())

    def switchImg(self, i):
        self.img = self.imgVersions[i]

    def setText(self, i, textSurface, x, y):
        self.textSurfaces[i] = (textSurface, (x, y))

    def render(self, win):
        win.blit(self.img, self.imgRect)
        for textSurface, pos in self.textSurfaces:
            win.blit(textSurface, pos)

    def click(self, x, y):
        for rect, func in self.clickableRects:
            if rect.collidepoint((x, y)):
                func()
                return True
        return False

def textSurface(text, fontSize):
    font = pygame.font.SysFont("verdana", fontSize)
    return font.render(text, True, eggWhite)

def getActionButton():
    actionButtonUI = UI("actionbtn.png", width-350, height-150)
    actionButtonUI.addClickableRect(actionButtonUI.imgRect, actionButton)
    actionButtonUI.addImg("actionbtnpressed.png")
    actionButtonUI.addText(textSurface("Next Turn", 50), width-320, height-138)
    actionButtonUI.addText(textSurface("Turn ", 20), width-320, height-60)
    return actionButtonUI

uiComponents = {}

def makeUIComponents():
    global uiComponents
    uiComponents = {
        "actionButton": getActionButton()
    }

def getUIComponents():
    return uiComponents
