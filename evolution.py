import random
import time
from collections import deque
import multiprocessing
from deap import base
from deap import creator
from deap import tools

class Evo:
    nActors = 8
    itLowerLimit = 5
    thresholdValue = 1
    thresholdLength = 15
    nParameters = 49
    nGames = 100
    parmRange = 100
    nKeep = 2
    #THOUGHTS IDEAS ECT
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
        #simultaniuis side evolution to improve accuracy of improvement
        #evo -> stand alone
        #label and group results in viewing
        #incorperate w/l multigenerational record
        #attempt 10 games, 8000 actors
        #probabilistic fitness matching for cross breeding

    #Priority 1
        #SPEED UP UNO GAME SIMULATION!!
            #create list/set of valid moves for every card at the beginning of simulation
            #Potential Solution 1: Vectorize
                #use numpy to multiply binary vectors to find crossover
                #this will require significantly longer lists. Will the speed up overcome this?
            #Potential Solution 2
                #Use set comparision to do the same thing
                #which cards in hand are in set that contains all valid move for the card on top of the discard pile

    #Priority 2
        #rewrite current evolution algorithim using DEAP library

    #Priority 3
        #implement randomization of node function,
            #remove unnessary parameters
            #determine how this will be incorperated into evolution
            #functions:
                # x
                # 1/x
                # + vs - ?
                # x^2
                #combinations of the above



    def __init__(self):

        # actors = [[1 for i in range(nParameters)] for j in range(nActors)]
        # actorHistory = {tuple(actor):(0,0) for actor in actors}
        self.fitHist = []
        # fitAvgMax = 0
        # improvIndex = 0
        self.avgActorHist = []

    def deapSetup(self, fitnessCheck):
        # deap class creation
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox() #toolbox container contains the individual, the population, as well as : functions, operators, and arguements
        self.toolbox.register("evaluate", fitnessCheck)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # creating our population container
        self.toolbox.register("attr_bool", random.random)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, self.nParameters) #initReapeat calsl the function container with a generator function corresponding to the calling n times the function .
        self.toolbox.register("population", tools.initRepeat, list, toolbox.individual) #create a population contains unfixed amount of individuals

    def mainLoop(self, fitnessCheck):
        start = 0
        end = 0
        iteration = 0
        continueCond = True
        # self.actors = self.createRandActors(self.nActors)

        population = self.toolbox.population(n=self.nActors)
        fitnesses = list(map(self.toolbox.evaluate, population))  # Evaluates the entire population
        for ind, fit in zip(population, fitnesses):
            fit = [fit]
            ind.fitness.values = fit
        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        CXPB, MUTPB = 0.5, 0.2
        fits = [ind.fitness.values[0] for ind in population]

        while continueCond:
            print('it:', iteration, 'time:', int(end-start))
            start = time.time()
            iteration += 1

            offspring = self.toolbox.select(population, len(population))  # selects all individuals in the population
            offspring = list(map(self.toolbox.clone, offspring))  # Clone creates a copy of each individual so our new list does not reference the prior generation of individuals

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)  # are child1 & child2 modified? are they the parents? do they become the children? are the both?
                    del child1.fitness.values  # why delete these
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)  # modifes the individual in place
                    del mutant.fitness.values

            population[:] = offspring  # replace old population with new population

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in population]

            length = len(population)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)

            # fitPairs = sorted([(actor, fitnessCheck(actor, self.nGames)) for actor in self.actors], key = lambda x: x[1], reverse = True)
            # avg, quartAvg, halfAvg, cumAvg = self.calcStats(fitPairs)
            # actorHistoryN = {}
            # for pair in fitPairs[:nActors//nKeep]:
            #     tActor = tuple(pair[0])
            #     if tActor in actorHistory:
            #         actorHistoryN[tActor] = (pair[1] + actorHistory[tActor][0], nGames + actorHistory[tActor][1])
            #     else:
            #         actorHistoryN[tActor] = (pair[1], nGames)
            # actorHistory = actorHistoryN
            # if self.nActors//4 > 20:
            #     step = (self.nActors//4)//20
            # else:
            #     step = 1
            # print([fitPairs[i][1] for i in range(0, self.nActors//4, step)], avg, str(quartAvg), str(halfAvg), str(cumAvg))
            # # avgActor = [sum([fitPairs[i][0][j] for i in range(nActors//nKeep//2)])/(nActors/nKeep/2) for j in range(nParameters)]
            # # avgActorHist.append(avgActor)
            # # print([top[0]])
            # # print([sum([avgActorHist[i][j] for i in range(len(avgActorHist))])//len(avgActorHist) for j in range(nParameters)])
            # top = [fitPairs[i][0] for i in range(self.nActors//2)]
            # if self.endCheck(iteration):
            #     return top[0]
            #
            # nNewActors = 3*self.nActors//8
            # actors = top + self.createChildren(top) + self.createRandActors(nNewActors)
            # end = time.time()


    def createRandActors(self, n):
        # return [[random.random() for i in range(nParameters)] for j in range(n)]
        return [[random.randint(-1*self.parmRange, self.parmRange) for i in range(self.nParameters)] for j in range(n)]


    def createChildren(self, parents):
        # random.shuffle(parents)
        children = []
        for i in range(0, self.nActors//(self.nKeep*2), 2):
            actor = []
            for j in range(self.nParameters):
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
        if iteration > self.itLowerLimit:
            return True
        else:
            return False

            # if runningAvg > fitAvgMax + thresholdValue:
            #     fitAvgMax = runningAvg
            #     improvIndex = iteration
            #
            # if iteration - improvIndex > thresholdLength:
            #     return top[0]
