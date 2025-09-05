"""
Chocolate Tycoon — pygame_remade.py
Fully-wired starter that ties together:
- ty_utils.py (login + save file format you already use)
- assets in ./graphics
- game loop + scene-ready structure
This file can stand alone as your entry point.
"""
from __future__ import annotations

import os
import sys
import time
import pygame as pg
from pathlib import Path
import random
import ty_utils as f  # your existing ty_utils.py
import settings as S


ROOT_DIR = Path(__file__).parent
ASSETS = ROOT_DIR / "assets"
IMAGES = ASSETS / "images"
SOUNDS = ASSETS / "sounds"

# ---------- constants ----------
GRID_ROWS, GRID_COLS = 4, 8
TILE_W = TILE_H = 126
SCREEN_W, SCREEN_H = 1080, 720
FPS = 60

# ---------- paths / save root ----------
ROOT_DIR = Path(__file__).parent
SAVE_DIR = ROOT_DIR / "saveFiles"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Point ty_utils.py at this save folder (overrides the hardcoded path in ty_utils.py)
f.root = str(SAVE_DIR) + os.sep  # e.g. ".../saveFiles/" cross-platform


def make_menu_button_rects(inScreenButtonX: int, menuButtonHitboxes: list[list[int]]) -> list[pg.Rect]:
    return [pg.Rect(inScreenButtonX, y, 124, 38) for (_, y) in menuButtonHitboxes]


def clicked_outside_menu(pos: tuple[int, int], menu_rect: pg.Rect) -> bool:
    return not menu_rect.collidepoint(pos)



class land:
    def __init__(self):
        self.farmType = None
        self.neighbors = []
        self.tileLocation = 0
        self.location = (0, 0)
        self.update = 0
        self.reward = 5
        self.rate = 1
        self.auto = 0

    def makeNeighbors(self):
        # 4x8 grid
        tileIsNotOnTopBorder = self.tileLocation >= 8
        tileIsNotOnLeftBorder = self.tileLocation not in (0, 8, 16, 24)
        if tileIsNotOnLeftBorder and tileIsNotOnTopBorder:
            self.neighbors = [self.tileLocation - 8, self.tileLocation + 1,
                              self.tileLocation + 8, self.tileLocation - 1]
        elif not tileIsNotOnTopBorder:
            self.neighbors = [None, self.tileLocation + 1,
                              self.tileLocation + 8, self.tileLocation - 1]
        elif not tileIsNotOnLeftBorder:
            self.neighbors = [self.tileLocation - 8, self.tileLocation + 1,
                              self.tileLocation + 8, None]


class farm(land):
    def __init__(self, app):
        super().__init__()
        self.app = app  # hold a reference to GameApp (for save + user)

    def upgrade(self):
        full = 100
        if self.update < full:
            self.update = min(self.update + self.rate, full)

    def rewardUpdate(self):
        # app.save format: [gold, wheat, cocoa, ?, map rows..., auto rows...]
        if self.farmType in (3, "3"):  # cocoa
            self.app.save[2] = str(int(self.app.save[2]) + self.reward)
        elif self.farmType in (4, "4"):  # wheat
            self.app.save[1] = str(int(self.app.save[1]) + self.reward)
        # persist using the app's helper (no root/userName globals)
        self.app._persist_save()

    def displayFarm(self, screen, iconTypes, iconPos, progressBarTypes, wheatStages, cocoaStages):
        r, c = self.location
        stage = 0 if self.update < 33 else (1 if self.update < 67 else 2)
        if self.farmType in (3, "3"):
            screen.blit(cocoaStages[stage], iconPos[r][c])
        elif self.farmType in (4, "4"):
            screen.blit(wheatStages[stage], iconPos[r][c])


# --- stacked toast notifications -------------------------------------------
class Toast:
    def __init__(self, text: str, kind: str = "info", ttl: float = 2.6):
        self.text = text
        self.kind = kind  # "info" | "warn" | "error"
        self.ttl  = ttl   # seconds to live
        self.age  = 0.0

    @property
    def alive(self) -> bool:
        return self.age < self.ttl

    @property
    def alpha(self) -> int:
        # last 0.6s fade out
        fade = 0.6
        if self.age <= self.ttl - fade:
            return 255
        remain = max(0.0, self.ttl - self.age)
        return int(255 * (remain / fade))



