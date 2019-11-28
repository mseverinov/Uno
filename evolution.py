#TO DO
#determine heuristics for end of evolution
#threhold testing length
#min amount of improvement
#whether to use fitness value of top actor or to average a portion of the top actors
#how many actors to use
#what portion to keep



import random

n = 100
itLowerLimit = 100
thresholdValue = 1
thresholdLength = 10

actors = [create(actor) for i in range(n)]
fitHist = []
iteration = 0
while condition:
    iteration  += 1
    fitnessPairs = sorted([(actor, evalFunction(actor)) for actor in actors], key = lambda x: x[1], reverse = True)

    topHalf = [fitness[i][0] for i in range(n//2)]
    fitHist.append((topHalf[1], sum([fitness[i][1] for i in range(n/2)])/(n/2)))

    if i > itLowerLimit:
        improvement = [(fitHist[i] + fitHist[1])/2 i in range(iteration-1)]

        if True in [all([improvement[i,j] < thresholdValuefor i in range(thresholdLength)])  for j in range(iteration - thresholdLength - 1)]:
            condition = False

    if condition:
        random.shuffle(topHalf)
        actorPairs = [(topHalf[i], topHalf[i+1]) for i in range(0,n/2,2)]
        children = [[(valuePair[0]+valuePair[1])/2 for valuePair in zip(actorPair[0], actorPair[1])] for actorPair in actorPairs]]
        actors = actorPairs + children + [create(actor) for i in range(n/4)]
