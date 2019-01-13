import pygame as pg
import random
import time
import sys

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 900, 580
WIDTH_TO_HEIGHT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

FIRE_HEIGHT = 120
FIRE_WIDTH = int(FIRE_HEIGHT * WIDTH_TO_HEIGHT_RATIO)
FIRE_SIZE = FIRE_WIDTH, FIRE_HEIGHT

FIRE_DURATION_SECONDS = 10

MAX_DECAY = 1
MIN_DECAY = 0

MIN_HORIZONTAL_PROPAGATION = -1
MAX_HORIZONTAL_PROPAGATION = 1

colormap = [
    (7,7,7),
    (31,7,7),
    (47,15,7),
    (71,15,7),
    (87,23,7),
    (103,31,7),
    (119,31,7),
    (143,39,7),
    (159,47,7),
    (175,63,7),
    (191,71,7),
    (199,71,7),
    (223,79,7),
    (223,87,7),
    (223,87,7),
    (215,95,7),
    (215,103,15),
    (207,111,15),
    (207,119,15),
    (207,127,15),
    (207,135,23),
    (199,135,23),
    (199,143,23),
    (199,151,31),
    (191,159,31),
    (191,159,31),
    (191,167,39),
    (191,167,39),
    (191,175,47),
    (183,175,47),
    (183,183,47),
    (183,183,55),
    (207,207,111),
    (223,223,159),
    (239,239,199),
    (255,255,255)
]


def create_fire_array():
    fire_pixels = []
    for x in range(FIRE_WIDTH):
        fire_pixels.append([0] * FIRE_HEIGHT)
        fire_pixels[x][0] = 35
    return fire_pixels


def update_fire(fire_pixels):
    for x in range(FIRE_WIDTH):
        for y in reversed(range(1, FIRE_HEIGHT)):
            decay = random.randint(MIN_DECAY, MAX_DECAY)
            x_prop = get_horizontal_propagation(x)
            new_color_index = fire_pixels[x][y - 1] - decay
            if new_color_index >= 0:
                fire_pixels[x + x_prop][y] = new_color_index
            else:
                fire_pixels[x + x_prop][y] = 0


def get_horizontal_propagation(x):
    x_prop_min = min(x, MIN_HORIZONTAL_PROPAGATION)
    x_prop_max = min(FIRE_WIDTH - 1 - x, MAX_HORIZONTAL_PROPAGATION)
    return random.randint(x_prop_min, x_prop_max)


def stop_fire(fire_pixels):
    for x in range(0, FIRE_WIDTH):
        fire_pixels[x][0] = 0


def draw_fire(fire_pixels):
    for x in range(FIRE_WIDTH):
        for y in range(FIRE_HEIGHT):
            pos = x, y
            color = fire_pixels[x][y]
            fire_screen.set_at(pos, colormap[color])


if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()

    screen = pg.display.set_mode(SCREEN_SIZE)
    fire_screen = pg.Surface(FIRE_SIZE)

    fire_pixels = create_fire_array()

    end_time = time.time() + FIRE_DURATION_SECONDS
    fire_ended = False
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()

        if time.time() > end_time and not fire_ended:
            fire_ended = True
            stop_fire(fire_pixels)

        update_fire(fire_pixels)
        draw_fire(fire_pixels)

        scaled_surface = pg.transform.scale(fire_screen, SCREEN_SIZE)
        flipped_and_scaled_surface = pg.transform.flip(scaled_surface, False, True)

        screen.blit(flipped_and_scaled_surface, (0, 0))
        pg.display.update()
        #clock.tick(30)
