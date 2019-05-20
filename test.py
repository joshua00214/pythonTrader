import sys

x = 1
def test():
    global x
    x += 1


test()
print(x)