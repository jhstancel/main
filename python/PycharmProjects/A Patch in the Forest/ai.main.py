#!/usr/bin/env python3
"""
A text-based adventure game set in the Alaskan wilderness.

You are a traveler who has decided to build your own cabin deep in the forest,
live simply, and reflect on life—much like Thoreau at Walden Pond. You start
with basic tools and must gather resources, build your cabin, and explore the
surrounding wilderness. Along the way, you'll encounter wildlife, harsh weather,
and opportunities for philosophical reflection.

This version clears the screen after each command and reprints the help text,
so that no previous commands are visible on the screen.
"""

import sys
import time
import os

# ---------------------------------------------------------------------------
# Data Structures & Constants
# ---------------------------------------------------------------------------

GAME_INTRO = """
You stand at the edge of a quiet lake in the Alaskan wilderness. Before you, tall pines
sway gently in a breeze, and beyond them lies the infinite quiet of the mountains. You've
come here to build a life of solitude—your own cabin, your own survival, and your own
philosophy. You carry a few tools in your pack, and your mind is filled with dreams and
questions.

A raven caws in the distance. It's time to begin.
"""

HELP_TEXT = """
Available commands:
- look: Examine your surroundings
- move <direction>: Move (e.g., move north, move east)
- gather <resource>: Attempt to gather resources (wood, berries, etc.)
- build <structure>: Attempt to build something (cabin, fire, tools)
- inventory: Check your inventory
- rest: Take a moment to rest and reflect
- talk: Reflect on philosophical themes or talk to yourself
- help: Show this help message
- quit: Exit the game
"""

DIRECTIONS = ["north", "south", "east", "west"]

RESOURCES = {
    "wood": {"tool_needed": "axe", "quantity": 3},
    "berries": {"tool_needed": None, "quantity": 5},
    "fish": {"tool_needed": "fishing_rod", "quantity": 2},
}

BUILDING_REQUIREMENTS = {
    "cabin": {"wood": 20},
    "fire": {"wood": 2},
    "fishing_rod": {"wood": 1},
}

REFLECTIONS = [
    "You think about the meaning of simplicity in a world driven by complexity.",
    "You contemplate the nature of solitude, and how it sharpens the mind and senses.",
    "You wonder if the true measure of wealth is not in coin but in self-sufficiency.",
    "You recall that every tree here is older than you, wiser in its quiet existence.",
    "You ponder how survival itself can be a profound teacher."
]


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def clear_screen():
    # Clears the terminal screen on Windows or Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = {
            "wood": 0,
            "berries": 0,
            "fish": 0
        }
        self.tools = ["axe"]  # start with a basic axe
        self.health = 100
        self.energy = 100
        self.location = (0, 0)  # starting location
        self.cabin_built = False
        self.has_fire = False
        self.time_passed = 0

    def gather_resource(self, resource):
        if resource not in RESOURCES:
            return ("You cannot gather that resource here.", False)

        req_tool = RESOURCES[resource]["tool_needed"]
        if req_tool and req_tool not in self.tools:
            return (f"You need a {req_tool} to gather {resource}.", False)

        quantity = RESOURCES[resource]["quantity"]
        self.inventory[resource] = self.inventory.get(resource, 0) + quantity
        self.energy = max(self.energy - 10, 0)
        return (f"You gather {quantity} units of {resource}.", True)

    def build_structure(self, structure):
        if structure not in BUILDING_REQUIREMENTS:
            return ("You cannot build that structure.", False)

        requirements = BUILDING_REQUIREMENTS[structure]
        for rsc, amt in requirements.items():
            if self.inventory.get(rsc, 0) < amt:
                return (f"You do not have enough {rsc} to build a {structure}.", False)

        for rsc, amt in requirements.items():
            self.inventory[rsc] -= amt

        if structure == "cabin":
            self.cabin_built = True
        elif structure == "fire":
            self.has_fire = True
        elif structure == "fishing_rod":
            self.tools.append("fishing_rod")

        self.energy = max(self.energy - 15, 0)
        return (f"You build a {structure}.", True)

    def rest(self):
        gained_energy = 20 if self.cabin_built else 10
        self.energy = min(self.energy + gained_energy, 100)
        self.time_passed += 1
        return "You rest quietly, regaining some energy."

    def reflect(self):
        import random
        return random.choice(REFLECTIONS)

    def move(self, direction):
        if direction not in DIRECTIONS:
            return ("You can't move in that direction.", False)
        x, y = self.location
        if direction == "north":
            self.location = (x, y + 1)
        elif direction == "south":
            self.location = (x, y - 1)
        elif direction == "east":
            self.location = (x + 1, y)
        elif direction == "west":
            self.location = (x - 1, y)
        self.energy = max(self.energy - 5, 0)
        self.time_passed += 1
        return (f"You move {direction}. The wilderness spreads out before you.", True)

    def check_inventory(self):
        inv_str = "Your inventory:\n"
        for item, qty in self.inventory.items():
            inv_str += f"  {item}: {qty}\n"
        if self.tools:
            inv_str += "Your tools: " + ", ".join(self.tools) + "\n"
        return inv_str


