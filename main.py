#!/bin/python3
import pygame
from library.graphics import drawGame, drag, changeZoom, rightClick

width = 1920
height = 1080

fps = 60

isDragging = False

def main():
    global isDragging
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Villages")
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    isDragging = True
                    rightClick(win, event.pos)
                elif event.button == 4: #wheelup
                    changeZoom(1, event.pos)
                elif event.button == 5: #wheeldown
                    changeZoom(-1, event.pos)
                    
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    isDragging = False 

            elif event.type == pygame.MOUSEMOTION:
                if isDragging:
                    drag(event.rel)

        drawGame(win)
        pygame.display.update()


if __name__ == "__main__":
    main()
