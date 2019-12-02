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

class Evo:
    nActors = 160
    itLowerLimit = 100
    thresholdValue = 1
    thresholdLength = 100
    nParameters = 49
    nGames = 500
    parmRange = 100
    nKeep = 2
    #better actors make more children?
    #add mutation rate?
    #lock parameters which have equilibriated
    #perhaps unlock and relock over time
    #clustering algorithim
    #rather than having a coefficient for all possible functional forms, randomize the choice of functional
        #only cross breed species with matching functional forms
        #mutuate children from loners
    #give opposing players parameters from other actors
    #multi threading
    #analyze differences in parameters of time for differerent portions of the top
    #write results to a file
    #increase number of games to test over as iteration number increases
    #discard any actors that perform below average, especially in the beginining
        #each generation keep above average until carry over cap reached
    #do parents need to be retested generation after generation?
    #in cross breeding explore other avenues besides averaging all values
        #some averages
        #some crossovers
        #some mutations
            #any ways to think about what an optimal coefficent of the above would be?
    #random include or drop various nodes to determine which are necesarry?
    #implement graphing of results
    #visualize what the w/l ratio of a single parameter set is across generations. is it consistent? how much so?


    #Monday
        #label and group results in viewing

    #Tuesday
        #simultanios side evolution

    #Wednesday
        #incorperate w/l multigenerational record

    #Thursday
        #probabilistic fitness matching for cross breeding

    def __init__(self):

        # actors = [[1 for i in range(nParameters)] for j in range(nActors)]
        # actorHistory = {tuple(actor):(0,0) for actor in actors}
        self.fitHist = []
        # fitAvgMax = 0
        # improvIndex = 0
        self.avgActorHist = []


    def mainLoop(self):
        start = 0
        end = 0
        iteration = 0
        continueCond = True
        self.actors = createRandActors(self, nActors)
        while continueCond:
            start = time.time()
            print('it:', iteration, 'time:', int(end-start))
            iteration += 1

            fitPairs = sorted([(actor, fitnessCheck(actor, self.nGames)) for actor in self.actors], key = lambda x: x[1], reverse = True)
            avg, quartAvg, halfAvg, cumAvg = calcStats(self, fitPairs)
            # actorHistoryN = {}
            # for pair in fitPairs[:nActors//nKeep]:
            #     tActor = tuple(pair[0])
            #     if tActor in actorHistory:
            #         actorHistoryN[tActor] = (pair[1] + actorHistory[tActor][0], nGames + actorHistory[tActor][1])
            #     else:
            #         actorHistoryN[tActor] = (pair[1], nGames)
            # actorHistory = actorHistoryN
            if self.nActors//4 > 20:
                step = (self.nActors//4)//20
            else:
                step = 1
            print([fitPairs[i][1] for i in range(0, self.nActors//4, step)], avg, str(quartAvg), str(halfAvg), str(cumAvg))
            # avgActor = [sum([fitPairs[i][0][j] for i in range(nActors//nKeep//2)])/(nActors/nKeep/2) for j in range(nParameters)]
            # avgActorHist.append(avgActor)
            # print([top[0]])
            # print([sum([avgActorHist[i][j] for i in range(len(avgActorHist))])//len(avgActorHist) for j in range(nParameters)])
            if self.endCheck(iteration):
                return top[0]

            nNewActors = 3*self.nActors//8
            actors = top + createChildren(parents) + createRandActors(nNewActors)
            end = time.time()


    def createRandActors(self, n):
        # return [[random.random() for i in range(nParameters)] for j in range(n)]
        return [[random.randint(-1*self.parmRange, self.parmRange) for i in range(self.nParameters)] for j in range(n)]


    def createChildren(self, parents):
        # random.shuffle(parents)
        children = []
        for i in range(0, nActors//(nKeep*2), 2):
            actor = []
            for j in range(nParameters):
                actor.append((parents[i][j] + parents[i+1][j])/2)
            children.append(actor)
        # print(children)
        # children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(nActors//2)]
        # actors = top + children + [[random.random() for i in range(nParameters)] for j in range(5*nActors//8)]
        return children


    def calcStats(self, fitPairs):
        top = [fitPairs[i][0] for i in range(self.nActors//self.nKeep)]
        avg = sum([fitPairs[i][1] for i in range(self.nActors//self.nKeep//2)])/(self.nGames*self.nActors/self.nKeep/2/4)
        self.fitHist.append(avg)

        cumAvg = sum(self.fitHist)/len(self.fitHist)
        half = self.fitHist[len(self.fitHist)//2:]
        halfAvg = sum(half)/(len(half))
        quart = self.fitHist[len(self.fitHist)//4:]
        quartAvg = sum(quart)/(len(quart))

        return avg, quartAvg, halfAvg, cumAvg

    def endCheck(self,iteration):
        if iteration > itLowerLimit:
            return True
        else:
            return False

            # if runningAvg > fitAvgMax + thresholdValue:
            #     fitAvgMax = runningAvg
            #     improvIndex = iteration
            #
            # if iteration - improvIndex > thresholdLength:
            #     return top[0]
