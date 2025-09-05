"""
Notes:

currently:
    - working on automation
        - for some odd reason the resources variable is empty unless the menu is opened? if opened it is fixed for rest
            of game
        - graphic for automation


- Automation tool (DONE BABY)
- mapdata needs to be profile-specific, not universal (FUCK YES I DID IT)
- put shit into other sections of menu
- Sound effect for things with variations
    - Upgrading land
    - Different tiers of sounds
- Tutorial
- Seed economy
    - Buy handfuls of seeds (5?) for coins and lower tier seeds (i.e. 5 wheat seeds cost 15 cocoa seeds and 20 coins)
- Adaptable menu
- Droughts, fires, natural disasters
- Animal / Kshtimi raid where after a random interval of time they spawn, if you don't kill them they will cause
    - a plague similar to the black death
    `- hire a farmer to save your crops / patrol them
- Loading animation for crops is them progressing, not just a bar
- Water plants
- Tips at beginning of game
- Not using cover crops leads to bad harvest, using them leads to some early extra good harvests
- Taxes
- Var "root" needs to be created based on players directory every time the game is launched
- Farm tiles should have 3 tiers of variety, rng roll to see which is displayed for less redundancies
- Sell list needs to be based off inventory
    - (

        if user has wheat, display wheat

        need to make a list with coords to display each material

        )

- Tiers of crops
    - Low tier crops (i.e. chili peppers, broccoli, onions, potatoes, carrots)
    - Mid tier crops (i.e. tomatoes, wheat, cabbage, cotton, )
    - High tier crops (i.e grapes, flowers, wild berries ( art should have strawberries, blueberries, blackberries, )
    - Lucrative tier crops (i.e cannabis (see note below), coca plant, peyote, mushrooms)

    cannabis - should you have to either get a license and sell for less or take the risk of farming illegally,
    making more money and now having to hav ea license and pay taxes on it?


map.txt template
32000000
21000000
10000000
00000000

idea 12.18.24: maybe a 2x2 of a farm type increases efficiency and turns it into a plantation?
"""
# Imports
import sys
import time
import pygame
from pygame.locals import *
import utils as f
import itertools
import random
import os

# ---------- Menu helpers (no changes to existing funcs) ----------
import pygame as pg


def make_menu_button_rects(inScreenButtonX: int, menuButtonHitboxes: list[list[int]]) -> list[pg.Rect]:
    """Build 7 menu button rects aligned with your existing hitbox Ys. Size = 124x38."""
    return [pg.Rect(inScreenButtonX, y, 124, 38) for (_, y) in menuButtonHitboxes]


def menu_pick(rects: list[pg.Rect], pos: tuple[int, int]) -> int | None:
    """Return clicked menu index or None."""
    for i, r in enumerate(rects):
        if r.collidepoint(pos):
            return i
    return None


def menu_bounds_rect() -> pg.Rect:
    """Your current visible menu bounds (from old logic)."""
    return pg.Rect(180, 120, 900 - 180, 600 - 120)


def clicked_outside_menu(pos: tuple[int, int]) -> bool:
    """True if click is outside the menu panel."""
    return not menu_bounds_rect().collidepoint(pos)


def toggle_tabs(resourcesOpened: bool, marketOpened: bool, automationOpened: bool, clicked_idx: int
                ) -> tuple[bool, bool, bool]:
    """
    Pure toggle logic that mirrors what you do now, but side-effect free.
    Returns the new (resourcesOpened, marketOpened, automationOpened).
    """
    if clicked_idx == 0:  # Resources tab
        resourcesOpened = not resourcesOpened
        marketOpened = False
        automationOpened = False
    elif clicked_idx == 1:  # Market tab
        marketOpened = not marketOpened
        resourcesOpened = False
        automationOpened = False
    elif clicked_idx == 2:  # (future) Automation tab
        automationOpened = not automationOpened
        resourcesOpened = False
        marketOpened = False
    return resourcesOpened, marketOpened, automationOpened


# Colors
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]

# Global Variables
gameName = "TYCOON"
# root = ''.join([char + '\\' if char == '\\' else char for char in os.getcwd()]) + "\\\\saveFiles\\\\"
root = os.path.dirname(os.path.realpath(__file__)) + "\\saveFiles\\"
userName = f.logIn()
if not userName:
    print("Created new account.")
    time.sleep(3)
    exit("Created new account.")

cocoaMinusCoordinates = (538, 352)
wheatMinusCoordinates = (538, 311)
wheatPlusCoordinates = (500, 311)
goldMinusCoordinates = (538, 247)
cocoaPlusCoordinates = (500, 352)
goldPlusCoordinates = (500, 247)

