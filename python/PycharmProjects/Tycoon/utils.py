gameName = "TYCOON"
root = "C:\\Users\\black\\code\\main\\python\\PycharmProjects\\Tycoon\\saveFiles"
newFileFormat = "0\n" \
                "0\n" \
                "0\n" \
                "0\n" \
                "32000000\n" \
                "21000000\n" \
                "10000000\n" \
                "00000000\n" \
                "00000000\n" \
                "00000000\n" \
                "00000000\n" \
                "00000000"
NOEVENT: int = 0


def logIn():
    # loop used to enable changing account at beginning
    loggedIn = False
    while not loggedIn:
        userName = input("What is your username?\n-->")
        saveName = root + userName
        # profile does exist
        if doesSaveExist(saveName):
            attempt = input("What is your password?\n-->")
            # setting variable to the profiles recorded password
            truePassword = str(passGetter(saveName + "pass"))
            # loop used in case password attempt is incorrect
            if attempt != truePassword:
                passwordLoopFinished = False
                while not passwordLoopFinished:
                    passAttempts = passwordAuthenticator(attempt, truePassword)
                    # one of the attempts worked
                    if passAttempts == "true":
                        print("Welcome back " + userName + "!")
                        passwordLoopFinished = True
                        loggedIn = True
                        return userName
                    # client quit the current attempt
                    elif passAttempts == "restart":
                        passwordLoopFinished = True
            else:
                loggedIn = True
                print("Welcome back " + userName + "!")
                return userName

        # profile does not exist
        else:
            truePassword = input("Please create a password.\n-->")
            setPassword(saveName + "pass", truePassword)
            print("Please restart the game to play.")
            return False


def doesSaveExist(file):
    # checks if you have a save
    try:
        # file doesnt exist, creating it
        inFile = open(file, "x")
        inFile.write(newFileFormat)
        # prints welcome screen to new players
        print("Welcome to " + gameName + "!")
        return False
    except FileExistsError:
        # file exists
        return True


def passFileCreator(file, password):
    passFile = open(file + "pass", "x")
    passFile.write(password)


def passwordAuthenticator(attempt, password):
    # confirms if password is accepted
    if attempt != password:
        print("If the username you entered is incorrect, type \"c\" to cancel.")
        for i in range(4):
            attempt = input("The password you entered is incorrect. Please reenter your password.\n-->")
            if attempt == password:
                return "true"
            elif attempt == "c":
                return "restart"
    else:
        return True


def setPassword(file, password):
    with open(file, "x"):
        with open(file, "a") as tempFile:
            tempFile.write(password)
            tempFile.close()


def strToInt(arg):
    # turning arg into int
    # returns int(arg) or False
    integ = False
    while not integ:
        try:
            arg = int(arg)
            integ = True
        except ValueError:
            return False
    return arg


def lineGrabber(file):
    global NOEVENT
    # this will grab all data as a list, assumes all data to be type str()
    # so it converts to type int() so that you can easily edit stat data
    # pos 0 is gold, 1 is wheat, 2 is cocoa
    with open(file, "r+") as tempFile:
        ret = tempFile.read().splitlines()
        for i in range(len(ret)):
            ret[i] = str(ret[i])
    return ret


def passGetter(file):
    # this will retrieve and return the password of a player
    with open(file, "r") as tempFile:
        ret = tempFile.read()
    return ret


def lineUpdater(file, stats):
    # this will update all data points in the file
    # stats list is for simple access to updated stat variables
    # opens file
    with open(file, "r+") as tempFile:
        tempFile.truncate(0)
        for i in range(len(stats)):
            tempFile.write(str(stats[i]))
            tempFile.write("\n")


def evenOrOdd(num):
    return 'Even' if num % 2 == 0 else 'Odd'
