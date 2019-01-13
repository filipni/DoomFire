import pygame as pg
import numpy as np
import random
import math
import sys

# Window parameters
WINDOW_NAME = "DoomFire"

FIRE_SIZE = FIRE_WIDTH, FIRE_HEIGHT = 100, 100
SCALE_FACTOR = 3
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = SCALE_FACTOR * FIRE_WIDTH, SCALE_FACTOR * FIRE_HEIGHT

# Fire parameters
MAX_DECAY = 1
MIN_DECAY = 0

MIN_HORIZONTAL_PROPAGATION = -1
MAX_HORIZONTAL_PROPAGATION = 1

FIRE_DURATION_SECONDS = 7

# Video parameters
VIDEO_DURATION_SECONDS = 10
FRAMERATE = 30
FRAMES_TO_GENERATE = FRAMERATE * VIDEO_DURATION_SECONDS

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


def update_fire(fire_array):
    for x in range(FIRE_WIDTH):
        for y in reversed(range(1, FIRE_HEIGHT)):
            decay = random.randint(MIN_DECAY, MAX_DECAY)
            x_prop = get_horizontal_propagation(x)
            new_color_index = fire_array[x, y - 1] - decay
            fire_array[x + x_prop, y] = max(new_color_index, 0)


def get_horizontal_propagation(x):
    x_prop_min = min(x, MIN_HORIZONTAL_PROPAGATION)
    x_prop_max = min(FIRE_WIDTH - 1 - x, MAX_HORIZONTAL_PROPAGATION)
    return random.randint(x_prop_min, x_prop_max)


def draw_fire(fire_pixel_colors, fire_array):
    for x in range(FIRE_WIDTH):
        for y in range(FIRE_HEIGHT):
            color = fire_pixel_colors[x, y]
            fire_array[x, y] = colormap[int(color)]


def render_fire():
    fire_array = np.zeros((FIRE_WIDTH, FIRE_HEIGHT, 3), dtype=int)

    fire_pixel_colors = np.zeros(FIRE_SIZE, dtype=int)
    fire_pixel_colors[:, 0] = len(colormap) - 1  # Init first row with highest color index, this will generate the fire

    fire_ended = False
    fire_frames = []
    frame_counter = 0
    while frame_counter < FRAMES_TO_GENERATE:
        current_second = frame_counter / FRAMERATE
        if current_second >= FIRE_DURATION_SECONDS and not fire_ended:
            fire_ended = True
            fire_pixel_colors[:, 0] = 0  # Kill fire by setting first row to lowest color index

        update_fire(fire_pixel_colors)
        draw_fire(fire_pixel_colors, fire_array)

        fire_surface = pg.surfarray.make_surface(fire_array)
        flipped_surface = pg.transform.flip(fire_surface, False, True)
        flipped_and_scaled_surface = pg.transform.scale(flipped_surface, SCREEN_SIZE)

        fire_frames.append(flipped_and_scaled_surface)
        frame_counter += 1

        percentage_done = math.ceil(100 * current_second / VIDEO_DURATION_SECONDS)
        print("\r{}% done".format(percentage_done), end="")

    return fire_frames


def play_fire(fire):
    pg.init()
    pg.display.set_caption(WINDOW_NAME)

    screen_surface = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    for frame in fire:
        handle_events()

        screen_surface.blit(frame, (0, 0))
        pg.display.update()

        clock.tick(FRAMERATE)


def handle_events():
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()


if __name__ == "__main__":
    print("Rendering fire...")
    fire = render_fire()
    play_fire(fire)

