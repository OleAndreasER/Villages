import pygame
import os
from library.gamelogic import actionButton

width = 1920
height = 1080

eggWhite = (239,234,231)

class UI:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(os.path.join("assets", img)).convert_alpha()
        self.imgRect = self.img.get_rect(topleft = (x, y))

    clickableRects = []

    def addClickableRect(self, rect, func):
        self.clickableRects.append((rect, func))
        
    textSurfaces = []

    def addText(self, text, fontSize, x, y):
        font = pygame.font.SysFont("verdana", fontSize)
        textSurface = font.render(text, True, eggWhite)

        self.textSurfaces.append((textSurface, (x, y)))

    def render(self, win):
        win.blit(self.img, self.imgRect)
        for textSurface, pos in self.textSurfaces:
            win.blit(textSurface, pos)

    def click(self, x, y):
        for rect, func in self.clickableRects:
            print(rect, func)
            if rect.collidepoint((x, y)):
                func()
                return True
        return False
    


def getActionButton():
    actionButtonUI = UI("actionbtn.png", width-350, height-150)
    actionButtonUI.addClickableRect(actionButtonUI.imgRect, actionButton)
    actionButtonUI.addText("Next Turn", 50, width-320, height-138)
    return actionButtonUI

uiComponents = []

def makeUIComponents():
    global uiComponents
    uiComponents.append(getActionButton())

