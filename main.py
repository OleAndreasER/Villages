#!/bin/python3
import pygame
from library.graphics import drawGame

width = 1920
height = 1080

fps = 60

def main():
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
        drawGame(win)
        pygame.display.update()


if __name__ == "__main__":
    main()
