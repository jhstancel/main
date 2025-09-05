# Started 12.15.22
# Watching a movie about a guy living in the Swedish forest for 3 years while home sick from school has made me want to
# do something of the sort, my outlet? Programming a game similar to what he is doing. A little ironic
# https://www.youtube.com/watch?v=FtiaSn5iCg8

"""
Ideas

Farming
Building
Domesticating


Forest
Lake
Prairie
"""

places = ["A clearing in a forest", "An old wooden cabin", "A dark cave", "The top of a Hill", "Deep in the Forest",
          "An Underground Lake", "Caught in the Brambles"]
moves = [{"n": 1, "s": 2, "e": 4}, {"s": 0, "e": 3}, {"n": 0}, {"w": 1, "s": 4}, {"n": 3, "w": 1, "e": 6}, {"w": 2},
         {"w": 4}]
objects = {"spanner": 0, "lockpick": 0, "spade": 2}
location = 0


def print_objects():
    for key, val in objects.items():
        if val == location:
            print(key)


def items():
    print("You are carrying: ")
    for key, val in objects.items():
        if val == 99:
            print(key)


def take_object(noun):
    for key, val in objects.items():
        if key == noun and val == location:
            print("Got it!")
            objects[noun] = 99


def drop_object(noun):
    for key, val in objects.items():
        if key == noun and val == 99:
            print("Dropped ", noun)
            objects[noun] = location


def use_object(noun):
    if noun == "spade" and location == 0:
        objects["gold"] = 0  # create the gold
        print("You dug up some gold!")
    if noun == "spade" and location == 2:
        moves[2] = {"n": 0, "e": 5}
        print("You've opened up a tunnel, leading east...")


def Main():
    ans = ""
    global location
    print(places[0])
    print_objects()

    while ans != "bye":
        ans = input("What now?")
        words = ans.split()

        # Check if it's a move
        if len(words) == 1:
            if ans == "items":
                items()
            elif ans == "look":
                print(places[location])
                print_objects()

            elif ans in moves[location]:
                location = moves[location].get(ans)
                print(places[location])
                print_objects()
            else:
                print("I can't move that way")
        else:
            verb = words[0]  # e.g. Take or Drop
            noun = words[1]  # e.g. hammer or spanner

            if verb == "take":
                take_object(noun)

            elif verb == "drop":
                drop_object(noun)

            elif verb == "use":
                try:
                    if objects[noun] == 99:  # check holding object
                        use_object(noun)
                    else:
                        print("I don't have a", noun)
                except:
                    print("I don't know what a", noun, "is")

            else:
                print("I don't understand what you mean")


Main()
