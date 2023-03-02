# Custom Path Finder Simulation
#
# author: David Yager

import pygame

BACKGROUND = pygame.image.load("images/background.png")
global TRACK
global TRACK_MASK
FINISH_LINE = pygame.image.load("images/finish_line.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (64, 64))
SPAWN_POINT = pygame.image.load("images/spawn_point.png")
SPAWN_POINT = pygame.transform.scale(SPAWN_POINT, (42, 42))

WIDTH = 640
HEIGHT = 480

pygame.init()
pygame.display.set_caption("Custom Path Finder Simulation")

global drawing_surface

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.blit(canvas, (0, 0))
window.blit(FINISH_LINE, (576, 416))
window.blit(SPAWN_POINT, (0, 0))
pygame.display.update()


class PlayerMarker:
    IMG = pygame.image.load("images/blip.png").convert()
    IMG = pygame.transform.scale(IMG, (16, 16))

    def __init__(self, x, y):
        self.img = self.IMG
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.speed = 1.5
        self.moveX = 0
        self.moveY = 0

    def draw(self, win):
        new_image = self.img
        new_rect = new_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(new_image, new_rect.topleft)
        pygame.display.update()

    def move(self, up=False, down=False, left=False, right=False):
        self.moveX = 0
        self.moveY = 0
        if up and not down:
            self.moveY = -self.speed
        if down and not up:
            self.moveY = self.speed
        if right and not left:
            self.moveX = self.speed
        if left and not right:
            self.moveX = -self.speed

        self.x += self.moveX
        self.y += self.moveY

    def collide(self, track_walls):
        blip_hitbox = pygame.mask.from_surface(self.img)
        collision = track_walls.overlap(blip_hitbox, (int(self.x), (int(self.y))))
        return collision


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
        if player.collide(TRACK_MASK) is not None:
            del player
            playing = False
        else:
            movement_check(player)


def movement_check(blip):
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        blip.move(up=True)
    if pressed_keys[pygame.K_a]:
        blip.move(left=True)
    if pressed_keys[pygame.K_s]:
        blip.move(down=True)
    if pressed_keys[pygame.K_d]:
        blip.move(right=True)


def draw():
    global drawing_surface
    drawing_surface = pygame.Surface((WIDTH, HEIGHT))
    drawing = True
    drawing_mode = False
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
                    drawing_surface.blit(canvas, (0, 0))
                    window.blit(drawing_surface, (0, 0))
                    window.blit(FINISH_LINE, (576, 416))
                    window.blit(SPAWN_POINT, (0, 0))
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    drawing_mode = False
                    drawing = False


def save_image():
    global drawing_surface
    image_to_save = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    image_to_save.fill((255, 255, 255, 0))
    image_to_save.blit(drawing_surface, (0, 0))
    image_to_save.set_colorkey((255, 255, 255))
    pygame.image.save(image_to_save, "images/map.png")


def update_display(win, player):
    global FINISH_LINE
    global TRACK
    global TRACK_MASK
    TRACK = pygame.image.load("images/map.png")
    FINISH_LINE = pygame.image.load("images/finish_line.png")
    FINISH_LINE = pygame.transform.scale(FINISH_LINE, (64, 64))
    TRACK_MASK = pygame.mask.from_surface(TRACK)
    win.blit(BACKGROUND, (0, 0))
    win.blit(FINISH_LINE, (576, 416))
    win.blit(TRACK, (0, 0))
    win.blit(SPAWN_POINT, (0, 0))
    player.draw(win)


if __name__ == "__main__":
    main()
