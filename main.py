# Custom Path Finder Simulation
#
# author: David Yager

import pygame
import os

BACKGROUND = pygame.image.load("images/background.png")

WIDTH = 640
HEIGHT = 480

pygame.init()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Custom Path Finder Simulation")
window.blit(canvas, (0, 0))
pygame.display.update()


class PlayerMarker:
    IMG = pygame.image.load("images/blip.png").convert()

    def __init__(self, x, y):
        self.img = self.IMG
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.speed = 0.1
        self.moveX = 0
        self.moveY = 0

    def move(self, up=False, down=False, left=False, right=False):
        self.moveX = 0
        self.moveY = 0
        if up and not down:
            self.moveY = -self.speed
            print(up)
        if down and not up:
            self.moveY = self.speed
        if right and not left:
            self.moveX = self.speed
        if left and not right:
            self.moveX = -self.speed

        self.x += self.moveX
        self.y += self.moveY

    def draw(self, win):
        new_image = self.img
        new_rect = new_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(new_image, new_rect.topleft)
        pygame.display.update()


def main():
    print("Custom Path Finder Simulation")
    draw()
    save_image()
    player = PlayerMarker(12, 12)
    playing = True
    while playing:
        update_display(window, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            player.move(up=True)
        if pressed_keys[pygame.K_a]:
            player.move(left=True)
        if pressed_keys[pygame.K_s]:
            player.move(down=True)
        if pressed_keys[pygame.K_d]:
            player.move(right=True)


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
                    pygame.draw.lines(canvas, color, True, [(current_mouse_pos[0] - 1,
                                                             current_mouse_pos[1] - 1), current_mouse_pos], 8)
                    window.blit(canvas, (0, 0))
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    drawing_mode = False
                    drawing = False


def save_image():
    image_to_save = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    image_to_save.fill((255, 255, 255, 0))
    image_to_save.blit(window, (0, 0))
    image_to_save.set_colorkey((255, 255, 255))
    pygame.image.save(image_to_save, "images/map.png")


def update_display(win, player):
    win.blit(BACKGROUND, (0, 0))
    player.draw(win)


if __name__ == "__main__":
    main()
