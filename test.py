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
