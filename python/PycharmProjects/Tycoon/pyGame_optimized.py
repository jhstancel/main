import sys
import time
import pygame
from pygame.locals import *
import os
import itertools
import random
import utils as f

# Configuration module
class Config:
    WIDTH = 1080
    HEIGHT = 720
    FPS = 15
    COLORS = {
        "WHITE": [255, 255, 255],
        "GREEN": [0, 255, 0],
        "BLUE": [0, 0, 255],
        "BLACK": [0, 0, 0],
        "RED": [255, 0, 0]
    }
    ROOT = os.path.dirname(os.path.realpath(__file__)) + "\\saveFiles\\"
    GRAPHICS_PATH = "graphics/"
    SOUND_PATH = "graphics/sound/"
    TILE_SIZE = (126, 126)
    BUTTON_SIZE = (126, 83)

    # Defined positions for UI elements
    BUTTON_POSITIONS = [8, 142, 276, 410, 544, 678, 812, 946,
                        8, 142, 276, 410, 544, 678, 812, 946]
    BUTTON_Y_POSITIONS = [544, 544, 544, 544, 544, 544, 544, 544,
                          635, 635, 635, 635, 635, 635, 635, 635]
    ICON_POSITIONS = [
        [(8, 8), (142, 8), (276, 8), (410, 8), (544, 8), (678, 8), (812, 8), (946, 8)],
        [(8, 142), (142, 142), (276, 142), (410, 142), (544, 142), (678, 142), (812, 142), (946, 142)],
        [(8, 276), (142, 276), (276, 276), (410, 276), (544, 276), (678, 276), (812, 276), (946, 276)],
        [(8, 410), (142, 410), (276, 410), (410, 410), (544, 410), (678, 410), (812, 410), (946, 410)]
    ]
    MENU_BUTTON_HITBOXES = [
        [900, 71], [900, 131], [900, 191], [900, 251], [900, 311], [900, 371], [900, 431]
    ]
    BUTTON_HITBOXES = [[8, 536], [142, 536], [276, 536], [410, 536], [544, 536], [678, 536], [812, 536], [946, 536],
                       [8, 627], [142, 627], [276, 627], [410, 627], [544, 627], [678, 627], [812, 627], [946, 627]]
    TILE_HITBOXES = [[8, 8], [142, 8], [276, 8], [410, 8], [544, 8], [678, 8], [812, 8], [946, 8],
                     [8, 142], [142, 142], [276, 142], [410, 142], [544, 142], [678, 142], [812, 142], [946, 142],
                     [8, 268], [142, 268], [276, 268], [410, 268], [544, 268], [678, 268], [812, 268], [946, 268],
                     [8, 402], [142, 402], [276, 402], [410, 402], [544, 402], [678, 402], [812, 402], [946, 402]]

# Resource Loader
class ResourceLoader:
    def __init__(self):
        self.graphics = {}
        self.sounds = {}

    def load_graphics(self, name, path, size=None):
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        self.graphics[name] = image

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def get_graphic(self, name):
        return self.graphics.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

# Game State Management
class GameState:
    def __init__(self):
        self.user_name = None
        self.save_information = []
        self.map_data = []
        self.auto_data = []
        self.cocoa_farm_list = []
        self.wheat_farm_list = []

    def initialize(self, loader):
        self.user_name = f.logIn()
        if not self.user_name:
            print("No account found. Exiting game.")
            sys.exit()
        self.load_save_information()
        self.setup_farms()
        loader.load_graphics("HUD", Config.GRAPHICS_PATH + "Map Final.png", (Config.WIDTH, Config.HEIGHT))

    def load_save_information(self):
        save_file = Config.ROOT + self.user_name
        if not f.doesSaveExist(save_file):
            print("New save file created.")
            return
        self.save_information = f.lineGrabber(save_file)
        self.map_data = self.save_information[4:8]
        self.auto_data = self.save_information[8:12]

    def save_game(self):
        save_file = Config.ROOT + self.user_name
        for i in range(4):
            self.save_information[4 + i] = self.map_data[i]
            self.save_information[8 + i] = self.auto_data[i]
        f.lineUpdater(save_file, self.save_information)

    def setup_farms(self):
        for i, j in itertools.product(range(len(self.map_data)), range(len(self.map_data[0]))):
            position = Config.ICON_POSITIONS[i][j]
            if self.map_data[i][j] == "3":
                self.cocoa_farm_list.append(Farm(3, position))
            elif self.map_data[i][j] == "4":
                self.wheat_farm_list.append(Farm(4, position))

class Farm:
    def __init__(self, farm_type, position):
        self.farm_type = farm_type
        self.position = position
        self.update_progress = 0
        self.reward = 5
        self.rate = 1

    def upgrade(self):
        if self.update_progress < 100:
            self.update_progress += self.rate

    def reward_update(self):
        pass

    def display(self, screen, loader):
        farm_icon = loader.get_graphic("CocoaFarm" if self.farm_type == 3 else "WheatFarm")
        screen.blit(farm_icon, self.position)

