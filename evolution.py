import random
import time
from collections import deque
from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import multiprocessing
import worker

import matplotlib.pyplot as plt

import numpy
#graph individual parameters
#strategy evolution
#similarity function

    #THOUGHTS IDEAS ECT
        #rather than having a coefficient for all possible functional forms, randomize the choice of functional
            #only cross breed species with matching functional forms
            #mutuate children from loners
        #give opposing players parameters from other actors
        #write results to a file
        #random include or drop various nodes to determine which are necesarry?
        #implement graphing of results
        #visualize what the w/l ratio of a single parameter set is across generations. is it consistent? how much so?
        #simultaniuis side evolution to improve accuracy of improvement
        #probabilistic fitness matching for cross breeding

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

class Evo:

    def __init__(self, nActors = 0, nGames = 0, sigma = 0, complexity = None):
        if nActors != 0:
            self.nActors = nActors
        else:
            self.nActors = 50
        if nGames != 0:
            self.nGames = nGames
        else:
            self.nGames = 1000
        if sigma != 0:
            self.sigma = sigma
        else:
            self.sigma = .5
        if complexity != None:
            self.complexity = complexity
        else:
            self.complexity = {'bot hand only':False, 'positive only':False, 'direct only':False, 'color':True}
        self.nParameters = 53
        self.nGen = 25
        self.parmRange = 10
        self.fInterval = self.nGames*self.nActors/1

    def deapSetup(self, fitnessCheck):
        # deap class creation
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax, statFit=None)

        self.toolbox = base.Toolbox() #toolbox container contains the individual, the population, as well as : functions, operators, and arguements
        self.toolbox.register("evaluate", fitnessCheck, self.nGames)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("zeroMutate", tools.mutFlipBit, indpb=0.025)
        self.toolbox.register("gausMutate", tools.mutGaussian, mu=0, sigma=self.sigma, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # creating our population container
        # self.toolbox.register("attr_bool", self.zeroFoo)
        self.toolbox.register("attr", random.randint, -self.parmRange, self.parmRange)
        self.toolbox.register("individual", self.initES, creator.Individual, self.toolbox.attr, self.nParameters) #initReapeat calsl the function container with a generator function corresponding to the calling n times the function .
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual) #create a population contains unfixed amount of individuals

        self.pool = multiprocessing.Pool()
        self.toolbox.register("starmap_async", self.pool.starmap_async)
        self.toolbox.register('poolclose', self.pool.close)

        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        self.CXPB, self.MUTPB = 0.1, 0.2

        # Objects that will compile the data
        self.fbest = numpy.ndarray((self.nGen, ))
        self.std = numpy.ndarray((self.nGen, self.nParameters))

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.halloffame = tools.HallOfFame(self.nActors)
        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "std", "min", "avg", "max"

    def mainLoop(self, fitnessCheck, gameLoop, classDict, recordHistorys):
        self.deapSetup(fitnessCheck)

        start = 0
        end = 0
        self.iteration = -1

        population = self.toolbox.population(n=self.nActors)
        fStart = time.time()
        fits = self.poolfoo(population, fitnessCheck, classDict)
        fEnd = time.time()


        # if fEnd-fStart < 60:
        #     self.fInterval = fEnd-fStart
        # else:
        #     print('problem')
        # print(self.fInterval, time.ctime(time.time()))
        # statFits = self.poolfoo(population, fitnessCheck, classDict, True)

        for i in range(len(population)):
            population[i].fitness.values = [fits[i]]
            # population[i].statFit = statFits[i]
        self.halloffame.update(population)
        if recordHistorys: genHistory = [numpy.average(numpy.array([ind for ind in population]), axis=0)]

        for i in range(self.nGen):
            self.iteration += 1
            start = time.time()
            # offspring = self.toolbox.select(population, len(population))  # selects top individual from 3 randomly chosen with replacemnt, as many times as there are members in the population
            offspring = self.toolbox.select(self.halloffame, self.nActors)  # selects top individual from 3 randomly chosen with replacemnt, as many times as there are members in the population
            offspring = list(map(self.toolbox.clone, offspring))  # Clone creates a copy of each individual so our new list does not reference the prior generation of individuals

            # self.gausMutation(offspring)
            # self.zeroMutation(offspring)
            self.comboMutation(offspring)
            self.crossBreed(offspring)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fits = self.poolfoo(invalid_ind, fitnessCheck, classDict)
            # statFits = self.poolfoo(invalid_ind, fitnessCheck, classDict, True)
            for i in range(len(invalid_ind)):
                invalid_ind[i].fitness.values = [fits[i]]
                # invalid_ind[i].statFit = statFits[i]

            population[:] = offspring  # replace old population with new population
            self.halloffame.update(population)
            record = self.stats.compile(population)
            self.logbook.record(evals=len(population), gen=self.iteration, **record)
            # self.fbest[self.iteration] = halloffame[0].fitness.values[0]
            self.std[self.iteration] = numpy.std(population)
            end = time.time()

            if recordHistorys: genHistories.append(numpy.average(numpy.array([ind for ind in population]), axis=0))


            # print('it:', self.iteration, 'time:', int(end-start))
            # self.calcStats(population)
            # print()
        # self.plotstuff()
        self.toolbox.poolclose()

        if recordHistorys:
            return self.logbook, genHistories
        return self.logbook, None

    def calcStats(self, population):
        # fits = [ind.statFit for ind in population]
        fits = [ind.fitness.values[0] for ind in population]
        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    def zeroMutation(self, offspring):
        for mutant in offspring:
            if random.random() < self.MUTPB:
                self.toolbox.zeroMutate(mutant)
                del mutant.fitness.values

    def gausMutation(self, offspring): #change mu & sigma to be related tp how far the parameter is from zero
        for mutant in offspring: # also sigma should decrease with iteration numnber
            if random.random() < self.MUTPB:
                self.toolbox.gausMutate(mutant)
                del mutant.fitness.values

    def comboMutation(self, offspring):
        for mutant in offspring:
            if random.random() < self.MUTPB:
                self.toolbox.gausMutate(mutant)
                self.toolbox.zeroMutate(mutant)
                del mutant.fitness.values

    def crossBreed(self, offspring):
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.CXPB:
                self.toolbox.mate(child1, child2)  # are child1 & child2 modified? are they the parents? do they become the children? are the both?
                del child1.fitness.values
                del child2.fitness.values

    def poolfoo(self, population, fitnessCheck, classDict, evoStrat = True):
        if not evoStrat:
            argIt = []
            for i in range(len(population)):
                parameters = [[list(population[i])] + [list(ind) for ind in self.toolbox.select(population, 3)]]
                argIt.append((fitnessCheck, parameters, self.nGames, classDict))
        else:
            argIt = [(fitnessCheck, [list(population[i])] + [[0 for _ in range(self.nParameters)] for _ in range(3)], self.nGames, classDict, self.complexity) for i in range(len(population))]
        condition = True
        while condition:
            try:
                fits = self.toolbox.starmap_async(worker.worker, argIt).get(timeout=self.fInterval)
                condition = False
            except multiprocessing.TimeoutError:
                print('TimedOut')
        return fits

    def plotstuff(self):
        x = list(range(self.nGen))
        avg, max_, min_ = self.logbook.select("avg", "max", "min")
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.semilogy(x, avg, "--b")
        plt.semilogy(x, max_, "-r")
        plt.semilogy(x, min_, "-r")
        plt.grid(True)
        plt.title("blue: f-values, green: sigma, red: axis ratio")

        # plt.subplot(2, 2, 2)
        # plt.plot(x, self.best)
        # plt.grid(True)
        # plt.title("Object Variables")

        plt.subplot(1, 2, 2)
        plt.semilogy(x, self.std)
        plt.grid(True)
        plt.title("Standard Deviations in All Coordinates")
        plt.show()

    def initES(self, icls, func, size):
        ind = icls(random.randint(not(self.complexity['positive only'])*-self.parmRange, self.parmRange) for _ in range(size))
        ind.fStat = 0
        return ind
