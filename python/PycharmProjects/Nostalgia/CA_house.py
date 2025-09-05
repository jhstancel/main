# Crustass House Adventure Project
# Created by: John Stancel
#  Dec. 16-17, 2020


# imports
import time

# ---

# settings values
done = False
current_room = 0
next_room = 0
# ---

# text prompt calls
storyPart1 = ""

storyPart2 = ""

upstairs = "The upstairs is mostly the boring stuff. Bedrooms, the\n" \
           "kitchen, the bar. Stuff like that. Not too much to see.\n"

controls = "north, east, south, west, quit"
# ---

# defining the rooms
room_list = []

room = ["This is the entrance of the Crust House. Statues of the elite four surround you.\n"
        "Patrick, John, Chloe, and Zach. The four horsemen of ___. Jazz plays faintly in\n"
        "the distance. You feel at peace. What a great way to start the day.\n"
        "There is a room to the north.\n",
        2, None, None, None]
room_list.append(room)
room = ["You are now in the refreshment and snack room. There is gFuel, Doritos, and\n"
        "Mountain Dew everywhere.\n"
        "There is a room to your north and east.\n",
        4, 2, None, None]
room_list.append(room)
room = ["This is the Southern Crust Hallway. Paintings of the elite four surround you, along\n"
        "with a monument to those that came in and out of this group.\n"
        "There is a room to your north, east, south, and west.\n",
        5, 3, 0, 1]
room_list.append(room)
room = ["You have entered the Theater. This place shows the best of the best movies, and videos.\n"
        "It is fabled that this is the room where everyone hooked up. How romantic.\n"
        "There is a room to your north, and west.\n",
        6, None, None, 2]
room_list.append(room)
room = ["Here is the bathroom. It has the most luxurious shower and toilet I have ever seen. The\n"
        "toilet paper is made of pure cloth, so no one has a crusty ass. How beautiful; and ironic.\n"
        "There is a room to the east and the south.\n",
        None, 5, 1, None]
room_list.append(room)
room = ["You have entered the Northern Crust Hallway. This room radiates good energy, and also water.\n"
        "There are fountains, a fish tank as the floor, and even a waterfall. This was expensive.\n"
        "There is a room to the north, east, south, and west.\n",
        7, 6, 2, 4]
room_list.append(room)
room = ["This room is known as the Disco room. Once a month the group meets here and has a\n"
        "disco night, where they hire a dj and do lots of drugs and dance. This usually\n"
        "ends in some sort of juvenile activity, or something of the sort, if you know\n"
        "what I mean.\n"
        "There is a room to the south and west.\n",
        None, None, 3, 5]
room_list.append(room)
room = ["This is the Vibe Lounge. Probably the most popular room of all, with the four\n"
        "gaming setups with matching duel monitors and mini fridges, the Hot tub, and\n"
        "the on-the-fly drug dealer, for long gaming sessions.\n"
        "Going north brings you upstairs.\n",
        9, None, 5, None]
room_list.append(room)
room = ["This is John's Minecraft Cellar. This is basically just his bedroom.\n"
        "Not much to see here besides a desk, a bed, some LED strips, and Duke, the\n"
        "house dog.\n"
        "There is a room to your north and west.\n",
        10, None, None, 9]
room_list.append(room)
room = ["You are now in Chloe's Bedwars Aquarium. It smells great, and the walls\n"
        "are pastel blue and green. It's a nice vibe, with the traditional desk and bed.\n"
        "There is a room to your north and east.\n",
        12, 10, None, None]
room_list.append(room)
room = ["You go into the Upper Southern Crust Hall. A display of nature. There are\n"
        "vines, and trees, and flowers, and plants of all different types and colors.\n"
        "The air in here is crisp, and it is foggy. Straight out of a horror movie, but\n"
        "it is tranquil. This is the only room in the building that has steady sunlight, from\n"
        "a glass dome in the roof.\n"
        "There is a room to your north, east, south, and west.\n",
        13, 11, 8, 9]
room_list.append(room)
room = ["This is Zach's VR room. Again, another bedroom. There is a lot of empty space\n"
        "for a working VR experience, but there is a bed in the corner.\n"
        "There is a room to your north and west.\n",
        14, None, None, 10]
room_list.append(room)
room = ["You go into the bar. Alcohol and a mix that is way to salty make the room feel\n"
        "classic. It's a comforting feeling from a black and white movie, where\n"
        "you are the protagonist.\n"
        "There is a room to your east and south.\n",
        None, 13, 9, None]
room_list.append(room)
room = ["This is the Upper Northern Crust Hallway. Nothing too special about this room, but \n"
        "this is where the four routers are. We use four so we all each have 1g up and down.\n"
        "There isa  room to your north, east, south, and west.\n",
        15, 14, 10, 12]
room_list.append(room)
room = ["Welcome to Patrick's Rainbow Six Siege Chamber. This is his bedroom. Not much to see here\n"
        "besides Steamy Linguini Monshtini, the house guinea pig, and a bottle of lotion.\n"
        "There is a room to your south and west.\n",
        None, None, 11, 13]
room_list.append(room)
room = ["Here is the kitchen. This is where the chef makes breakfast, lunch, and dinner. He\n"
        "is a professional from Africa, so we pay him with water. A little racist, but it\n"
        "doesn't really matter, we have four refrigerators.\n"
        "There is a room to your south.\n",
        None, None, 13, None]
# ---

# beginning prompt
print(storyPart1)
time.sleep(0)
print(storyPart2)
time.sleep(0)
print()
print("The controls are:", controls)
# ---


# main loop
while not done:
    print()
    print(room_list[current_room][0])

    # evaluating users input
    user_choice = input("What would you like to do?\n-~>").lower()
    while user_choice not in ["north", "n", "east", "e", "south", "s", "west", "w", "quit", "q"]:
        user_choice = input("That is not a valid input. Please reselect:\n-~>")

    # computing the choice
    if user_choice in ["north", "n"]:
        next_room = room_list[current_room][1]
    elif user_choice in ["east", "e"]:
        next_room = room_list[current_room][2]
    elif user_choice in ["south", "s"]:
        next_room = room_list[current_room][3]
    elif user_choice in ["west", "w"]:
        next_room = room_list[current_room][4]
    elif user_choice in ["quit", "q"]:
        done = True
    elif user_choice == "north" and next_room == 8:
        print(upstairs)
    else:
        print("This outcome is not possible.")

    # 'can't go that way' protocol
    if next_room is None:
        print("You can't go that way, sorry.")
    else:
        current_room = next_room


