import random
a = [list()]
b = [[random.randint(0,1) for i in range(3)] for j in range(3)]
c = a + b
print(c)
