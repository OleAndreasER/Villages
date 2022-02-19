#!/bin/python3
import pygame
from library.graphics import drawWorld, drawUI, drag, changeZoom, rightClick, leftClick, leftClickRelease
from library.gamelogic import endTurn
from library.UI import makeUIComponents

width = 1920
height = 1080

fps = 60

isDragging = False

def main():
    global isDragging
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Villages")
    clock = pygame.time.Clock()

    makeUIComponents()

    while True:
        clock.tick(fps)
        pos = None
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    isDragging = True
                    leftClick(win, event.pos)
                elif event.button == 4: #wheelup
                    changeZoom(1, event.pos)
                elif event.button == 5: #wheeldown
                    changeZoom(-1, event.pos)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    leftClickRelease(win, event.pos)
                    isDragging = False 
                elif event.button == 3:
                    rightClick(win, event.pos)

            elif event.type == pygame.MOUSEMOTION:
                if isDragging:
                    drag(event.rel)

        pos = pygame.mouse.get_pos()

        drawWorld(win)
        drawUI(win, *pos)
        pygame.display.update()


if __name__ == "__main__":
    main()
