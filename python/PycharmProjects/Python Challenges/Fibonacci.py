# these functions should do several different things with the fibonacci sequence

# 0 1 1 2 3 5 8 13 21 34 55 89
def cringeAhhFibonacci(amount):
    num, num2, counter, fibSeq = 0, 1, 0, [0]
    for i in range(amount):
        if counter % 2:
            num += num2
            fibSeq.append(num)
        else:
            num2 += num
            fibSeq.append(num2)
        counter += 1
    return fibSeq

# ^^ this is hella goofy smh, better way to alternate variables is below where instead of a counter, you use a
# greater than operator


def fib(amount):
    num, num2, fibSeq = 0, 1, [0, 1]
    for i in range(amount):
        if num2 > num:
            num += num2
            fibSeq.append(num)
        else:
            num2 += num
            fibSeq.append(num2)
    return fibSeq


def fibNthTerm(term):
    return fib(term)[term - 1]


def sumOfFib(nums):
    total = 0
    for num in fib(nums):
        total += num
    return total


print(fib(int(input(">> "))))
"""print(fibNthTerm(int(input(">> "))))"""
"""print(sumOfFib(int(input(">> "))))"""
