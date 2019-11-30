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
from main import *
from collections import deque


def fitnessCheck(actor, nGames):
    bot = Player()
    Player.bot = bot
    p2 = Player()
    p3 = Player()
    p4 = Player()
    Game.createCards()

    return sum([main.gameLoop(actor) for i in range(nGames)])


def evo():
    nActors = 20
    itLowerLimit = 10
    thresholdValue = 1
    thresholdLength = 10
    nParameters = 100
    nGames = 100

    actors = [[random.random() for i in range(nParameters)] for j in range(nActors)]

    fitHist = []
    iteration = 0
    condition = True
    while condition:
        iteration += 1
        fitPairs = sorted([(actor, fitnessCheck(actor, nGames)) for actor in actors], key = lambda x: x[1], reverse = True)

        topHalf = [fitPairs[i][0] for i in range(nActors//2)]
        t = sum([fitPairs[i][1] for i in range(nActors/2)])
        avg = t/(nActors/2)
        tup = (fitPairs[0][1], avg)
        fitHist.append(tup)

        if iteration > itLowerLimit:
            improvement = [(fitHist[i] + fitHist[1])/2 for i in range(iteration-1)]

            #history only needs to be checked for the last thresholdLength values
            #currently checking all values each iteration
            if True in [all([improvement[i, j] < thresholdValue for i in range(thresholdLength)])  for j in range(iteration - thresholdLength - 1)]:
                return fitPairs[0][0]

        random.shuffle(topHalf)
        children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(0, nActors//2)]
        actors = topHalf + children + [[random.random() for i in range(nParameters)] for j in range(nActors/4)]
