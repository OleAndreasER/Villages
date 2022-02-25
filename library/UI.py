import pygame
import os
from library.gamelogic import actionButton, idle, citizenAction
from library.settings import width, height, eggWhite

class UI:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(os.path.join("assets", img)).convert_alpha()
        self.imgVersions = [self.img]
        self.imgRect = self.img.get_rect(topleft = (x, y))
        self.textElements = []
        self.clickableRects = []

    isHidden = False

    def addClickableRect(self, rect, func):
        self.clickableRects.append((rect, func))

    def addText(self, text, fontSize, pos, location = "topLeft"):
        self.textElements.append({
            "text":text, "location":location, "fontSize":fontSize, "pos":pos 
        })

    def addImg(self, imgPath):
        self.imgVersions.append(pygame.image.load(os.path.join("assets", imgPath)).convert_alpha())

    def switchImg(self, i):
        self.img = self.imgVersions[i]

    def setText(self, i, text):
        self.textElements[i]["text"] = text

    def render(self, win):
        if self.isHidden: return
        win.blit(self.img, self.imgRect)
        for text in self.textElements:
            renderText(win, text)

    def click(self, x, y):
        for rect, func in self.clickableRects:
            if rect.collidepoint((x, y)):
                func()
                return True
        return False

def textSurface(text, fontSize):
    font = pygame.font.SysFont("verdana", fontSize)
    return font.render(text, True, eggWhite)

def renderText(win, text):
    surface = textSurface(text["text"], text["fontSize"])
    rect = None
    if text["location"] == "topLeft":
        rect = surface.get_rect(topleft = text["pos"])
    elif text["location"] == "topRight":
        rect = surface.get_rect(topright = text["pos"])
        
    win.blit(surface, rect)

#UI Components
def makeActionButton():
    actionButtonUI = UI("actionbtn.png", width-350, height-150)
    actionButtonUI.addClickableRect(actionButtonUI.imgRect, actionButton)
    actionButtonUI.addImg("actionbtnpressed.png")

    actionButtonUI.addText("Next Turn", 50, (width-320, height-138))
    actionButtonUI.addText("Turn ", 20, (width-320, height-60))
    actionButtonUI.addText("", 20, (width-30, height-60), "topRight")
    return actionButtonUI

def makeIdleButton():
    idleButtonUI = UI("idlebutton.png", 193, height-421+361)
    idleButtonUI.addClickableRect(pygame.Rect(193, height-421+361, 39, 39), idle) 
    idleButtonUI.addImg("idlebutton.png")
    return idleButtonUI

def makeResourceBar():
    resourceBarUI = UI("resourcebar.png", 0, 0)
    resourceBarUI.addClickableRect(resourceBarUI.imgRect, doNothing)
    resourceBarUI.addImg("resourcebar.png")

    resourceBarUI.addText("0", 13, (65, 0))
    resourceBarUI.addText("0", 13, (195, 0))
    return resourceBarUI

def makeCitizenMenu():
    citizenMenuUI = UI("citizenmenu.png", 0, height-421)
    citizenMenuUI.addClickableRect(citizenMenuUI.imgRect, doNothing)
    citizenMenuUI.addText("Action points: ", 15, (7, height-370))
    citizenMenuUI.addText("Health points: ", 15, (7, height-350))
    citizenMenuUI.addText("Hunger status: ", 15, (7, height-330))
    return citizenMenuUI

def makeCitizenActionButton():
    citizenActionButtonUI = UI("citizenactionbutton.png", 14, height-421+361)
    citizenActionButtonUI.addClickableRect(citizenActionButtonUI.imgRect, citizenAction)
    citizenActionButtonUI.addImg("citizenactionbutton.png")
    citizenActionButtonUI.addText("", 15, (24, height-421+370))
    return citizenActionButtonUI

uiComponents = {}

def makeUIComponents():
    global uiComponents
    uiComponents = {
        "actionButton": makeActionButton(),
        "resourceBar": makeResourceBar(),
        "citizenMenu": makeCitizenMenu(),
        "citizenActionButton": makeCitizenActionButton(),
        "idleButton": makeIdleButton()
    }

def getUIComponents():
    return uiComponents

def doNothing(): #For clickable UI rects that don't don't do anything (ex. menu backgrounds).
    return

