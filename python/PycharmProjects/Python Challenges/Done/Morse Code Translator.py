# this function will turn any piece of english into a sentence in morse code!

morseDict = {
    "a": "·−",
    "b": "−···",
    "c": "−·−·",
    "d": "−··",
    "e": "·",
    "f": "··−·",
    "g": "−−·",
    "h": "····",
    "i": "··",
    "j": "·−−−",
    "k": "−·−",
    "l": "·−··",
    "m": "−−",
    "n": "−·",
    "o": "−−−",
    "p": "·−−·",
    "q": "−−·−",
    "r": "·−·",
    "s": "···",
    "t": "−",
    "u": "··−",
    "v": "···−",
    "w": "·−−",
    "x": "−··−",
    "y": "−·−−",
    "z": "−−··",
}


def englishToMorse(userInput):
    translation = []
    for letter in userInput:
        translation.append(morseDict[letter]) if letter in morseDict else translation.append(letter)
    newSentence = ' '.join(translation)
    return newSentence


while True:
    uInput = input(">> ")
    print(englishToMorse(uInput))