class World:
    def __init__(self):
        self.map_data = {
            (0, 0): {
                "desc": "Your starting location by the quiet lake. Tall pines and calm waters.",
                "resources": ["wood", "berries"]
            },
            (1, 0): {
                "desc": "A thicker forest area. The trees whisper in the wind.",
                "resources": ["wood"]
            },
            (0, 1): {
                "desc": "A small stream with clear water. You might fish here.",
                "resources": ["fish"]
            },
            (-1, 0): {
                "desc": "A mossy clearing. The ground is soft and your footsteps muffled.",
                "resources": ["berries", "wood"]
            },
            (0, -1): {
                "desc": "A rocky hillside. You see potential building materials scattered about.",
                "resources": ["wood"]
            }
        }

    def look(self, location):
        area = self.map_data.get(location, None)
        if area:
            return area["desc"]
        else:
            return "You are in a thick forest. It's hard to tell what lies here."

    def get_resources_at(self, location):
        return self.map_data.get(location, {}).get("resources", [])


class Game:
    def __init__(self):
        self.world = World()
        player_name = self.ask_name()
        self.player = Player(name=player_name)
        self.is_running = True

    def ask_name(self):
        clear_screen()
        print("What is your name, traveler?")
        name = input("> ")
        return name.strip() if name.strip() else "Wanderer"

    def intro(self):
        clear_screen()
        print(GAME_INTRO)
        time.sleep(2)
        print("Type 'help' for a list of commands.")
        time.sleep(1)

    def process_command(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()

        if cmd == "look":
            self.do_look()
        elif cmd == "move":
            if len(parts) < 2:
                print("Move where?")
            else:
                self.do_move(parts[1])
        elif cmd == "gather":
            if len(parts) < 2:
                print("Gather what?")
            else:
                self.do_gather(parts[1])
        elif cmd == "build":
            if len(parts) < 2:
                print("Build what?")
            else:
                self.do_build(parts[1])
        elif cmd == "inventory":
            print(self.player.check_inventory())
        elif cmd == "rest":
            print(self.player.rest())
        elif cmd == "talk":
            print(self.player.reflect())
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "quit":
            self.is_running = False
            print("Farewell, traveler. May your reflections linger in these woods.")
        else:
            print("You mutter a few words, but nothing happens. (Unknown command)")

    def do_look(self):
        desc = self.world.look(self.player.location)
        print(desc)
        if not self.player.cabin_built:
            print("You think: 'I should gather wood and build a cabin to rest at night.'")

    def do_move(self, direction):
        msg, success = self.player.move(direction)
        print(msg)
        if success:
            print(self.world.look(self.player.location))

    def do_gather(self, resource):
        area_resources = self.world.get_resources_at(self.player.location)
        if resource not in area_resources:
            print(f"You find no {resource} here.")
            return
        msg, success = self.player.gather_resource(resource)
        print(msg)

    def do_build(self, structure):
        msg, success = self.player.build_structure(structure)
        print(msg)

    def game_loop(self):
        self.intro()

        # After introduction, print help and wait for commands
        while self.is_running:
            if self.player.energy <= 0:
                clear_screen()
                print("You collapse from exhaustion. Game over.")
                break

            # Weather or random event could be inserted here
            if self.player.time_passed > 0 and self.player.time_passed % 10 == 0:
                print("\nThe wind picks up. The air smells of pine and distant rain.")
                print("You feel time passing differently here, each hour a lesson.\n")

            # Clear screen before showing prompt, print help every time
            clear_screen()
            print(HELP_TEXT)
            command = input("> ")
            clear_screen()
            # Process command and then reprint help after
            self.process_command(command)
            # If still running, next loop iteration will clear screen and show help again


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    game = Game()
    game.game_loop()
