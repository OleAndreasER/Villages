import pygame
import os
from library.gamelogic import actionButton, idle, selectedCitizenAction, lockAction, buildHouse, buildSawMill, getTurn, actionButtonText, isCitizenSelected, actionPointTxt, healthPointTxt, hungerStatusTxt, isNonCitizenSelected, citizenActionButtonTxt, isCitizenMenuHidden, isCitizenActionButtonHidden, isBuildMenuButtonHidden
from library.settings import width, height, eggWhite
from library.Player import currentPlayer

class UI:
    def __init__(self, img, x, y):
        self.img = pygame.image.load(os.path.join("assets", img)).convert_alpha()
        self.imgVersions = [self.img]
        self.imgRect = self.img.get_rect(topleft = (x, y))
        self.textElements = []
        self.clickableRects = []

    isToggle = False
    isPressed = False
    isHidden = staticmethod(lambda: False)

    def setIsHidden(self, predicate):
        self.isHidden = staticmethod(predicate)

    def addClickableRect(self, rect, func):
        self.clickableRects.append((rect, func))

    def addText(self, text, fontSize, pos, shouldUpdate, updatedText, location = "topLeft"):
        self.textElements.append({
            "text":text, "location":location,
            "fontSize":fontSize, "pos":pos,
            "shouldUpdate":shouldUpdate, "updatedText":updatedText
        })

    def addImg(self, imgPath):
        self.imgVersions.append(pygame.image.load(os.path.join("assets", imgPath)).convert_alpha())

    def setImg(self, i):
        if len(self.imgVersions) > i:
            self.img = self.imgVersions[i]

    def toggleImg(self):
        if self.img == self.imgVersions[0]:
            self.img = self.imgVersions[1]
        else:
            self.img = self.imgVersions[0]

    def setText(self, i, text):
        self.textElements[i]["text"] = text

    def updateTexts(self):
        for text in self.textElements:
            if text["shouldUpdate"]():
                text["text"] = text["updatedText"]()

    def render(self, win):
        if self.isHidden(): return

        win.blit(self.img, self.imgRect)

        self.updateTexts()

        for text in self.textElements:
            renderText(win, text)

    def click(self, x, y):
        for rect, func in self.clickableRects:
            if rect.collidepoint((x, y)):
                func()
                if self.isToggle:
                    self.isPressed = not self.isPressed
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
    from library.graphics import hoveredTileInfo
    actionButtonUI = UI("actionbtn.png", width-350, height-150)
    actionButtonUI.addClickableRect(actionButtonUI.imgRect, actionButton)
    actionButtonUI.addImg("actionbtnpressed.png")

    actionButtonUI.addText("Next Turn", 50, (width-320, height-138), true, actionButtonText)
    actionButtonUI.addText("Turn ", 20, (width-320, height-60), true, lambda: f"Turn {getTurn()}")
    actionButtonUI.addText("", 20, (width-30, height-60), true, hoveredTileInfo, "topRight")
    return actionButtonUI

def makeIdleButton():
    idleButtonUI = UI("idlebutton.png", 193, height-421+361)
    idleButtonUI.addClickableRect(pygame.Rect(193, height-421+361, 39, 39), idle) 
    idleButtonUI.setIsHidden(isCitizenMenuHidden)
    return idleButtonUI

def makeResourceBar():
    resourceBarUI = UI("resourcebar.png", 0, 0)
    resourceBarUI.addClickableRect(resourceBarUI.imgRect, doNothing)

    resourceBarUI.addText("0", 13, (65, 0), true, lambda: str(currentPlayer.wood))
    resourceBarUI.addText("0", 13, (195, 0), true, lambda: str(currentPlayer.stone))
    return resourceBarUI

