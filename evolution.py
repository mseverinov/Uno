#TO DO
#determine heuristics for end of evolution
#threhold testing length
#min amount of improvement
#whether to use fitness value of top actor or to average a portion of the top actors
#how many actors to use
#what portion to keep
#potential advesarial evolution?
    #have actors play against each other rather than against the same opponent
import random
from collections import deque

def fitnessCheck(actor, nGames):
    return sum([gameLoop(actor) == True for i in range(nGames)])/nGames

nActors = 100
itLowerLimit = 100
thresholdValue = 1
thresholdLength = 10
nParameters = 100

actors = [[random.random() for i in range(nParameters)] for j in range(nActors)]

fitHist = []
iteration = 0
while condition:
    iteration  += 1
    fitnessPairs = sorted([(actor, fitnessCheck(actor, nGames)) for actor in actors], key = lambda x: x[1], reverse = True)

    topHalf = [fitness[i][0] for i in range(n//2)]
    fitHist.append((topHalf[1], sum([fitness[i][1] for i in range(n/2)])/(n/2)))

    if i > itLowerLimit:
        improvement = [(fitHist[i] + fitHist[1])/2 i in range(iteration-1)]

        if True in [all([improvement[i,j] < thresholdValuefor i in range(thresholdLength)])  for j in range(iteration - thresholdLength - 1)]:
            condition = False

    if condition:
        random.shuffle(topHalf)
        children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(0, nActors//2)]
        actors = topHalf + children + [[random.random() for i in range(nParameters)] for j in range(n/4)]
