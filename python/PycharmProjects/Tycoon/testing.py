# testing doc
# 3/18/2022

"""
saveFiles path -> C:\\Users\\black\PycharmProjects\Tycoon\saveFiles\\
-creating the part of the function that will edit the stats of the player, might make separate function for
    file synthesis and formatting than the file updating
(3/19/2022)
-created function to read data from individual lines (indivStatRead)
(3/26/2022)
-created function to change data from individual lines (indivStatChange)
(3/27/2022)
-working on a temporary text displayHud function
-completely scrapped all previous data grabbing and saving attempts and processes for a much simpler, easier, and
working way. This took all of last night and some of today. That's programming for ya! :P
-created separate file for password feature
(3/29/2022)
-started work on PyGame
-made working click counter woahhh crazy
(3/31/2022)
not going to document graphics because i forgot, but that has been what I've been working on recently
its a feature, not a bug
(1/12/2023)
holy shit ive literally been fixing ONE FUCKING MAP THING WHERE IT USES THE SAME DATA BUT FROM THE SAVE DOCUMENT
INSTEAD OF THE MAPDATA.TXT FILE AND HOLY SHIT IVE BEEN ON THIS FOR HOURS WHAT THE HELL WHY IS EVERYTHING BROKEN AHH
i <3 TonaBrix1 tbh this man saving my ass frfr
"""

import utils as f
import os

# root = "C:\\Users\\black\\PycharmProjects\\Tycoon\\saveFiles\\"
root = ''.join([char + '\\' if char == '\\' else char for char in os.getcwd()]) + "\\\\saveFiles\\\\"
# userName = f.logIn()

# saveInformation = f.lineGrabber(root + userName)

current_directory = os.path.dirname(os.path.realpath(__file__))

print("Current directory:", current_directory)
