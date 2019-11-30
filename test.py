import random
a = [(i, random.randint(1,100)) for i in range(100)]
print(sorted(a,key = lambda x: x[1], reverse = True))

sorted
