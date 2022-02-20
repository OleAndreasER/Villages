
#width = 1920 
#height = 1080 

width = 1366
height = 768 

fps = 60

#Colors

eggWhite = (239,234,231)
tileSelectColor = (225,229,124)
white = (225,225,225)
grassGreen = (3,90,35)
black = (0,0,0)

#Keybinds
import pygame
from library.gamelogic import actionButton, idle, citizenAction

keybinds = [
    (pygame.K_RETURN, actionButton),
    (pygame.K_SPACE, idle),
    (pygame.K_a, citizenAction)
]
#http://www.pygame.org/docs/ref/key.html