automationOpened = False
tempShapeToggler = False
resourcesOpened = False
demoToggler = False
marketOpened = False
menuActive = False
cocoaEmpty = False
srm = False

selectedMenuButton = None
selectedButton = None
selectedTile = None
toolActive = None
display_message = ""
message_start_time = 0
message_duration = 3  # Message stays on screen for 3 seconds
message_position = (0, 0)  # Position where the message should appear

buildingToolTog = 1
cocoaFullInt = 100  # maybe put this in the class
wheatFullInt = 100  # maybe put this in the class
farmingToolTog = 1
wheatSeedsTog = 1
cocoaSeedsTog = 1
automationTog = 0
resourcesTog = 0
demoTog = 0
marketTog = 0
menuTog = 0

saveInformation = []
cocoaFarmList = []
wheatFarmList = []
tileList = []
autoData = []


class land:
    def __init__(self):
        self.farmType = None
        self.neighbors = []
        self.tileLocation = 0  # 0, 1, 2, etc...
        self.location = 0, 0  # x, y
        self.update = 0  # int corresponding to the progress till the farm is harvestable
        self.reward = 5  # how much the player is rewarded for harvesting the farm
        self.rate = 1  # how fast the farm is growing
        self.auto = 0

    def makeNeighbors(self):
        tileIsNotOnTopBorder = True
        tileIsNotOnLeftBorder = True

        if self.tileLocation < 8:
            tileIsNotOnTopBorder = False
        if self.tileLocation == 0 or self.tileLocation == 8 or self.tileLocation == 16 or self.tileLocation == 24:
            tileIsNotOnLeftBorder = False
        if tileIsNotOnLeftBorder and tileIsNotOnTopBorder:
            self.neighbors = [self.tileLocation - 8, self.tileLocation + 1,
                              self.tileLocation + 8, self.tileLocation - 1]
        elif not tileIsNotOnTopBorder:  # this runs if tileLocation is on the top border
            self.neighbors = [None, self.tileLocation + 1,
                              self.tileLocation + 8, self.tileLocation - 1]
        elif not tileIsNotOnLeftBorder:  # this runs if tileLocation is on the left border
            self.neighbors = [self.tileLocation - 8, self.tileLocation + 1,
                              self.tileLocation + 8, None]


class farm(land):
    # the following two functions can be altered in a way to change the value or speed of which the player can gain
    #  rewards from the given farm
    def upgrade(self):  # this function continuously refreshes and adds up the self.update variable at the self.rate
        if self.farmType == 4 or self.farmType == "4":
            if self.update < wheatFullInt:
                self.update += self.rate
        elif self.farmType == 3 or self.farmType == "3":
            if self.update < cocoaFullInt:
                self.update += self.rate

    def rewardUpdate(self):  # this function adds the given rewards to the player
        if self.farmType == 3 or self.farmType == "3":  # cocoa
            saveInformation[2] = int(saveInformation[2]) + self.reward  # self.reward = 5
        elif self.farmType == 4 or self.farmType == "4":  # wheat
            saveInformation[1] = int(saveInformation[1]) + self.reward
        f.lineUpdater(root + userName, saveInformation)

    def displayFarm(self, screen, iconTypes, iconPos, progressBarTypes, wheatStages, cocoaStages):
        if self.farmType == 3:  # cocoa
            if self.update < cocoaFullInt / 3:
                stage = 0
            elif cocoaFullInt / 3 <= self.update < 2 * (cocoaFullInt / 3):
                stage = 1
            else:
                stage = 2
            screen.blit(cocoaStages[stage], iconPos[self.location[0]][self.location[1]])
        elif self.farmType == 4:  # wheat
            if self.update < wheatFullInt / 3:
                stage = 0
            elif wheatFullInt / 3 <= self.update < 2 * (wheatFullInt / 3):
                stage = 1
            else:
                stage = 2
            screen.blit(wheatStages[stage], iconPos[self.location[0]][self.location[1]])


