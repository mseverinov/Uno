<<<<<<< HEAD
from collections import deque


a = deque()
a.append(1)
print(a)
=======
m = 1
M = 1
def combos(m, M):
    combinations = 1
    for i in range(1,m+1):
        combinations += i*(M - i)
    return combinations

for m in range(1, 6):
    for M in range(m, 6):
        print('m: ' + str(m), 'M: ' + str(M), 'combos: ' + str(combos(m, M)))
>>>>>>> 3f0c7071fd86a3d140c5c135d964675e48b71d8b
