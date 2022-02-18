import pygame
import os
from library.gamelogic import actionButton

width = 1920
height = 1080

class UI:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(os.path.join("assets", img)).convert_alpha()
        self.imgRect = self.img.get_rect(topleft = (x, y))

    clickableRects = []

    def addClickableRect(self, rect, func):
        self.clickableRects.append((rect, func))
        
    def render(self, win):
        win.blit(self.img, self.imgRect)

    def click(self, x, y):
        for rect, func in self.clickableRects:
            print(rect, func)
            if rect.collidepoint((x, y)):
                func()
                return True

def getActionButton():
    actionButtonUI = UI("actionbtn.png", width-350, height-150)
    actionButtonUI.addClickableRect(actionButtonUI.imgRect, actionButton)
    return actionButtonUI

uiComponents = []

def makeUIComponents():
    global uiComponents
    uiComponents.append(getActionButton())

