def multIt(it):
    t = 1
    for i in it:
        t *= i
    return t


def pColorDist(color):
    dist = []
    for n in range(1,8):
        if n == 7:
            print('x')
        dist.append(colorDistRecurs(0, 1, n))
    return dist


def colorDistRecurs(iteration, depth, n):
    start = iteration + depth
    end = 7 - n + depth
    if n == 6:
        print(start, end)
    #n is number of successes
    pT = 0
    for iteration, i in enumerate(range(start, end + 1)): #index of success
        if end == 7:
            sLst = [m for m in range(26-n, 26)]
            successNum = multIt(sLst)
            # for m in range(26-n, 26):
            #     #as many successes as n
            #     successNum *= m
            fLst = [m for m in range(84-i+n,84)]
            failNum = multIt(fLst)
            # for m in range(84-i+n,84):
            #     failNum *= m
            dLst = [m for m in range(109-i, 109)]
            denom = multIt(dLst)
            # for m in range(109-i, 109):
            #     denom *= m
            pi = successNum*failNum/denom
            # print(pi)
            if n == 6:
                print(pi, n, i)
                print(sLst, fLst, dLst)
                print(start, end)
                # raise
        else:
            pi = colorDistRecurs(iteration, depth + 1, n)
        pT += pi
    return pT


    def pColorNonRecurs(color):
        dist = []
        for n in range(1,8):
            pn = 0
            indicies = [i for i in range(1,1+n)]:
            while condition:
                sLst = [m for m in range(26-n, 26)]
                successNum = multIt(sLst)

                fLst = [m for m in range(84-indicies[-1]+n,84)]
                failNum = multIt(fLst)

                dLst = [m for m in range(109-indicies[-1], 109)]
                denom = multIt(dLst)

                pn += successNum*failNum/denom

                indicies[-1] += 1

                i = n-1
                cond2 = True
                while cond2:
                    if indicies[i] > 7:
                        indicies[i] = indicies[i-1] + 2
                        indicies[i-1] += 1
                    i -= 1
