"""
Chocolate Tycoon — pygame_remade.py
Fully-wired starter that ties together:
- utils.py (login + save file format you already use)
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
import utils as f  # your existing utils.py

# ---------- constants ----------
GRID_ROWS, GRID_COLS = 4, 8
TILE_W = TILE_H = 126
SCREEN_W, SCREEN_H = 1080, 720
FPS = 60

# ---------- paths / save root ----------
ROOT_DIR = Path(__file__).parent
SAVE_DIR = ROOT_DIR / "saveFiles"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Point utils.py at this save folder (overrides the hardcoded path in utils.py)
f.root = str(SAVE_DIR) + os.sep  # e.g. ".../saveFiles/" cross-platform


class GameApp:
    def __init__(self):
        # --- init pygame ---
        pg.init()
        try:
            pg.mixer.init()
        except Exception:
            pass
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        pg.display.set_caption("Chocolate Tycoon")
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
        surf = pg.image.load(str(ROOT_DIR / "graphics" / rel)).convert_alpha()
        return pg.transform.scale(surf, size) if size else surf

    def _sfx(self, rel: str) -> pg.mixer.Sound:
        return pg.mixer.Sound(str(ROOT_DIR / "graphics" / rel))

    def _grid_positions(self, rows: int, cols: int, start=(0, 0), step=(0, 0)) -> list[tuple[int, int]]:
        sx, sy = start
        dx, dy = step
        return [(sx + c * dx, sy + r * dy) for r in range(rows) for c in range(cols)]

    def _load_images_and_sounds(self) -> None:
        self.HUD = self._img("Map Final.png", (SCREEN_W, SCREEN_H))
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
        self.menu_img = self._img("Menu.png", (int(SCREEN_W/1.5), int(SCREEN_H/1.5)))
        self.plus, self.minus = self._img("plus.png", (25, 15)), self._img("minus.png", (25, 15))
        self.inMenuButton = self._img("InMenuButton.png", (124, 38))
        self.inMenuButtonMaterials = self._img("MenuTileMaterials.png", (124, 38))
        self.inMenuButtonMaterialsToggled = self._img("MenuTileMaterialsToggled.png", (124, 38))
        self.inMenuButtonBazaar = self._img("MenuTileBazaar.png", (124, 38))
        self.inMenuButtonBazaarToggled = self._img("MenuTileBazaarToggled.png", (124, 38))
        self.inMenuButtonAutomation = self._img("MenuTileAutomation.png", (124, 38))
        self.inMenuButtonAutomationToggled = self._img("MenuTileAutomationToggled.png", (124, 38))
        self.inMenuButtons = [
            self.inMenuButton, self.inMenuButtonMaterials, self.inMenuButtonMaterialsToggled,
            self.inMenuButtonBazaar, self.inMenuButtonBazaarToggled,
            self.inMenuButtonAutomation, self.inMenuButtonAutomationToggled
        ]

        # Icons
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

        # Sounds
        self.coinCollectSound = self._sfx("sound/coincollect.wav")
        self.plantSound = [
            self._sfx("sound/plant1.ogg"),
            self._sfx("sound/plant2.ogg"),
            self._sfx("sound/plant3.ogg")
        ]
        self.buildSound = [
            self._sfx("sound/stone1.ogg"),
            self._sfx("sound/stone2.ogg"),
            self._sfx("sound/stone3.ogg"),
            self._sfx("sound/stone4.ogg")
        ]

        # Button data (from file)
        self.buttonData = []
        with open(ROOT_DIR / "graphics" / "buttondata.txt") as fh:
            for row in fh.read().splitlines():
                self.buttonData.append([int(c) for c in row])

        # Button images
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
            self.harvestButton, self.buildButton, self.harvestButtonToggled, self.buildButtonToggled,
            self.wheatButton, self.wheatButtonToggled,
            self.cocoaButton, self.cocoaButtonToggled,
            self.shovelButton, self.shovelButtonToggled,
            self.automationTool, self.automationToolToggled
        ]

        # Geometry for buttons
        self.button_positions = [8, 142, 276, 410, 544, 678, 812, 946,
                                 8, 142, 276, 410, 544, 678, 812, 946]
        self.button_y_positions = [544, 544, 544, 544, 544, 544, 544, 544,
                                   635, 635, 635, 635, 635, 635, 635, 635]

        # Build menu button rects
        menuButtonHitboxes = [
            [self.inScreenButtonX, self.screen.get_height() - 1.25 * self.menu_img.get_height() + off]
            for off in (71, 131, 191, 251, 311, 371, 431)
        ]
        self.menu_button_rects = make_menu_button_rects(self.inScreenButtonX, menuButtonHitboxes)

        # Build tile rects
        self.tile_rects = [pg.Rect(x, y, TILE_W, TILE_H) for (x, y) in self.tile_positions]

        # Coordinates for resource +/- in market
        self.wheatPlusRect = pg.Rect(500, 182 + 3 + 64 + 62, 25, 15)
        self.wheatMinusRect = pg.Rect(500 + 38, 182 + 3 + 64 + 62, 25, 15)
        self.cocoaMinusRect = pg.Rect(500 + 38, 182 + 3 + 105 + 62, 25, 15)
        self.cocoaPlusRect = pg.Rect(500, 182 + 3 + 105 + 62, 25, 15)

        # ---- UI state ----
        self.menuActive = False
        self.resourcesOpened = False
        self.marketOpened = False
        self.automationOpened = False

        self.toolActive: str | None = None
        self.selectedTile: int | None = None
        self.selectedButton: int | None = None

        # Floating message (errors, tips)
        self.display_message: str | None = None
        self.message_start_time = 0.0
        self.message_duration = 3.0
        self.message_position = (0, 0)

        # Misc togglers (keep parity with old logic)
        self.farmingToolTog = 1
        self.buildingToolTog = 1
        self.demoTog = 0
        self.automationTog = 0
        self.wheatSeedsTog = 1
        self.cocoaSeedsTog = 1
        self.menuTog = 0

        # Progress bar alias for older calls
        self.progressBars = self.progressBarTypes

    # ---------- helpers ----------
    def _flash(self, msg: str) -> None:
        self.display_message = msg
        self.message_start_time = time.time()
        self.message_position = pg.mouse.get_pos()

    def _blit_label(self, text: str, pos: tuple[int, int]) -> None:
        surf = self.font.render(str(text), True, (199, 178, 153))
        self.screen.blit(surf, pos)

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
        self._blit_label(self.save[0], (363 + 60,  182 + 3 + 62))
        self._blit_label(self.save[1], (363 + 74,  182 + 64 + 62))
        self._blit_label(self.save[2], (363 + 72,  182 + 105 + 62))

    def _draw_market_panel(self) -> None:
        screen = self.screen
        box = self.inMenuBazaarTextBox
        screen.blit(box, (363, 182))

        # GOLD (display only)
        self._blit_label(self.save[0], (363 + 60,  182 + 3 + 62))

        # WHEAT (value + +/-)
        self._blit_label(self.save[1], (363 + 74,  182 + 64 + 62))
        screen.blit(self.plus,  self.wheatPlusRect.topleft)
        screen.blit(self.minus, self.wheatMinusRect.topleft)

        # COCOA (value + +/-)
        self._blit_label(self.save[2], (363 + 72,  182 + 105 + 62))
        screen.blit(self.plus,  self.cocoaPlusRect.topleft)
        screen.blit(self.minus, self.cocoaMinusRect.topleft)

    # ---------- main update/draw ----------
    def update(self, dt: float) -> None:
        # Auto-harvest for automated farms
        for fm in self.cocoaFarmList:
            if fm.auto == 1 and fm.update >= 100:
                fm.rewardUpdate(); fm.update = 0
        for fm in self.wheatFarmList:
            if fm.auto == 1 and fm.update >= 100:
                fm.rewardUpdate(); fm.update = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit()

            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
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
                        self._handle_tool_button(btn)

                # In-game menu buttons
                if self.menuActive:
                    idx = next((i for i, r in enumerate(self.menu_button_rects) if r.collidepoint(pos)), None)
                    if idx is not None:
                        self._handle_menu_tab(idx)
                    else:
                        # click outside → close
                        if clicked_outside_menu(pos):
                            self.menuActive = False

                    # Bazaar +/- clicks
                    if self.marketOpened:
                        self._handle_market_clicks(pos)

                # Tile actions (build/plant/harvest/demo/automation)
                if self.selectedTile is not None:
                    self._handle_tile_action(self.selectedTile)

    def draw(self) -> None:
        screen = self.screen

        # Tiles (base terrain)
        idx = 0
        for row in self.mapData:
            for _ in row:
                x, y = self.tile_positions[idx]
                code = int(row[idx % len(row)])
                screen.blit(self.tileTypes[code], (x, y))
                idx += 1

        # Farms grow + render
        for fm in self.cocoaFarmList:
            fm.upgrade()
            fm.displayFarm(screen, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)
        for fm in self.wheatFarmList:
            fm.upgrade()
            fm.displayFarm(screen, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)

        # HUD overlay
        screen.blit(self.HUD, (0, 0))

        # Floating message
        if self.display_message and (time.time() - self.message_start_time) < self.message_duration:
            txt = self.font.render(self.display_message, True, (255, 0, 0))
            mx, my = self.message_position
            screen.blit(txt, (mx + 10, my + 10))
        else:
            self.display_message = None

        # In-game menu
        if self.menuActive:
            self.menu_display()
        # Buttons (draw last so they sit above the HUD)
        self._update_button_visuals()
        for row_idx, row in enumerate(self.buttonData):
            for col_idx, code in enumerate(row):
                img = self.buttonTypes[code]
                i = row_idx * 8 + col_idx
                x = self.button_positions[i]
                y = self.button_y_positions[i]
                self.screen.blit(img, (x, y))

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

        if btn == 0:          # harvest/farming
            toggle("farming", "farmingToolTog")
        elif btn == 1:        # building
            toggle("building", "buildingToolTog")
        elif btn == 2:        # demo
            toggle("demo", "demoTog")
        elif btn == 3:        # automation
            toggle("automation", "automationTog")
        elif btn == 8:        # cocoa seeds
            toggle("cocoaSeeds", "cocoaSeedsTog")
        elif btn == 9:        # wheat seeds
            toggle("wheatSeeds", "wheatSeedsTog")
        elif btn == 15:       # menu button (bottom-right)
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

        gold = int(self.save[0]); wheat = int(self.save[1]); cocoa = int(self.save[2])

        # Wheat +
        if self.wheatPlusRect.collidepoint(pos):
            if gold >= wheatGoldCost and cocoa >= wheatCocoaCost:
                gold -= wheatGoldCost
                wheat += 1
                cocoa -= wheatCocoaCost
                pg.mixer.Sound.play(self.coinCollectSound)
            else:
                self._flash("Not enough gold/cocoa to buy wheat!")
        # Wheat -
        if self.wheatMinusRect.collidepoint(pos):
            if wheat >= 1:
                wheat -= 1
                gold += wheatSellPrice
                pg.mixer.Sound.play(self.coinCollectSound)
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

        gold = int(self.save[0]); wheat = int(self.save[1]); cocoa = int(self.save[2])

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
                fm = farm(); fm.farmType = 3; fm.location = (r, c); fm.tileLocation = tile_idx
                self.cocoaFarmList.append(fm)
                pg.mixer.Sound.play(self.plantSound[random.randrange(3)])
            else:
                self._flash("Need 100 gold + 15 cocoa and established land.")

        # PLANT WHEAT
        elif self.toolActive == "wheatSeeds":
            if code == 2 and gold >= wheatFarmUpgradeGoldCost and wheat >= wheatFarmUpgradeWheatCost:
                self._set_map_code(r, c, 4)
                gold -= wheatFarmUpgradeGoldCost
                wheat -= wheatFarmUpgradeWheatCost
                fm = farm(); fm.farmType = 4; fm.location = (r, c); fm.tileLocation = tile_idx
                self.wheatFarmList.append(fm)
                pg.mixer.Sound.play(self.plantSound[random.randrange(3)])
            else:
                self._flash("Need 300 gold + 15 wheat and established land.")

        # HARVEST (also happens on click if using farming tool)
        elif self.toolActive == "farming":
            # cocoa
            for fm in self.cocoaFarmList:
                if fm.tileLocation == tile_idx and fm.update >= 100:
                    fm.rewardUpdate(); fm.update = 0
            # wheat
            for fm in self.wheatFarmList:
                if fm.tileLocation == tile_idx and fm.update >= 100:
                    fm.rewardUpdate(); fm.update = 0

        # DEMOLISH
        elif self.toolActive == "demo":
            if code in (3, 4):
                self._set_map_code(r, c, 1)
                if code == 3:  # cocoa
                    self.cocoaFarmList[:] = [fm for fm in self.cocoaFarmList if fm.tileLocation != tile_idx]
                else:          # wheat
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
                    self._flash(f"Need {automationCocoaFarmGoldCost} gold + {automationCocoaFarmCocoaCost} cocoa.")
            elif code == 4:  # wheat
                if gold >= automationWheatFarmGoldCost and wheat >= automationWheatFarmWheatCost:
                    gold -= automationWheatFarmGoldCost
                    wheat -= automationWheatFarmWheatCost
                    for fm in self.wheatFarmList:
                        if fm.tileLocation == tile_idx:
                            fm.auto = 1
                    self._set_auto_flag(r, c, 1)
                else:
                    self._flash(f"Need {automationWheatFarmGoldCost} gold + {automationWheatFarmWheatCost} wheat.")

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
