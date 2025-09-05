# settings.py
import pygame as pg

TITLE = "Chocolate Tycoon (Remade)"
# settings.py
WINDOW_W, WINDOW_H = 1280, 720   # keep if you like a bigger window
LOGICAL_W, LOGICAL_H = 1080, 720 # << this must match your art
SCALE_TO_WINDOW = True

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Menu/UI geometry used by your existing helpers
MENU_BUTTON_W, MENU_BUTTON_H = 124, 38
INSCREEN_BUTTON_X = 180  # align with your old "in-screen" menu X


def make_surface(size: tuple[int, int], alpha=False) -> pg.Surface:
    flags = pg.SRCALPHA if alpha else 0
    return pg.Surface(size, flags)