def makeCitizenMenu():
    citizenMenuUI = UI("citizenmenu.png", 0, height-421)
    citizenMenuUI.addClickableRect(citizenMenuUI.imgRect, doNothing)
    citizenMenuUI.addText("Action points: ", 15, (7, height-370), isCitizenSelected, actionPointTxt)
    citizenMenuUI.addText("Health points: ", 15, (7, height-350), isCitizenSelected, healthPointTxt) 
    citizenMenuUI.addText("Hunger status: ", 15, (7, height-330), isCitizenSelected, hungerStatusTxt)
    citizenMenuUI.setIsHidden(isCitizenMenuHidden)
    return citizenMenuUI

def makeCitizenActionButton():
    citizenActionButtonUI = UI("citizenactionbutton.png", 14, height-421+361)
    citizenActionButtonUI.addClickableRect(citizenActionButtonUI.imgRect, selectedCitizenAction)
    citizenActionButtonUI.addText("", 15, (24, height-421+370), isNonCitizenSelected, citizenActionButtonTxt)
    citizenActionButtonUI.setIsHidden(isCitizenActionButtonHidden)
    return citizenActionButtonUI

def makeBuildMenuButton():
    buildMenuButtonUI = UI("buildmenuicon.png", 193, height-421+300)
    buildMenuButtonUI.addClickableRect(buildMenuButtonUI.imgRect, doNothing)
    buildMenuButtonUI.isToggle = True
    buildMenuButtonUI.setIsHidden(isBuildMenuButtonHidden)
    return buildMenuButtonUI

def makeLockButton():
    lockButtonUI = UI("lockiconunlocked.png", 193, height-421+25)
    lockButtonUI.addImg("lockicon.png")
    lockButtonUI.addClickableRect(lockButtonUI.imgRect, lockAction)
    lockButtonUI.isToggle = True
    lockButtonUI.setIsHidden(isCitizenMenuHidden)
    return lockButtonUI

def makeBuildMenu():
    buildMenuUI = UI("buildmenu.png", 260, height-421+8)
    buildMenuUI.addClickableRect(buildMenuUI.imgRect, doNothing)
    buildMenuUI.setIsHidden(isBuildMenuHidden)
    return buildMenuUI

def makeHouseButton():
    houseButtonUI = UI("buildhouseicon.png", 260+9, height-421+8+3+9)
    houseButtonUI.addClickableRect(houseButtonUI.imgRect, buildHouse)
    houseButtonUI.setIsHidden(isBuildMenuHidden)
    return houseButtonUI

def makeSawMillButton():
    sawMillButtonUI = UI("buildsawmillicon.png", 260+9, height-421+8+3+9+9+40)
    sawMillButtonUI.addClickableRect(sawMillButtonUI.imgRect, buildSawMill)
    sawMillButtonUI.setIsHidden(isBuildMenuHidden)
    return sawMillButtonUI

uiComponents = {}
buildButtons = {}
citizenMenuComponents = {}

def makeUIComponents():
    global uiComponents
    global buildButtons
    global citizenMenu

    citizenMenu = {
        "citizenMenu": makeCitizenMenu(),
        "citizenActionButton": makeCitizenActionButton(),
        "idleButton": makeIdleButton(),
        "buildMenuButton": makeBuildMenuButton(),
        "lockButton": makeLockButton(),
        "buildMenu": makeBuildMenu()
    }

    buildButtons = {
        "houseButton": makeHouseButton(),
        "sawMillButton": makeSawMillButton()
    }

    uiComponents = {
        "actionButton": makeActionButton(),
        "resourceBar": makeResourceBar(),
        **citizenMenu,
        **buildButtons
    }


def UIComponent(component):
    return uiComponents[component]

def UIComponents():
    return uiComponents.values()

def buildButtonComponents():
    return buildButtons.values()

def citizenMenuComponents():
    return citizenMenu.values()


def doNothing(): #For clickable UI rects that don't don't do anything (ex. menu backgrounds).
    return

def true(): #True as a function for updating UI
    return True

def isBuildMenuHidden():
    return isCitizenMenuHidden() or not UIComponent("buildMenuButton").isPressed
