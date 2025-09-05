# find the largest and smallest number in a given array


def largestInArray(array):
    sizeCounter = 0
    for num in range(len(array)):
        for enum in range(len(array)):
            try:
                array[num] = int(array[num])
                if array[num] >= array[enum]:
                    sizeCounter += 1
                else:
                    sizeCounter = 0
                if sizeCounter == len(array):
                    return array[num]
            except ValueError:
                # string was inside array argument
                return "Error"


myList = [7, 9, 15, 2, 17, 22, 29, 201, 1, -1, 1.01, 201.1, 205, 205.5]
# print(largestInArray(myList))
print(205.5 >= 205)
