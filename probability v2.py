n = 25 #number of success cards in pool
N = 108 #total number of cards in pool
M = 7 #hand size
m = 7 #number of success in hand

def handProb(m, M, n, N):
    """Probability the m success are in opponent's hand

    m := number of success cards drawn
    M := hand size
    n := # of success cards in pool
    N := # of cards in pool """
    succEvents = 1
    for i in range(m):
        succEvents *= n-i

    failEvents = 1
    for i in range(M-m):
        failEvents *= N - n - i

    totalEvents = 1
    for i in range(M):
        totalEvents *= N - i

    combinations = 1
    for i in range(1,M):
        combinations += i*(M - i)
    print(succEvents, failEvents, totalEvents, combinations)

    return succEvents * failEvents / totalEvents * combinations

for m in range(8):
    print(handProb(m, M, n, N))
