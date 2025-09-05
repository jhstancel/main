# this function will remove any duplicate letters from an entered string

def duplicateLetters(sentence):
    duplicateFreeList = []
    for letter in sentence:
        if letter not in duplicateFreeList:
            duplicateFreeList.append(letter)
    newSentence = ''.join(duplicateFreeList)
    return newSentence


while True:
    uInput = input(">> ")
    print(duplicateLetters(uInput))