class Menu:
    def __init__(self, loader):
        self.loader = loader

    def display(self, screen):
        menu_graphic = self.loader.get_graphic("Menu")
        screen.blit(menu_graphic, (Config.WIDTH - 540, Config.HEIGHT - 360))

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Chocolate Tycoon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.loader = ResourceLoader()
        self.state = GameState()
        self.menu = Menu(self.loader)
        self.menu_active = False
        self.font = pygame.font.SysFont("Acumin-Variable-Concept.ttf", 20)

    def load_resources(self):
        # Load graphics
        self.loader.load_graphics("HUD", Config.GRAPHICS_PATH + "Map Final.png", (Config.WIDTH, Config.HEIGHT))
        self.loader.load_graphics("Menu", Config.GRAPHICS_PATH + "Menu.png", (720, 480))
        self.loader.load_graphics("LockedLand", Config.GRAPHICS_PATH + "LockedLand.png", Config.TILE_SIZE)
        self.loader.load_graphics("UnlockedLand", Config.GRAPHICS_PATH + "UnlockedLand.png", Config.TILE_SIZE)
        self.loader.load_graphics("EstablishedLand", Config.GRAPHICS_PATH + "EstablishedLand.png", Config.TILE_SIZE)
        self.loader.load_graphics("CocoaFarm", Config.GRAPHICS_PATH + "CocoaFarm.png", Config.TILE_SIZE)
        self.loader.load_graphics("WheatFarm", Config.GRAPHICS_PATH + "WheatFarm.png", Config.TILE_SIZE)
        self.loader.load_graphics("ProgressBar0", Config.GRAPHICS_PATH + "Progress Bar No Mass.png", (72, 8))
        self.loader.load_graphics("ProgressBar1", Config.GRAPHICS_PATH + "Progress Bar One Mass.png", (72, 8))
        self.loader.load_graphics("ProgressBar2", Config.GRAPHICS_PATH + "Progress Bar Two Mass.png", (72, 8))

        # Load buttons
        self.loader.load_graphics("MenuButton", Config.GRAPHICS_PATH + "MenuButton.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("ButtonBackgroundReleased", Config.GRAPHICS_PATH + "Button Backgrounds Released.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("HarvestButton", Config.GRAPHICS_PATH + "Farm Tool Button Icon.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("HarvestButtonToggled", Config.GRAPHICS_PATH + "Farm Tool Button Toggled.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("BuildButton", Config.GRAPHICS_PATH + "Building Tool.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("BuildButtonToggled", Config.GRAPHICS_PATH + "Building Tool Toggled.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("WheatButton", Config.GRAPHICS_PATH + "Wheat Tool.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("WheatButtonToggled", Config.GRAPHICS_PATH + "Wheat Tool Toggled.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("CocoaButton", Config.GRAPHICS_PATH + "Cocoa Tool.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("CocoaButtonToggled", Config.GRAPHICS_PATH + "Cocoa Tool Toggled.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("ShovelButton", Config.GRAPHICS_PATH + "Shovel Tool.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("ShovelButtonToggled", Config.GRAPHICS_PATH + "Shovel Tool Toggled.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("AutomationTool", Config.GRAPHICS_PATH + "Automation Tool.png", Config.BUTTON_SIZE)
        self.loader.load_graphics("AutomationToolToggled", Config.GRAPHICS_PATH + "Automation Tool Toggled.png", Config.BUTTON_SIZE)

        # Load icons
        self.loader.load_graphics("CocoaFarmIcon", Config.GRAPHICS_PATH + "Cocoa Bean.png", Config.TILE_SIZE)
        self.loader.load_graphics("WheatFarmIcon", Config.GRAPHICS_PATH + "wheat.png", Config.TILE_SIZE)

        # Load menu controls
        self.loader.load_graphics("InMenuResourcesTextBox", Config.GRAPHICS_PATH + "In Menu Resources Text Box.png", (520, 400))
        self.loader.load_graphics("InMenuBazaarTextBox", Config.GRAPHICS_PATH + "In Menu Resources Text Box.png", (520, 400))
        self.loader.load_graphics("Plus", Config.GRAPHICS_PATH + "plus.png", (25, 15))
        self.loader.load_graphics("Minus", Config.GRAPHICS_PATH + "minus.png", (25, 15))

        # Load sounds
        self.loader.load_sound("CoinCollect", Config.SOUND_PATH + "coincollect.wav")
        self.loader.load_sound("Plant1", Config.SOUND_PATH + "plant1.ogg")
        self.loader.load_sound("Plant2", Config.SOUND_PATH + "plant2.ogg")
        self.loader.load_sound("Plant3", Config.SOUND_PATH + "plant3.ogg")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.menu_active = not self.menu_active

    def update(self):
        for farm in self.state.cocoa_farm_list + self.state.wheat_farm_list:
            farm.upgrade()

    def draw(self):
        self.screen.blit(self.loader.get_graphic("HUD"), (0, 0))

        # Draw tiles based on map data
        for i, tile_type in enumerate(self.state.map_data):
            for j, tile in enumerate(tile_type):
                tile_name = "LockedLand" if tile == "0" else \
                            "UnlockedLand" if tile == "1" else \
                            "EstablishedLand" if tile == "2" else \
                            "CocoaFarm" if tile == "3" else \
                            "WheatFarm" if tile == "4" else None
                if tile_name:
                    self.screen.blit(self.loader.get_graphic(tile_name), Config.ICON_POSITIONS[i][j])

        # Draw buttons
        for idx, (x, y) in enumerate(zip(Config.BUTTON_POSITIONS, Config.BUTTON_Y_POSITIONS)):
            if idx == len(Config.BUTTON_POSITIONS) - 1:  # Last button as menu
                button_type = "MenuButton"
            elif idx < 4:  # First four buttons as tools
                button_type = ["HarvestButton", "BuildButton", "WheatButton", "CocoaButton"][idx]
            else:
                button_type = "ButtonBackgroundReleased"  # Default for remaining buttons
            self.screen.blit(self.loader.get_graphic(button_type), (x, y))

        for farm in self.state.cocoa_farm_list + self.state.wheat_farm_list:
            farm.display(self.screen, self.loader)

        if self.menu_active:
            self.menu.display(self.screen)
        pygame.display.flip()

    def run(self):
        self.load_resources()
        self.state.initialize(self.loader)
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(Config.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