class GameApp:
    def __init__(self):
        # --- init pygame ---
        pg.init()
        # inside GameApp.__init__ right after you set up screen/clock
        self.inScreenButtonX = 0
        self.cocoaFarmList = []
        self.wheatFarmList = []
        self.tileTypes = []
        self.buttonData = [[2, 3, 10, 12, 0, 0, 0, 0], [8, 6, 0, 0, 0, 0, 0, 0]]
        self.button_positions = []
        self.button_y_positions = []
        self.menu_button_rects = []
        self.tile_positions = []
        self.tile_rects = []
        self.menu_img = None
        self.plus = None
        self.minus = None
        self.menu_rect = pg.Rect(0, 0, 0, 0)  # set real size later in _load_images_and_sounds
        try:
            pg.mixer.init()
        except Exception:
            pass
        self.screen = pg.display.set_mode((S.WINDOW_W, S.WINDOW_H), pg.RESIZABLE)
        pg.display.set_caption(S.TITLE)

        # Optional logical canvas (lets you keep old 960x540 math and scale to window)
        self.logical = pg.Surface((S.LOGICAL_W, S.LOGICAL_H), pg.SRCALPHA) if S.SCALE_TO_WINDOW else None

        self.clock = pg.time.Clock()
        self.dt = 0.0

        # --- login & save ---
        self.user = f.logIn()
        if not self.user:
            print("Account created. Restart the game to play.")
            pg.quit()
            sys.exit(0)
        self.save: list[str] = f.lineGrabber(f.root + self.user)  # 12+ lines

        # mapData (4 rows) + autoData (4 rows) live at the tail
        self.mapData: list[str] = [str(self.save[i + 4]) for i in range(len(self.save) - 8)]
        self.autoData: list[str] = [str(self.save[i + 8]) for i in range(len(self.save) - 8)]

        # --- load assets ---
        self.font = pg.font.SysFont("Acumin-Variable-Concept.ttf", 20)
        self._load_images_and_sounds()

        # --- build geometry ---
        self.tile_positions = self._grid_positions(GRID_ROWS, GRID_COLS, start=(8, 8), step=(134, 134))
        self.tile_rects = [pg.Rect(x, y, TILE_W, TILE_H) for (x, y) in self.tile_positions]

        # --- game state flags ---
        self.menuActive = False
        self.toolActive: str | None = None
        self.selectedTile: int | None = None

    # ---------- helpers ----------
    def _img(self, rel: str, size: tuple[int, int] | None = None) -> pg.Surface:
        surf = pg.image.load(str(IMAGES / rel)).convert_alpha()
        return pg.transform.scale(surf, size) if size else surf

    def _sfx(self, rel: str) -> pg.mixer.Sound | None:
        """Load from assets/sounds. Accepts strings that accidentally start with 'sound/'."""
        rel = rel.replace("\\", "/")
        if rel.startswith("sound/"):
            rel = rel[6:]  # strip leading 'sound/'
        path = SOUNDS / rel
        try:
            return pg.mixer.Sound(str(path))
        except Exception as e:
            print(f"[audio] couldn't load {path}: {e}")
            return None

    def _grid_positions(self, rows: int, cols: int, start=(0, 0), step=(0, 0)) -> list[tuple[int, int]]:
        sx, sy = start
        dx, dy = step
        return [(sx + c * dx, sy + r * dy) for r in range(rows) for c in range(cols)]

    def _load_images_and_sounds(self) -> None:
        # Use the current window size for HUD/menu scaling
        geo_w, geo_h = (self.logical.get_size() if getattr(self, "logical", None) else self.screen.get_size())

        # --- images (tiles, HUD, menu, icons) ---
        self.HUD = self._img("Map Final.png", (geo_w, geo_h))
        self.lockedLand = self._img("LockedLand.png", (TILE_W, TILE_H))
        self.unlockedLand = self._img("UnlockedLand.png", (TILE_W, TILE_H))
        self.establishedLand = self._img("EstablishedLand.png", (TILE_W, TILE_H))

        self.wheatStages = [
            self._img("wheat_farm_ungrown_NEW.PNG", (TILE_W, TILE_H)),
            self._img("wheat_farm_grown_new.PNG", (TILE_W, TILE_H)),
            self._img("wheat_farm_grown_more_NEW.PNG", (TILE_W, TILE_H)),
        ]
        self.cocoaStages = [
            self._img("cocoa_farm_stage1.PNG", (TILE_W, TILE_H)),
            self._img("cocoa_farm_stage2.PNG", (TILE_W, TILE_H)),
            self._img("cocoa_farm_stage3.PNG", (TILE_W, TILE_H)),
        ]

        self.menu_img = self._img("Menu.png", (int(geo_w / 1.5), int(geo_h / 1.5)))
        self.plus = self._img("plus.png", (25, 15))
        self.minus = self._img("minus.png", (25, 15))

        self.inMenuButton = self._img("InMenuButton.png", (124, 38))
        self.inMenuButtonMaterials = self._img("MenuTileMaterials.png", (124, 38))
        self.inMenuButtonMaterialsToggled = self._img("MenuTileMaterialsToggled.png", (124, 38))
        self.inMenuButtonBazaar = self._img("MenuTileBazaar.png", (124, 38))
        self.inMenuButtonBazaarToggled = self._img("MenuTileBazaarToggled.png", (124, 38))
        self.inMenuButtonAutomation = self._img("MenuTileAutomation.png", (124, 38))
        self.inMenuButtonAutomationToggled = self._img("MenuTileAutomationToggled.png", (124, 38))
        self.inMenuButtons = [
            self.inMenuButton,
            self.inMenuButtonMaterials, self.inMenuButtonMaterialsToggled,
            self.inMenuButtonBazaar, self.inMenuButtonBazaarToggled,
            self.inMenuButtonAutomation, self.inMenuButtonAutomationToggled
        ]

        # Icons (used by farm display)
        self.cocoaFarmIcon = self._img("Cocoa Bean.png", (126, 126))
        self.wheatFarmIcon = self._img("wheat.png", (126, 126))
        self.iconTypes = [None, None, None, self.cocoaFarmIcon, self.wheatFarmIcon]

        self.iconPos = [
            [(8, 8), (142, 8), (276, 8), (410, 8), (544, 8), (678, 8), (812, 8), (946, 8)],
            [(8, 142), (142, 142), (276, 142), (410, 142), (544, 142), (678, 142), (812, 142), (946, 142)],
            [(8, 276), (142, 276), (276, 276), (410, 276), (544, 276), (678, 276), (812, 276), (946, 276)],
            [(8, 410), (142, 410), (276, 410), (410, 410), (544, 410), (678, 410), (812, 410), (946, 410)]
        ]

        # Menu text boxes
        self.inMenuResourcesTextBox = self._img("In Menu Resources Text Box.png", (520, 400))
        self.inMenuBazaarTextBox = self.inMenuResourcesTextBox

        # Progress bars
        self.progressBar0 = self._img("Progress Bar No Mass.png", (71, 8))
        self.progressBar1 = self._img("Progress Bar One Mass.png", (71, 8))
        self.progressBar2 = self._img("Progress Bar Two Mass.png", (71, 8))
        self.progressBarTypes = [self.progressBar0, self.progressBar1, self.progressBar2]

        # --- sounds (no "sound/" prefix; guard against missing audio) ---
        try:
            if not pg.mixer.get_init():
                pg.mixer.init()
        except Exception:
            # Audio is optional; continue without mixer
            pass

        # _sfx() should already normalize & return None on failure; still guard at play time.
        # Sounds (guard mixer init; load bare filenames; filter out Nones)
        try:
            if not pg.mixer.get_init():
                pg.mixer.init()
        except Exception:
            pass

        self.coinCollectSound = self._sfx("coincollect.wav")
        self.plantSound = [s for s in (
            self._sfx("plant1.ogg"),
            self._sfx("plant2.ogg"),
            self._sfx("plant3.ogg"),
        ) if s]
        self.buildSound = [s for s in (
            self._sfx("stone1.ogg"),
            self._sfx("stone2.ogg"),
            self._sfx("stone3.ogg"),
            self._sfx("stone4.ogg"),
        ) if s]

        # Button data (robust; supports CSV, spaces, or old per-digit; safe default)
        default_button_data = [
            [2, 3, 10, 12, 0, 0, 0, 0],  # top row
            [8, 6, 0, 0, 0, 0, 0, 1],  # bottom row (menu at end)
        ]
        btn_path = ASSETS / "buttondata.txt"
        self.buttonData = default_button_data
        try:
            text = btn_path.read_text(encoding="utf-8").strip()
            if text:
                parsed = []
                for line in (ln.strip() for ln in text.splitlines() if ln.strip()):
                    if "," in line or " " in line or "\t" in line:
                        tokens = [t for t in line.replace(",", " ").split()]
                        row = [int(t) for t in tokens]
                    else:
                        row = [int(ch) for ch in line]
                    row = (row + [0] * 8)[:8]
                    parsed.append(row)
                if len(parsed) >= 2:
                    self.buttonData = [parsed[0][:8], parsed[1][:8]]
        except FileNotFoundError:
            pass

        # --- button images ---
        self.menuButton = self._img("MenuButton.png", (126, 83))
        self.buttonBackgroundReleased = self._img("Button Backgrounds Released.png", (126, 83))
        self.harvestButton = self._img("Farm Tool Button Icon.png", (126, 83))
        self.harvestButtonToggled = self._img("Farm Tool Button Toggled.png", (126, 83))
        self.buildButton = self._img("Building Tool.png", (126, 83))
        self.buildButtonToggled = self._img("Building Tool Toggled.png", (126, 83))
        self.wheatButton = self._img("Wheat Tool.png", (126, 83))
        self.wheatButtonToggled = self._img("Wheat Tool Toggled.png", (126, 83))
        self.cocoaButton = self._img("Cocoa Tool.png", (126, 83))
        self.cocoaButtonToggled = self._img("Cocoa Tool Toggled.png", (126, 83))
        self.shovelButton = self._img("Shovel Tool.png", (126, 83))
        self.shovelButtonToggled = self._img("Shovel Tool Toggled.png", (126, 83))
        self.automationTool = self._img("Automation Tool.png", (126, 83))
        self.automationToolToggled = self._img("Automation Tool Toggled.png", (126, 83))

        self.buttonTypes = [
            self.buttonBackgroundReleased, self.menuButton,
            self.harvestButton, self.buildButton,
            self.harvestButtonToggled, self.buildButtonToggled,
            self.wheatButton, self.wheatButtonToggled,
            self.cocoaButton, self.cocoaButtonToggled,
            self.shovelButton, self.shovelButtonToggled,
            self.automationTool, self.automationToolToggled
        ]

        # --- button geometry ---

        self.button_positions = [8, 142, 276, 410, 544, 678, 812, 946,
                                 8, 142, 276, 410, 544, 678, 812, 946]
        top_y = geo_h - 176  # 720-544 when geo_h=720
        bot_y = geo_h - 85  # 720-635 when geo_h=720
        self.button_y_positions = [top_y] * 8 + [bot_y] * 8

        # --- in-menu button rects (needs self.inScreenButtonX set elsewhere in __init__) ---
        menu_w, menu_h = self.menu_img.get_size()
        x0 = geo_w - int(1.25 * menu_w)
        y0 = geo_h - int(1.25 * menu_h)
        self.menu_rect = pg.Rect(x0, y0, menu_w, menu_h)  # <- store the real rect
        self.inScreenButtonX = x0 + 18

        menuButtonHitboxes = [[self.inScreenButtonX, y0 + off]
                              for off in (71, 131, 191, 251, 311, 371, 431)]
        self.menu_button_rects = make_menu_button_rects(self.inScreenButtonX, menuButtonHitboxes)

        # --- tile rects (click detection) ---
        self.tile_rects = [pg.Rect(x, y, TILE_W, TILE_H) for (x, y) in self.tile_positions]

        # --- Market +/- hitboxes ---
        self.wheatPlusRect = pg.Rect(500, 182 + 3 + 64 + 62, 25, 15)
        self.wheatMinusRect = pg.Rect(500 + 38, 182 + 3 + 64 + 62, 25, 15)
        self.cocoaMinusRect = pg.Rect(500 + 38, 182 + 3 + 105 + 62, 25, 15)
        self.cocoaPlusRect = pg.Rect(500, 182 + 3 + 105 + 62, 25, 15)

        # --- UI state defaults ---
        self.menuActive = False
        self.resourcesOpened = False
        self.marketOpened = False
        self.automationOpened = False

        self.toolActive = None  # type: str | None
        self.selectedTile = None  # type: int | None
        self.selectedButton = None  # type: int | None

        # Toasts (stacked notifications)
        self.toasts: list[Toast] = []
        self.max_toasts = 6  # keep the stack tidy

        # Toggles (preserve original semantics)
        self.farmingToolTog = 1
        self.buildingToolTog = 1
        self.demoTog = 0
        self.automationTog = 0
        self.wheatSeedsTog = 1
        self.cocoaSeedsTog = 1
        self.menuTog = 0

        # Alias used elsewhere
        self.progressBars = self.progressBarTypes

    # ---------- helpers ----------
    def toast(self, msg: str, kind: str = "info", ttl: float = 2.6) -> None:
        """Push a stacked toast; newest appears at the bottom and fades out."""
        self.toasts.append(Toast(msg, kind, ttl))
        # trim if we exceed the cap
        if len(self.toasts) > self.max_toasts:
            self.toasts = self.toasts[-self.max_toasts:]

    def _update_toasts(self, dt: float) -> None:
        for t in self.toasts:
            t.age += dt
        self.toasts = [t for t in self.toasts if t.alive]

    def _draw_toasts(self, canvas: pg.Surface) -> None:
        # styles per kind
        styles = {
            "info": ((30, 30, 35), (230, 230, 230)),  # bg, text
            "warn": ((60, 45, 8), (255, 230, 150)),
            "error": ((60, 10, 10), (255, 190, 190)),
        }
        pad = 8
        gap = 6
        # bottom-left stack
        x = 12
        y = canvas.get_height() - 12
        # newest should appear on the bottom; draw oldest first
        for t in self.toasts[-self.max_toasts:]:
            bg_col, fg_col = styles.get(t.kind, styles["info"])
            text_surf = self.font.render(t.text, True, fg_col)
            w, h = text_surf.get_size()
            box = pg.Surface((w + pad * 2, h + pad * 2), pg.SRCALPHA)
            box.fill((*bg_col, max(70, t.alpha)))  # translucent bg + fade
            y -= box.get_height()
            canvas.blit(box, (x, y))
            canvas.blit(text_surf, (x + pad, y + pad))
            y -= gap

    def _blit_label(self, text: str, pos: tuple[int, int]) -> None:
        surf = self.font.render(str(text), True, (199, 178, 153))
        self.screen.blit(surf, pos)

    def _mouse_pos(self) -> tuple[int, int]:
        """Return mouse position in the same coordinate space we draw in."""
        mx, my = pg.mouse.get_pos()
        # if we draw to a logical canvas, convert window coords → logical coords
        if getattr(self, "logical", None):
            sw, sh = self.screen.get_size()
            lw, lh = self.logical.get_size()
            # avoid divide-by-zero; int math keeps it stable
            if sw > 0 and sh > 0:
                mx = mx * lw // sw
                my = my * lh // sh
        return (mx, my)

    # ---------- in-game menu ----------
    def menu_display(self) -> None:
        screen = self.screen
        menu = self.menu_img

        # Bottom-right anchored
        x0 = screen.get_width() - int(1.25 * menu.get_width())
        y0 = screen.get_height() - int(1.25 * menu.get_height())
        screen.blit(menu, (x0, y0))

        # 7 stacked buttons
        y_offs = [71, 131, 191, 251, 311, 371, 431]

        # Resources tab (index 0)
        btn0 = self.inMenuButtons[2] if self.resourcesOpened else self.inMenuButtons[1]
        screen.blit(btn0, (self.inScreenButtonX, y0 + y_offs[0]))

        # Market tab (index 1)
        btn1 = self.inMenuButtons[4] if self.marketOpened else self.inMenuButtons[3]
        screen.blit(btn1, (self.inScreenButtonX, y0 + y_offs[1]))

        # Automation tab (index 2) – placeholder toggle
        btn2 = self.inMenuButtons[6] if self.automationOpened else self.inMenuButtons[5]
        screen.blit(btn2, (self.inScreenButtonX, y0 + y_offs[2]))

        # Remaining (indices 3..6) use neutral tiles for now
        for i in range(3, 7):
            screen.blit(self.inMenuButtons[0], (self.inScreenButtonX, y0 + y_offs[i]))

        # Panels
        if self.resourcesOpened:
            self._draw_resources_panel()
        if self.marketOpened:
            self._draw_market_panel()

    def _draw_resources_panel(self) -> None:
        screen = self.screen
        box = self.inMenuResourcesTextBox
        screen.blit(box, (363, 182))
        # GOLD / WHEAT / COCOA
        self._blit_label(self.save[0], (363 + 60, 182 + 3 + 62))
        self._blit_label(self.save[1], (363 + 74, 182 + 64 + 62))
        self._blit_label(self.save[2], (363 + 72, 182 + 105 + 62))

    def _draw_market_panel(self) -> None:
        screen = self.screen
        box = self.inMenuBazaarTextBox
        screen.blit(box, (363, 182))

        # GOLD (display only)
        self._blit_label(self.save[0], (363 + 60, 182 + 3 + 62))

        # WHEAT (value + +/-)
        self._blit_label(self.save[1], (363 + 74, 182 + 64 + 62))
        screen.blit(self.plus, self.wheatPlusRect.topleft)
        screen.blit(self.minus, self.wheatMinusRect.topleft)

        # COCOA (value + +/-)
        self._blit_label(self.save[2], (363 + 72, 182 + 105 + 62))
        screen.blit(self.plus, self.cocoaPlusRect.topleft)
        screen.blit(self.minus, self.cocoaMinusRect.topleft)

    # ---------- main update/draw ----------
    def update(self, dt: float) -> None:
        # Auto-harvest for automated farms
        for fm in self.cocoaFarmList:
            if fm.auto == 1 and fm.update >= 100:
                fm.rewardUpdate();
                fm.update = 0
        for fm in self.wheatFarmList:
            if fm.auto == 1 and fm.update >= 100:
                fm.rewardUpdate();
                fm.update = 0
        self._update_toasts(dt)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit();
                sys.exit()

            if event.type == pg.MOUSEBUTTONUP:
                pos = self._mouse_pos()
                self.selectedTile = None
                self.selectedButton = None

                # Tile pick (if menu closed)
                if not self.menuActive:
                    for idx, r in enumerate(self.tile_rects):
                        if r.collidepoint(pos):
                            self.selectedTile = idx
                            break

                # Tool buttons (row of 8 x 2)
                if not self.menuActive:
                    btn = next((i for i, (x, y) in enumerate(zip(self.button_positions, self.button_y_positions))
                                if pg.Rect(x, y, 126, 83).collidepoint(pos)), None)
                    if btn is not None:
                        self.selectedButton = btn
                        if btn == 15:  # menu button is index 15 (bottom-right)
                            self._handle_tool_button(btn)
                            continue  # <<< do NOT process the rest of this click
                        self._handle_tool_button(btn)

                    # In-game menu buttons
                    if self.menuActive:
                        idx = next((i for i, r in enumerate(self.menu_button_rects) if r.collidepoint(pos)), None)
                        if idx is not None:
                            self._handle_menu_tab(idx)
                        else:
                            if clicked_outside_menu(pos, self.menu_rect):
                                self.menuActive = False

                    # Bazaar +/- clicks
                    if self.marketOpened:
                        self._handle_market_clicks(pos)

                # Tile actions (build/plant/harvest/demo/automation)
                if self.selectedTile is not None:
                    self._handle_tile_action(self.selectedTile)

    def draw(self) -> None:
        """
        Frame render:
          1) draw base tiles from mapData
          2) draw farms (with growth stages)
          3) draw HUD overlay
          4) draw in-game menu (Resources/Market) if open
          5) draw floating message (errors/tips)
          6) draw tool buttons (with toggled visuals)
        NOTE: This renders to the logical canvas if S.SCALE_TO_WINDOW is True.
        """
        # --- pick target surface (logical canvas or the real screen) ---
        canvas = self.logical if getattr(self, "logical", None) else self.screen
        canvas.fill(S.BLACK)

        # ---------- 1) BASE TILES ----------
        # Show locked / unlocked / established for each cell.
        # If the code is a farm (3/4), draw established as the base and the farm sprite on top.
        idx = 0
        for r in range(4):
            row = self.mapData[r]
            for c in range(8):
                x, y = self.tile_positions[idx]
                code = int(row[c])
                if code == 0:
                    base = self.lockedLand
                elif code == 1:
                    base = self.unlockedLand
                else:
                    # 2 (established), 3 (cocoa farm), 4 (wheat farm) use established as base
                    base = self.establishedLand
                canvas.blit(base, (x, y))
                idx += 1

        # ---------- 2) FARMS (growth + sprite) ----------
        # upgrade growth and render current stage
        for fm in self.cocoaFarmList:
            fm.upgrade()
            fm.displayFarm(canvas, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)
        for fm in self.wheatFarmList:
            fm.upgrade()
            fm.displayFarm(canvas, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)

        # ---------- 3) HUD OVERLAY ----------
        canvas.blit(self.HUD, (0, 0))

        # ---------- 4) IN-GAME MENU ----------
        if self.menuActive:
            # bottom-right anchor for the menu panel
            menu = self.menu_img
            menu_w, menu_h = menu.get_size()
            x0 = canvas.get_width() - int(1.25 * menu_w)
            y0 = canvas.get_height() - int(1.25 * menu_h)
            canvas.blit(menu, (x0, y0))

            # 7 stacked buttons (first 3 are tabs)
            y_offs = [71, 131, 191, 251, 311, 371, 431]

            # Resources tab
            btn0 = self.inMenuButtons[2] if self.resourcesOpened else self.inMenuButtons[1]
            canvas.blit(btn0, (self.inScreenButtonX, y0 + y_offs[0]))

            # Market tab
            btn1 = self.inMenuButtons[4] if self.marketOpened else self.inMenuButtons[3]
            canvas.blit(btn1, (self.inScreenButtonX, y0 + y_offs[1]))

            # Automation tab (toggle look only; panel optional)
            btn2 = self.inMenuButtons[6] if self.automationOpened else self.inMenuButtons[5]
            canvas.blit(btn2, (self.inScreenButtonX, y0 + y_offs[2]))

            # Remaining filler tiles
            for i in range(3, 7):
                canvas.blit(self.inMenuButtons[0], (self.inScreenButtonX, y0 + y_offs[i]))

            # Panels
            if self.resourcesOpened:
                # Resources panel box
                box_pos = (363, 182)
                canvas.blit(self.inMenuResourcesTextBox, box_pos)
                # GOLD / WHEAT / COCOA labels
                #   save[0] gold, save[1] wheat, save[2] cocoa
                gold_pos = (363 + 60, 182 + 3 + 62)
                wheat_pos = (363 + 74, 182 + 64 + 62)
                cocoa_pos = (363 + 72, 182 + 105 + 62)
                canvas.blit(self.font.render(str(self.save[0]), True, (199, 178, 153)), gold_pos)
                canvas.blit(self.font.render(str(self.save[1]), True, (199, 178, 153)), wheat_pos)
                canvas.blit(self.font.render(str(self.save[2]), True, (199, 178, 153)), cocoa_pos)

            if self.marketOpened:
                # Market panel box
                box_pos = (363, 182)
                canvas.blit(self.inMenuBazaarTextBox, box_pos)

                # GOLD display
                gold_pos = (363 + 60, 182 + 3 + 62)
                canvas.blit(self.font.render(str(self.save[0]), True, (199, 178, 153)), gold_pos)

                # WHEAT value + +/- buttons
                wheat_pos = (363 + 74, 182 + 64 + 62)
                canvas.blit(self.font.render(str(self.save[1]), True, (199, 178, 153)), wheat_pos)
                canvas.blit(self.plus, self.wheatPlusRect.topleft)
                canvas.blit(self.minus, self.wheatMinusRect.topleft)

                # COCOA value + +/- buttons
                cocoa_pos = (363 + 72, 182 + 105 + 62)
                canvas.blit(self.font.render(str(self.save[2]), True, (199, 178, 153)), cocoa_pos)
                canvas.blit(self.plus, self.cocoaPlusRect.topleft)
                canvas.blit(self.minus, self.cocoaMinusRect.topleft)

        # Toasts (stacked/fading)
        self._draw_toasts(canvas)

        # ---------- 6) TOOL BUTTONS (draw last, above HUD) ----------
        self._update_button_visuals()
        for row_idx, row in enumerate(self.buttonData):
            for col_idx, code in enumerate(row):
                img = self.buttonTypes[code]
                i = row_idx * 8 + col_idx
                x = self.button_positions[i]
                y = self.button_y_positions[i]
                canvas.blit(img, (x, y))

    # ---------- helpers: visuals ----------
    def _update_button_visuals(self) -> None:
        """Flip button sprites based on the active tool."""
        # Row 0: [harvest, build, demo, automation, ?, ?, ?, ?]
        # Row 1: [cocoa, wheat, ?, ?, ?, ?, ?, menu?]
        # Harvest/farming
        self.buttonData[0][0] = 4 if self.toolActive == "farming" else 2
        # Building
        self.buttonData[0][1] = 5 if self.toolActive == "building" else 3
        # Demo
        self.buttonData[0][2] = 11 if self.toolActive == "demo" else 10
        # Automation
        self.buttonData[0][3] = 13 if self.toolActive == "automation" else 12
        # Cocoa seeds
        self.buttonData[1][0] = 9 if self.toolActive == "cocoaSeeds" else 8
        # Wheat seeds
        self.buttonData[1][1] = 7 if self.toolActive == "wheatSeeds" else 6

    # ---------- helpers: input ----------
    def _handle_tool_button(self, btn: int) -> None:
        """Toggle tools or open menu based on which button index was clicked."""

        def toggle(tool_name: str, attr: str):
            val = getattr(self, attr)
            # odd -> turn on; even -> turn off
            self.toolActive = tool_name if (val % 2) else None
            setattr(self, attr, val + 1)

        if btn == 0:  # harvest/farming
            toggle("farming", "farmingToolTog")
        elif btn == 1:  # building
            toggle("building", "buildingToolTog")
        elif btn == 2:  # demo
            toggle("demo", "demoTog")
        elif btn == 3:  # automation
            toggle("automation", "automationTog")
        elif btn == 8:  # cocoa seeds
            toggle("cocoaSeeds", "cocoaSeedsTog")
        elif btn == 9:  # wheat seeds
            toggle("wheatSeeds", "wheatSeedsTog")
        elif btn == 15:  # menu button (bottom-right)
            self.menuActive = (self.menuTog % 2 == 0)
            self.menuTog += 1

    def _handle_menu_tab(self, idx: int) -> None:
        """Switch between Resources / Market / Automation."""
        if idx == 0:  # Resources
            self.resourcesOpened = not self.resourcesOpened
            self.marketOpened = False
            self.automationOpened = False
        elif idx == 1:  # Market
            self.marketOpened = not self.marketOpened
            self.resourcesOpened = False
            self.automationOpened = False
        elif idx == 2:  # Automation
            self.automationOpened = not self.automationOpened
            self.resourcesOpened = False
            self.marketOpened = False

    def _handle_market_clicks(self, pos: tuple[int, int]) -> None:
        """Buy/sell wheat & cocoa using +/- in the Market tab."""
        # Costs (match your old values)
        wheatGoldCost, wheatCocoaCost = 15, 5
        wheatSellPrice, cocoaSellPrice = 5, 3

        gold = int(self.save[0]);
        wheat = int(self.save[1]);
        cocoa = int(self.save[2])

        # Wheat +
        if self.wheatPlusRect.collidepoint(pos):
            if gold >= wheatGoldCost and cocoa >= wheatCocoaCost:
                gold -= wheatGoldCost
                wheat += 1
                cocoa -= wheatCocoaCost
                if self.coinCollectSound: self.coinCollectSound.play()
            else:
                self.toast(f"Need {wheatGoldCost} gold + {wheatCocoaCost} cocoa "
                           f"(have {gold}g / {cocoa}c) to buy wheat.", kind="error")

        # Wheat -
        if self.wheatMinusRect.collidepoint(pos):
            if wheat >= 1:
                wheat -= 1
                gold += wheatSellPrice
                if self.coinCollectSound: self.coinCollectSound.play()

        # Cocoa +
        if self.cocoaPlusRect.collidepoint(pos):
            # (No cocoa+ purchase specified in your design; omit or add rules here)
            pass
        # Cocoa -
        if self.cocoaMinusRect.collidepoint(pos):
            if cocoa >= 1:
                cocoa -= 1
                gold += cocoaSellPrice
                pg.mixer.Sound.play(self.coinCollectSound)

        self.save[0], self.save[1], self.save[2] = str(gold), str(wheat), str(cocoa)
        self._persist_save()

    # ---------- helpers: tile actions ----------
    def _neighbors(self, idx: int) -> list[int]:
        r, c = divmod(idx, 8)
        ns = []
        if r > 0: ns.append((r - 1) * 8 + c)
        if c < 7: ns.append(r * 8 + (c + 1))
        if r < 3: ns.append((r + 1) * 8 + c)
        if c > 0: ns.append(r * 8 + (c - 1))
        return ns

    def _set_map_code(self, row: int, col: int, new_code: int) -> None:
        s = self.mapData[row]
        self.mapData[row] = s[:col] + str(new_code) + s[col + 1:]

    def _set_auto_flag(self, row: int, col: int, value: int) -> None:
        s = self.autoData[row]
        self.autoData[row] = s[:col] + str(value) + s[col + 1:]

    def _handle_tile_action(self, tile_idx: int) -> None:
        """Do build/plant/harvest/demo/automation based on active tool."""
        r, c = divmod(tile_idx, 8)
        code = int(self.mapData[r][c])

        # Prices (same as your originals)
        unlockLandUpgrade, establishLandUpgrade = 50, 100
        cocoaFarmUpgradeGoldCost, cocoaFarmUpgradeCocoaCost = 100, 15
        wheatFarmUpgradeGoldCost, wheatFarmUpgradeWheatCost = 300, 15
        automationCocoaFarmGoldCost, automationCocoaFarmCocoaCost = 750, 250
        automationWheatFarmGoldCost, automationWheatFarmWheatCost = 300, 100

        gold = int(self.save[0]);
        wheat = int(self.save[1]);
        cocoa = int(self.save[2])

        # Neighbor check: allow unlocking only if any neighbor is >0
        neighbor_has_land = any(int(self.mapData[nr][nc]) > 0
                                for n in self._neighbors(tile_idx)
                                for nr, nc in [(n // 8, n % 8)])

        # BUILD
        if self.toolActive == "building" and neighbor_has_land:
            if code == 0 and gold >= unlockLandUpgrade:
                self._set_map_code(r, c, 1)
                gold -= unlockLandUpgrade
                pg.mixer.Sound.play(self.buildSound[random.randrange(4)])
            elif code == 1 and gold >= establishLandUpgrade:
                self._set_map_code(r, c, 2)
                gold -= establishLandUpgrade
                pg.mixer.Sound.play(self.buildSound[random.randrange(4)])

        # PLANT COCOA
        elif self.toolActive == "cocoaSeeds":
            if code == 2 and gold >= cocoaFarmUpgradeGoldCost and cocoa >= cocoaFarmUpgradeCocoaCost:
                self._set_map_code(r, c, 3)
                gold -= cocoaFarmUpgradeGoldCost
                cocoa -= cocoaFarmUpgradeCocoaCost

                fm = farm(self)
                fm.farmType = 3
                fm.location = (r, c)
                fm.tileLocation = tile_idx  # <-- use the index passed into this handler
                self.cocoaFarmList.append(fm)
                self._set_auto_flag(r, c, 0)  # new farms start non-automated

                if self.plantSound:  # play sound if mixer/asset loaded
                    pg.mixer.Sound.play(self.plantSound[random.randrange(len(self.plantSound))])
            else:
                need_g, need_c = cocoaFarmUpgradeGoldCost, cocoaFarmUpgradeCocoaCost
                self.toast(f"Plant cocoa: need {need_g} gold + {need_c} cocoa on established land "
                           f"(have {gold}g / {cocoa}c).", kind="error")

        # PLANT WHEAT
        elif self.toolActive == "wheatSeeds":
            if code == 2 and gold >= wheatFarmUpgradeGoldCost and wheat >= wheatFarmUpgradeWheatCost:
                self._set_map_code(r, c, 4)
                gold -= wheatFarmUpgradeGoldCost
                wheat -= wheatFarmUpgradeWheatCost

                fm = farm(self)
                fm.farmType = 4
                fm.location = (r, c)
                fm.tileLocation = tile_idx
                self.wheatFarmList.append(fm)
                self._set_auto_flag(r, c, 0)

                if self.plantSound:
                    pg.mixer.Sound.play(self.plantSound[random.randrange(len(self.plantSound))])
            else:
                need_g, need_w = wheatFarmUpgradeGoldCost, wheatFarmUpgradeWheatCost
                self.toast(f"Plant wheat: need {need_g} gold + {need_w} wheat on established land "
                           f"(have {gold}g / {wheat}w).", kind="error")

        # HARVEST (also happens on click if using farming tool)
        elif self.toolActive == "farming":
            # cocoa
            for fm in self.cocoaFarmList:
                if fm.tileLocation == tile_idx and fm.update >= 100:
                    fm.rewardUpdate();
                    fm.update = 0
            # wheat
            for fm in self.wheatFarmList:
                if fm.tileLocation == tile_idx and fm.update >= 100:
                    fm.rewardUpdate();
                    fm.update = 0

        # DEMOLISH
        elif self.toolActive == "demo":
            if code in (3, 4):
                self._set_map_code(r, c, 1)
                if code == 3:  # cocoa
                    self.cocoaFarmList[:] = [fm for fm in self.cocoaFarmList if fm.tileLocation != tile_idx]
                else:  # wheat
                    self.wheatFarmList[:] = [fm for fm in self.wheatFarmList if fm.tileLocation != tile_idx]

        # AUTOMATION
        elif self.toolActive == "automation":
            if code == 3:  # cocoa
                if gold >= automationCocoaFarmGoldCost and cocoa >= automationCocoaFarmCocoaCost:
                    gold -= automationCocoaFarmGoldCost
                    cocoa -= automationCocoaFarmCocoaCost
                    for fm in self.cocoaFarmList:
                        if fm.tileLocation == tile_idx:
                            fm.auto = 1
                    self._set_auto_flag(r, c, 1)
                else:
                    need_g, need_c = automationCocoaFarmGoldCost, automationCocoaFarmCocoaCost
                    self.toast(f"Automate cocoa: need {need_g} gold + {need_c} cocoa "
                               f"(have {gold}g / {cocoa}c).", kind="error")
            elif code == 4:  # wheat
                if gold >= automationWheatFarmGoldCost and wheat >= automationWheatFarmWheatCost:
                    gold -= automationWheatFarmGoldCost
                    wheat -= automationWheatFarmWheatCost
                    for fm in self.wheatFarmList:
                        if fm.tileLocation == tile_idx:
                            fm.auto = 1
                    self._set_auto_flag(r, c, 1)
                else:
                    need_g, need_w = automationWheatFarmGoldCost, automationWheatFarmWheatCost
                    self.toast(f"Automate wheat: need {need_g} gold + {need_w} wheat "
                               f"(have {gold}g / {wheat}w).", kind="error")

        # write back updated resources and persist
        self.save[0], self.save[1], self.save[2] = str(gold), str(wheat), str(cocoa)
        self._persist_save()

    def _persist_save(self) -> None:
        """Write head(4) + mapData(4) + autoData(4) back to disk, update RAM copy."""
        head = self.save[:4]
        new = head[:] + self.mapData[:4] + self.autoData[:4]
        self.save = [str(x) for x in new]
        f.lineUpdater(f.root + self.user, self.save)

    # ---------- main loop ----------
    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.update(dt)
            self.draw()
            if self.logical:
                # scale the logical canvas up to the actual window size
                scaled = pg.transform.smoothscale(self.logical, self.screen.get_size())
                self.screen.fill(S.BLACK)
                self.screen.blit(scaled, (0, 0))
            pg.display.flip()
            # end while
        pg.quit()
        sys.exit(0)


# ------------ launcher ------------
def main() -> None:
    # Ensure save directory root is set (already set at top via SAVE_DIR → f.root)
    # Initialize and run the app
    app = GameApp()
    try:
        app.run()
    finally:
        # Best-effort save on exit if a profile was loaded
        try:
            app._persist_save()
        except Exception:
            pass


if __name__ == "__main__":
    main()
