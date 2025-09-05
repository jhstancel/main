# settings.py
import pygame as pg

TITLE = "Chocolate Tycoon (Remade)"
WINDOW_W, WINDOW_H = 1280, 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# If your old code used a "logical" canvas and scaled to fit:
LOGICAL_W, LOGICAL_H = 960, 540  # keep your original coordinate system if needed
SCALE_TO_WINDOW = True  # set False if you draw directly at WINDOW size

# Menu/UI geometry used by your existing helpers
MENU_BUTTON_W, MENU_BUTTON_H = 124, 38
INSCREEN_BUTTON_X = 180  # align with your old "in-screen" menu X


def make_surface(size: tuple[int, int], alpha=False) -> pg.Surface:
    flags = pg.SRCALPHA if alpha else 0
    return pg.Surface(size, flags)
