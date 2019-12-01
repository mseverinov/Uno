import random
a = [i for i in range(10)]
b = []
for i in range(10):
    b.append(a.copy())
    print(b)
    random.shuffle(b[-1])

print(b)
