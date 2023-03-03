# Custom Path Finder Simulation
#
# author: David Yager

import pygame
import neat

BACKGROUND = pygame.image.load("images/background.png")
global TRACK
global TRACK_MASK
global SELECTED_TRACK
global FINISH_LINE_MASK
global DRAWING_SURFACE
global NO_MAP
NO_MAP = True

FINISH_LINE = pygame.image.load("images/finish_line.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (64, 64))
SPAWN_POINT = pygame.image.load("images/spawn_point.png")
SPAWN_POINT = pygame.transform.scale(SPAWN_POINT, (42, 42))

WIDTH = 640
HEIGHT = 480

pygame.init()
pygame.display.set_caption("Custom Path Finder Simulation")

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
        self.speed = 10
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
        if self.x < 0:
            self.x = 0
        if self.x > 623:
            self.x = 623
        if self.y < 0:
            self.y = 0
        if self.y > 463:
            self.y = 463

        self.x += self.moveX
        self.y += self.moveY

    def collide(self, collidable_object):
        blip_hitbox = pygame.mask.from_surface(self.img)
        collision = collidable_object.overlap(blip_hitbox, (int(self.x), int(self.y)))
        return collision


def main(genomes, config):
    print("Custom Path Finder Simulation")
    draw()
    save_image()
    nets = []
    ge = []
    players = []
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(PlayerMarker(12, 12))
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    finish_line_x, finish_line_y = 576, 416

    playing = True
    while playing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
        for i, player in enumerate(players):
            update_display(window, players)
            distance_to_finish = ((finish_line_x - player.x)**2 + (finish_line_y - player.y)**2)**0.5
            output = nets[i].activate((player.x, player.y, finish_line_x, finish_line_y))
            up, down, left, right = [bool(round(o)) for o in output]
            player.move(up=up, down=down, left=left, right=right)
            new_distance_to_finish = ((finish_line_x - player.x) ** 2 + (finish_line_y - player.y) ** 2) ** 0.5
            genomes[i][1].fitness += distance_to_finish - new_distance_to_finish
            if player.collide(TRACK_MASK) is not None:
                genomes[i][1].fitness -= 1
                print("collide")
                players.pop(i)
                nets.pop(i)
                genomes.pop(i)
        for i, g in genomes:
            if player.collide(FINISH_LINE_MASK) is not None:
                print("\nYou have won!\n")
                genomes[i][1].fitness += 999
                # else:
                #    movement_check(player)


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
    global DRAWING_SURFACE
    if NO_MAP:
        DRAWING_SURFACE = pygame.Surface((WIDTH, HEIGHT))
        drawing = True
        pen_down = False
        color = (0, 0, 0)
        while drawing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    drawing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pen_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pen_down = False
                elif event.type == pygame.MOUSEMOTION:
                    if pen_down:
                        current_mouse_pos = pygame.mouse.get_pos()
                        pygame.draw.lines(canvas, color, True, [(current_mouse_pos[0] - 1,
                                                                 current_mouse_pos[1] - 1), current_mouse_pos], 8)
                        DRAWING_SURFACE.blit(canvas, (0, 0))
                        window.blit(DRAWING_SURFACE, (0, 0))
                        window.blit(FINISH_LINE, (576, 416))
                        window.blit(SPAWN_POINT, (0, 0))
                        pygame.display.update()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        pen_down = False
                        drawing = False


def save_image():
    global DRAWING_SURFACE
    global SELECTED_TRACK
    global NO_MAP
    if NO_MAP:
        image_to_save = pygame.Surface(window.get_size(), pygame.SRCALPHA)
        image_to_save.fill((255, 255, 255, 0))
        image_to_save.blit(DRAWING_SURFACE, (0, 0))
        image_to_save.set_colorkey((255, 255, 255))
        # input "please name your track" (assign to SELECTED_TRACK)
        pygame.image.save(image_to_save, "images/map.png")  # save as f'images/{SELECTED_TRACK}.png'
        NO_MAP = False


def update_display(win, players):
    global FINISH_LINE
    global FINISH_LINE_MASK
    global TRACK
    global TRACK_MASK
    TRACK = pygame.image.load("images/map.png")  # change to "images/selectedmap.png"
    FINISH_LINE = pygame.image.load("images/finish_line.png")
    FINISH_LINE = pygame.transform.scale(FINISH_LINE, (64, 64))
    finish_line_mask_surface = pygame.Surface((WIDTH, HEIGHT))
    finish_line_mask_surface.fill((0, 255, 0))
    finish_line_mask_surface.blit(FINISH_LINE, (576, 416))
    finish_line_mask_surface.set_colorkey((0, 255, 0))
    TRACK_MASK = pygame.mask.from_surface(TRACK)
    FINISH_LINE_MASK = pygame.mask.from_surface(finish_line_mask_surface)
    win.blit(BACKGROUND, (0, 0))
    win.blit(FINISH_LINE, (576, 416))
    win.blit(TRACK, (0, 0))
    win.blit(SPAWN_POINT, (0, 0))
    for player in players:
        player.draw(win)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 30)


if __name__ == "__main__":
    config_file = "config-feedforward.txt"
    run(config_file)