'''

from dataclasses import dataclass
from typing import Optional, Tuple, List

GRID_ROWS, GRID_COLS = 4, 8

@dataclass(slots=True)
class Land:
    farmType: Optional[int] = None
    tileLocation: int = 0
    location: Tuple[int, int] = (0, 0)
    update: int = 0
    reward: int = 5
    rate: int = 1
    auto: int = 0
    neighbors: List[Optional[int]] = None

    def __post_init__(self):
        if self.neighbors is None:
            self.makeNeighbors()

    def makeNeighbors(self) -> None:
        r, c = divmod(self.tileLocation, GRID_COLS)
        def idx(rc): return rc[0]*GRID_COLS + rc[1] if rc else None
        self.neighbors = [
            idx((r-1, c)) if r > 0 else None,
            idx((r, c+1)) if c < GRID_COLS-1 else None,
            idx((r+1, c)) if r < GRID_ROWS-1 else None,
            idx((r, c-1)) if c > 0 else None,
        ]


class Farm(Land):
    def full_amount(self) -> int:
        ft = self.farmType
        if ft == 3: return cocoaFullInt
        if ft == 4: return wheatFullInt
        return 0

    def upgrade(self, dt: float = 0.0) -> None:
        """Optionally scale by dt later: self.rate * dt."""
        full = self.full_amount()
        if full > 0 and self.update < full:
            self.update = min(self.update + self.rate, full)

    def harvest(self) -> dict:
        """No globals: return a dict of resource deltas; caller applies & saves."""
        if self.farmType == 3 and self.update >= cocoaFullInt:
            self.update = 0
            return {"cocoa": self.reward}
        if self.farmType == 4 and self.update >= wheatFullInt:
            self.update = 0
            return {"wheat": self.reward}
        return {}

    def stage_index(self) -> int:
        full = self.full_amount()
        if full <= 0: return 0
        t = self.update / full
        return 0 if t < 1/3 else (1 if t < 2/3 else 2)

    def draw(self, screen, iconPos, wheatStages, cocoaStages) -> None:
        r, c = self.location
        if self.farmType == 3:
            screen.blit(cocoaStages[self.stage_index()], iconPos[r][c])
        elif self.farmType == 4:
            screen.blit(wheatStages[self.stage_index()], iconPos[r][c])


def menu_display(self) -> None:
    """Pure render: draw the in-game menu based on current state flags."""
    screen = self.screen
    menu = self.menu_img
    x0 = screen.get_width() - int(1.25 * menu.get_width())
    y0 = screen.get_height() - int(1.25 * menu.get_height())
    screen.blit(menu, (x0, y0))

    # Buttons down the right side (7 slots)
    y_offs = [71, 131, 191, 251, 311, 371, 431]
    # inMenuButtons = [inMenuButton, Materials, MaterialsToggled, Bazaar, BazaarToggled, Automation, AutomationToggled]
    # Top tab: Resources (materials)
    btn0 = self.inMenuButtons[2] if self.resourcesOpened else self.inMenuButtons[1]
    screen.blit(btn0, (self.inScreenButtonX, y0 + y_offs[0]))
    # Tab 2 label (we’re using Bazaar instead of Automation per your comment)
    screen.blit(self.inMenuButtons[0], (self.inScreenButtonX, y0 + y_offs[1]))
    # Tabs 3..7 (placeholders)
    for i in range(2, 7):
        screen.blit(self.inMenuButtons[0], (self.inScreenButtonX, y0 + y_offs[i]))

    # Panels
    if self.resourcesOpened:
        self._draw_resources_panel()
    if self.marketOpened:
        self._draw_market_panel()


def handle_menu_click(self, index: int) -> None:
    """Flip tabs when a menu button is clicked (called from update())."""
    if index == 0:  # Resources
        self.resourcesOpened = not self.resourcesOpened
        self.marketOpened = False
        self.automationOpened = False
    elif index == 1:  # Market
        self.marketOpened = not self.marketOpened
        self.resourcesOpened = False
        self.automationOpened = False
    elif index == 2:  # (future) Automation
        self.automationOpened = not self.automationOpened
        self.marketOpened = False
        self.resourcesOpened = False
    # else: other slots currently do nothing


def _draw_resources_panel(self) -> None:
    """Left-side resources readout (no +/-)."""
    screen = self.screen
    box = self.inMenuResourcesTextBox
    screen.blit(box, (363, 182))
    # GOLD / WHEAT / COCOA
    self._blit_label(str(self.save[0]), (363 + 60, 182 + 3 + 62))
    self._blit_label(str(self.save[1]), (363 + 74, 182 + 64 + 62))
    self._blit_label(str(self.save[2]), (363 + 72, 182 + 105 + 62))


def _draw_market_panel(self) -> None:
    """Market readout with +/- for wheat and cocoa."""
    screen = self.screen
    box = self.inMenuResourcesTextBox  # same art used
    screen.blit(box, (363, 182))

    # GOLD (display only)
    self._blit_label(str(self.save[0]), (363 + 60, 182 + 3 + 62))

    # WHEAT (value + +/-)
    self._blit_label(str(self.save[1]), (363 + 74, 182 + 64 + 62))
    screen.blit(self.plus, (500, 182 + 3 + 64 + 62))
    screen.blit(self.minus, (500 + 38, 182 + 3 + 64 + 62))

    # COCOA (value + +/-)
    self._blit_label(str(self.save[2]), (363 + 72, 182 + 105 + 62))
    screen.blit(self.plus, (500, 182 + 3 + 105 + 62))
    screen.blit(self.minus, (500 + 38, 182 + 3 + 105 + 62))


def _blit_label(self, text: str, pos: tuple[int, int]) -> None:
    surf = self.font.render(text, False, (199, 178, 153))
    self.screen.blit(surf, pos)


def update(self, dt: float) -> None:
    # ---- one-time automation tick for farms ----
    for fm in self.cocoaFarmList:
        if fm.auto == 1 and fm.update == cocoaFullInt:
            fm.rewardUpdate(); fm.update = 0
    for fm in self.wheatFarmList:
        if fm.auto == 1 and fm.update == wheatFullInt:
            fm.rewardUpdate(); fm.update = 0

    # ---- event handling ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            # re-read save if that’s your intended design
            self.save = f.lineGrabber(str(self.root / self.user_name))

            pos = pygame.mouse.get_pos()
            self.selectedMenuButton = None
            self.selectedTile = None
            self.selectedButton = None

            # ---------- TILE PICK (replaces 32 if-elif blocks) ----------
            # self.tile_rects should be list[pygame.Rect] aligned to tile indices 0..31
            for idx, r in enumerate(self.tile_rects):
                if r.collidepoint(pos) and not self.menuActive:
                    self.selectedTile = idx
                    break

            # costs (kept as your values)
            wheatGoldCost, wheatCocoaCost = 15, 5
            wheatSellPrice, cocoaSellPrice = 5, 3
            unlockLandUpgrade, establishLandUpgrade = 50, 100
            cocoaFarmUpgradeGoldCost, cocoaFarmUpgradeCocoaCost = 100, 15
            wheatFarmUpgradeGoldCost, wheatFarmUpgradeWheatCost = 300, 15
            automationCocoaFarmGoldCost, automationCocoaFarmCocoaCost = 750, 250
            automationWheatFarmGoldCost, automationWheatFarmWheatCost = 300, 100

            # ---------- TOOL BUTTONS ----------
            # Build button rects once in setup: self.button_rects aligned to index 0..15
            # Map indices to actions/toggles
            def toggle(tool, toggler_attr):
                val = getattr(self, toggler_attr)
                self.toolActive = tool if (val % 2) else None
                setattr(self, toggler_attr, val + 1)

            btn_clicked = next((i for i, r in enumerate(self.button_rects) if r.collidepoint(pos)), None)
            if btn_clicked is not None and not self.menuActive:
                self.selectedButton = btn_clicked
                if btn_clicked == 0:        # farming
                    toggle("farming", "farmingToolTog")
                elif btn_clicked == 1:      # building
                    toggle("building", "buildingToolTog")
                elif btn_clicked == 2:      # demo
                    toggle("demo", "demoTog")
                elif btn_clicked == 3:      # automation
                    toggle("automation", "automationTog")
                elif btn_clicked == 8:      # cocoa seeds
                    toggle("cocoaSeeds", "cocoaSeedsTog")
                elif btn_clicked == 9:      # wheat seeds
                    toggle("wheatSeeds", "wheatSeedsTog")
                elif btn_clicked == 15:     # menu button (always works)
                    self.menuActive = (self.menuTog % 2 == 0)
                    self.menuTog += 1

            # ---------- MENU BUTTONS + CLICK-OUTSIDE TO CLOSE ----------
            if self.menuActive:
                # self.menu_button_rects should be 7 buttons stacked vertically at x = self.inScreenButtonX
                clicked_idx = next((i for i, r in enumerate(self.menu_button_rects) if r.collidepoint(pos)), None)
                if clicked_idx is not None:
                    self.selectedMenuButton = clicked_idx
                else:
                    # click outside menu: hard-coded bounds from old code (180..900, 120..600)
                    mx, my = pos
                    if (mx < 180 or mx > 900) or (my < 120 or my > 600):
                        self.menuActive = False

                # resources +/- (market)
                if self.marketOpened:
                    # wheat +/-
                    if self.wheatPlusRect.collidepoint(pos):
                        if int(self.save[0]) >= wheatGoldCost and int(self.save[2]) >= wheatCocoaCost:
                            self.save[0] = int(self.save[0]) - wheatGoldCost
                            self.save[1] = int(self.save[1]) + 1
                            self.save[2] = int(self.save[2]) - wheatCocoaCost
                            pygame.mixer.Sound.play(self.coinCollectSound)
                    if self.wheatMinusRect.collidepoint(pos) and int(self.save[1]) >= 1:
                        self.save[1] = int(self.save[1]) - 1
                        self.save[0] = int(self.save[0]) + wheatSellPrice
                        pygame.mixer.Sound.play(self.coinCollectSound)
                    # cocoa -
                    if self.cocoaMinusRect.collidepoint(pos) and int(self.save[2]) >= 1:
                        self.save[2] = int(self.save[2]) - 1
                        self.save[0] = int(self.save[0]) + cocoaSellPrice
                        pygame.mixer.Sound.play(self.coinCollectSound)

            # ---------- HARVEST ----------
            if self.selectedTile is not None and self.toolActive == "farming":
                for fm in self.cocoaFarmList:
                    if fm.tileLocation == self.selectedTile and fm.update == cocoaFullInt:
                        fm.rewardUpdate(); fm.update = 0
                for fm in self.wheatFarmList:
                    if fm.tileLocation == self.selectedTile and fm.update == wheatFullInt:
                        fm.rewardUpdate(); fm.update = 0

            # ---------- BUILD/PLANT/DEMO/AUTOMATE ----------
            if self.selectedTile is not None:
                r, c = divmod(self.selectedTile, 8)  # 4x8 grid
                code = int(self.mapData[r][c])

                # neighbor check to allow unlocking
                totalNeighbors = []
                for t in self.tileList:
                    if int(t.farmType) > 0:
                        totalNeighbors.extend(t.neighbors)

                def set_map_code(row, col, new_code):
                    s = self.mapData[row]
                    self.mapData[row] = s[:col] + str(new_code) + s[col+1:]

                # BUILD (unlock/establish)
                if self.toolActive == "building" and self.selectedTile in totalNeighbors:
                    if code == 0 and int(self.save[0]) >= unlockLandUpgrade:
                        set_map_code(r, c, 1)
                        self.tileList[self.selectedTile].farmType = "1"
                        self.save[0] = int(self.save[0]) - unlockLandUpgrade
                        pygame.mixer.Sound.play(self.buildSound[random.randrange(4)])
                    elif code == 1 and int(self.save[0]) >= establishLandUpgrade:
                        set_map_code(r, c, 2)
                        self.tileList[self.selectedTile].farmType = "2"
                        self.save[0] = int(self.save[0]) - establishLandUpgrade
                        pygame.mixer.Sound.play(self.buildSound[random.randrange(4)])

                # PLANT COCOA
                elif self.toolActive == "cocoaSeeds":
                    if code == 2 and int(self.save[0]) >= cocoaFarmUpgradeGoldCost and int(self.save[2]) >= cocoaFarmUpgradeCocoaCost:
                        set_map_code(r, c, 3)
                        fm = farm(); fm.farmType = 3; fm.location = (r, c); fm.tileLocation = self.selectedTile
                        self.save[0] = int(self.save[0]) - cocoaFarmUpgradeGoldCost
                        self.save[2] = int(self.save[2]) - cocoaFarmUpgradeCocoaCost
                        self.cocoaFarmList.append(fm)
                        pygame.mixer.Sound.play(self.plantSound[random.randrange(3)])

                # PLANT WHEAT
                elif self.toolActive == "wheatSeeds":
                    if code == 2 and int(self.save[0]) >= wheatFarmUpgradeGoldCost and int(self.save[1]) >= wheatFarmUpgradeWheatCost:
                        set_map_code(r, c, 4)
                        fm = farm(); fm.farmType = 4; fm.location = (r, c); fm.tileLocation = self.selectedTile
                        self.save[0] = int(self.save[0]) - wheatFarmUpgradeGoldCost
                        self.save[1] = int(self.save[1]) - wheatFarmUpgradeWheatCost
                        self.wheatFarmList.append(fm)
                        pygame.mixer.Sound.play(self.plantSound[random.randrange(3)])

                # DEMOLISH → set to unlocked land (1)
                elif self.toolActive == "demo":
                    if code == 4:  # wheat
                        set_map_code(r, c, 1)
                        self.wheatFarmList[:] = [fm for fm in self.wheatFarmList if fm.tileLocation != self.selectedTile]
                    elif code == 3:  # cocoa
                        set_map_code(r, c, 1)
                        self.cocoaFarmList[:] = [fm for fm in self.cocoaFarmList if fm.tileLocation != self.selectedTile]

                # AUTOMATION
                elif self.toolActive == "automation":
                    if code == 3:  # cocoa
                        if int(self.save[0]) >= automationCocoaFarmGoldCost and int(self.save[2]) >= automationCocoaFarmCocoaCost:
                            self.save[0] = int(self.save[0]) - automationCocoaFarmGoldCost
                            self.save[2] = int(self.save[2]) - automationCocoaFarmCocoaCost
                            for fm in self.cocoaFarmList:
                                if fm.tileLocation == self.selectedTile:
                                    fm.auto = 1
                        else:
                            self._flash(f"Not enough resources to automate cocoa farm! Need {automationCocoaFarmGoldCost} gold and {automationCocoaFarmCocoaCost} cocoa.")
                    elif code == 4:  # wheat
                        if int(self.save[0]) >= automationWheatFarmGoldCost and int(self.save[1]) >= automationWheatFarmWheatCost:
                            self.save[0] = int(self.save[0]) - automationWheatFarmGoldCost
                            self.save[1] = int(self.save[1]) - automationWheatFarmWheatCost
                            for fm in self.wheatFarmList:
                                if fm.tileLocation == self.selectedTile:
                                    fm.auto = 1
                        else:
                            self._flash(f"Not enough resources to automate wheat farm! Need {automationWheatFarmGoldCost} gold and {automationWheatFarmWheatCost} wheat.")

            # ---------- PERSIST SAVE ----------
            # Old code popped 4 times then appended. Build fresh instead (safer & faster).
            head = self.save[:4]
            tail = self.save[len(self.save)-8:]  # drop old map/auto tail if present
            new = head[:]  # copy head
            new.extend(self.mapData[:4])
            new.extend(self.autoData[:4])
            self.save = new
            f.lineUpdater(str(self.root / self.user_name), self.save)


def draw(self) -> None:
    """Render one frame. Assumes pg.display.flip() is called by the main loop."""
    screen = self.screen

    # ---- MAP TILES ----
    idx = 0
    for row in self.mapData:               # each row is a string like "32000000"
        for _ in row:                      # iterate characters by position
            x, y = self.tile_positions[idx]
            tile_code = int(row[idx % len(row)])  # same logic as your rc = int(row[column])
            screen.blit(self.tileTypes[tile_code], (x, y))
            idx += 1

    # ---- TOOL BUTTON STATES ----
    # Mirrors your original buttonData mutations, but uses self.* state.
    # Expected: self.buttonData -> 2xN int matrix; self.buttonTypes -> list of button images in the same order.
    if self.toolActive == "farming":
        self.buttonData[0][0] = 4
    else:
        self.buttonData[0][0] = 2

    if self.toolActive == "building":
        self.buttonData[0][1] = 5
    else:
        self.buttonData[0][1] = 3

    if self.toolActive == "demo":
        self.buttonData[0][2] = 11
    else:
        self.buttonData[0][2] = 10

    if self.toolActive == "automation":
        self.buttonData[0][3] = 13
    else:
        self.buttonData[0][3] = 12

    self.buttonData[1][0] = 9 if self.toolActive == "cocoaSeeds" else 8
    self.buttonData[1][1] = 7 if self.toolActive == "wheatSeeds" else 6

    # ---- DRAW BUTTONS ----
    bx = by = 0
    for row in self.buttonData:
        for col_idx in range(len(row)):
            img = self.buttonTypes[row[col_idx]]
            x, y = self.button_positions[bx], self.button_y_positions[by]
            screen.blit(img, (x, y))
            bx += 1
            by += 1
    # reset (optional if you don’t reuse bx/by)
    bx = by = 0

    # ---- FARMS ----
    # Upgrade + render (unchanged logic; just uses self.*)
    for fm in self.cocoaFarmList:
        fm.upgrade()
        fm.displayFarm(screen, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)
    for fm in self.wheatFarmList:
        fm.upgrade()
        fm.displayFarm(screen, self.iconTypes, self.iconPos, self.progressBars, self.wheatStages, self.cocoaStages)

    # ---- HUD ----
    screen.blit(self.HUD, (0, 0))

    # Floating message near mouse, timed
    if self.display_message and (time.time() - self.message_start_time) < self.message_duration:
        txt = self.font.render(self.display_message, True, (255, 0, 0))
        mx, my = self.message_position
        screen.blit(txt, (mx + 10, my + 10))
    elif self.display_message and (time.time() - self.message_start_time) >= self.message_duration:
        self.display_message = None  # clear after duration

    # ---- IN-GAME MENU ----
    if self.menuActive:
        # assumes you migrated menuDisplay(...) to a method on the class:
        self.menu_display()

    # NOTE: flip in main loop, not here.


from __future__ import annotations
import itertools, os, pygame as pg
from pathlib import Path

TILE_W = TILE_H = 126
GRID_ROWS, GRID_COLS = 4, 8
SCREEN_W, SCREEN_H = 1080, 720
FPS = 60

class GameApp:
    def __init__(self, root: str, user_name: str):
        # --- init pygame/window ---
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        pg.display.set_caption("Chocolate Tycoon")
        self.clock = pg.time.Clock()
        self.dt = 0.0

        # --- paths/constants ---
        self.root = Path(root)
        self.assets = Path("graphics")  # make this absolute if needed: self.root / "graphics"
        self.font = pg.font.SysFont("Acumin-Variable-Concept.ttf", 20)

        # --- save + map ---
        self.save = f.lineGrabber(str(self.root / user_name))
        self.mapData = [str(self.save[i + 4]) for i in range(len(self.save) - 8)]
        self.autoData = [str(self.save[i + 8]) for i in range(len(self.save) - 8)]

        # --- resources (images/sfx cached) ---
        self.images = {}
        self.sounds = {}
        self._load_assets()

        # --- tiles / farms ---
        self.tileList = self._build_tiles(self.mapData, self.autoData)
        self.cocoaFarmList, self.wheatFarmList = self._build_farms(self.mapData, self.autoData)

        # --- UI geometry (computed, not hard-coded) ---
        self.tile_positions = self._grid_positions(GRID_ROWS, GRID_COLS, start=(8, 8), step=(134, 134))
        self.button_positions = self._grid_positions(2, GRID_COLS, start=(8, 544), step=(134, 91))
        self.menu_rect = pg.Rect(0, 0, int(self.screen.get_width() / 1.5), int(self.screen.get_height() / 1.5))
        self.menu_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.inScreenButtonX = self.screen.get_width() - int(1.25 * self.menu_rect.w) + 18

        # --- button data ---
        self.buttonData = self._load_button_data(self.assets / "buttondata.txt")

        # keep your existing toggles/state elsewhere; this class just replaces runPyGame setup
        # e.g. self.state = GameState(...)

    # ---------------- helpers ----------------
    def _p(self, *parts: str) -> str:
        return str(Path(*parts))

    def _img(self, rel: str, size: tuple[int, int] | None = None) -> pg.Surface:
        # cache by (rel, size)
        key = (rel, size)
        if key in self.images:
            return self.images[key]
        surf = pg.image.load(self._p(self.assets, rel)).convert_alpha()
        if size is not None:
            surf = pg.transform.scale(surf, size)
        self.images[key] = surf
        return surf

    def _sfx(self, rel: str) -> pg.mixer.Sound:
        if rel in self.sounds:
            return self.sounds[rel]
        s = pg.mixer.Sound(self._p(self.assets, rel))
        self.sounds[rel] = s
        return s

    def _grid_positions(self, rows: int, cols: int, start=(0, 0), step=(0, 0)) -> list[tuple[int, int]]:
        sx, sy = start
        dx, dy = step
        return [(sx + c * dx, sy + r * dy) for r in range(rows) for c in range(cols)]

    def _load_button_data(self, path: Path) -> list[list[int]]:
        data = []
        with open(path, "r") as fh:
            for row in fh.read().splitlines():
                data.append([int(ch) for ch in row])
        return data

    def _build_tiles(self, mapData: list[str], autoData: list[str]):
        tiles = []
        for i, j in itertools.product(range(GRID_ROWS), range(GRID_COLS)):
            t = land()
            t.farmType = mapData[i][j]
            t.tileLocation = i * GRID_COLS + j
            t.makeNeighbors()
            if int(autoData[i][j]) == 1:
                t.auto = 1
            tiles.append(t)
        return tiles

    def _build_farms(self, mapData: list[str], autoData: list[str]):
        cocoa, wheat = [], []
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                code = mapData[i][j]
                if code == "3":  # cocoa
                    fm = farm(); fm.farmType = 3; fm.location = (i, j); fm.tileLocation = i * GRID_COLS + j; fm.auto = int(autoData[i][j])
                    cocoa.append(fm)
                elif code == "4":  # wheat
                    fm = farm(); fm.farmType = 4; fm.location = (i, j); fm.tileLocation = i * GRID_COLS + j; fm.auto = int(autoData[i][j])
                    wheat.append(fm)
        return cocoa, wheat

    def _load_assets(self) -> None:
        # HUD & menu
        self.HUD = self._img("Map Final.png", (self.screen.get_width(), self.screen.get_height()))
        self.menu_img = self._img("Menu.png", (int(self.screen.get_width() / 1.5), int(self.screen.get_height() / 1.5)))

        # tiles
        self.lockedLand = self._img("LockedLand.png", (TILE_W, TILE_H))
        self.unlockedLand = self._img("UnlockedLand.png", (TILE_W, TILE_H))
        self.establishedLand = self._img("EstablishedLand.png", (TILE_W, TILE_H))
        self.wheatStages = [self._img("wheat_farm_ungrown_NEW.PNG", (TILE_W, TILE_H)),
                            self._img("wheat_farm_grown_new.PNG", (TILE_W, TILE_H)),
                            self._img("wheat_farm_grown_more_NEW.PNG", (TILE_W, TILE_H))]
        self.cocoaStages = [self._img("cocoa_farm_stage1.PNG", (TILE_W, TILE_H)),
                            self._img("cocoa_farm_stage2.PNG", (TILE_W, TILE_H)),
                            self._img("cocoa_farm_stage3.PNG", (TILE_W, TILE_H))]
        self.cocoaFarmIcon = self._img("Cocoa Bean.png", (TILE_W, TILE_H))
        self.wheatFarmIcon = self._img("wheat.png", (TILE_W, TILE_H))

        # buttons
        self.buttonImages = {
            "menu": self._img("MenuButton.png", (126, 83)),
            "bg": self._img("Button Backgrounds Released.png", (126, 83)),
            "harvest": self._img("Farm Tool Button Icon.png", (126, 83)),
            "harvest_on": self._img("Farm Tool Button Toggled.png", (126, 83)),
            "build": self._img("Building Tool.png", (126, 83)),
            "build_on": self._img("Building Tool Toggled.png", (126, 83)),
            "wheat": self._img("Wheat Tool.png", (126, 83)),
            "wheat_on": self._img("Wheat Tool Toggled.png", (126, 83)),
            "cocoa": self._img("Cocoa Tool.png", (126, 83)),
            "cocoa_on": self._img("Cocoa Tool Toggled.png", (126, 83)),
            "shovel": self._img("Shovel Tool.png", (126, 83)),
            "shovel_on": self._img("Shovel Tool Toggled.png", (126, 83)),
            "auto": self._img("Automation Tool.png", (126, 83)),
            "auto_on": self._img("Automation Tool Toggled.png", (126, 83)),
        }

        # in-menu widgets
        self.plus = self._img("plus.png", (25, 15))
        self.minus = self._img("minus.png", (25, 15))
        self.inMenuResourcesTextBox = self._img("In Menu Resources Text Box.png", (520, 400))
        self.inMenuBazaarTextBox = self.inMenuResourcesTextBox

        # progress bars
        self.progressBars = [
            self._img("Progress Bar No Mass.png", (72, 8)),
            self._img("Progress Bar One Mass.png", (72, 8)),
            self._img("Progress Bar Two Mass.png", (72, 8)),
        ]

        # sounds
        self.coinCollectSound = self._sfx("sound/coincollect.wav")
        self.plantSound = [self._sfx("sound/plant1.ogg"), self._sfx("sound/plant2.ogg"), self._sfx("sound/plant3.ogg")]
        self.buildSound = [self._sfx("sound/stone1.ogg"), self._sfx("sound/stone2.ogg"),
                           self._sfx("sound/stone3.ogg"), self._sfx("sound/stone4.ogg")]

        # tile atlas for draw pass
        self.tileTypes = [self.lockedLand, self.unlockedLand, self.establishedLand,
                          self.cocoaStages[0], self.wheatStages[0]]

    # ---------------- main loop ----------------
    def run(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                # delegate to your existing input/menu handlers here

            # call your existing update/draw functions with self.* instead of globals
            # update(self.dt, self.screen, ...)
            # draw(self.screen, self.font, ...)

            pg.display.flip()
            self.dt = self.clock.tick(FPS) / 1000.0
        pg.quit()


# Replace runPyGame() with:
def runPyGame():
    app = GameApp(root, userName)
    app.run()


'''