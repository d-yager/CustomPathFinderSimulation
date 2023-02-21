# Custom Path Finder Simulation
#
# author: David Yager

import pygame
import os

WIDTH = 640
HEIGHT = 480

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))

canvas.fill((255, 255, 255))
pygame.display.flip()
pygame.display.set_caption("Custom Path Finder Simulation")
window.fill((0, 0, 0))


def main():
    print("Custom Path Finder Simulation")
    draw()


def draw():
    drawing = True
    drawing_mode = False
    prev_mouse_pos = (0, 0)
    color = (0, 0, 0)
    while drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing_mode = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing_mode = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing_mode:
                    current_mouse_pos = pygame.mouse.get_pos()
                    print(current_mouse_pos)
                    pygame.draw.lines(canvas, color, True, [(current_mouse_pos[0] - 1,
                                                             current_mouse_pos[1] - 1), current_mouse_pos], 8)
                    window.blit(canvas, (0, 0))
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    drawing_mode = False
                    drawing = False


if __name__ == "__main__":
    main()
