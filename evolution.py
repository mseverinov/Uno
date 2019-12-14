import random
import time
from collections import deque
from deap import base
from deap import creator
from deap import tools

import multiprocessing
import worker

import matplotlib.pyplot as plt

import numpy

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
        #write results to a file
        #random include or drop various nodes to determine which are necesarry?
        #implement graphing of results
        #visualize what the w/l ratio of a single parameter set is across generations. is it consistent? how much so?
        #simultaniuis side evolution to improve accuracy of improvement
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

class Evo:

    def __init__(self):
        self.nActors = 50
        self.nParameters = 49
        self.nGames = 400
        self.nGen = 200
        self.parmRange = 10

    def deapSetup(self, fitnessCheck):
        # deap class creation
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox() #toolbox container contains the individual, the population, as well as : functions, operators, and arguements
        self.toolbox.register("evaluate", fitnessCheck, self.nGames)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("zeroMutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("gausMutate", tools.mutGaussian, mu=0, sigma=.5, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # creating our population container
        # self.toolbox.register("attr_bool", self.zeroFoo)
        self.toolbox.register("attr_bool", random.randint, -self.parmRange, self.parmRange)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.nParameters) #initReapeat calsl the function container with a generator function corresponding to the calling n times the function .
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual) #create a population contains unfixed amount of individuals

        self.pool = multiprocessing.Pool()
        self.toolbox.register("starmap_async", self.pool.starmap_async)

        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        self.CXPB, self.MUTPB = 0.5, 0.2

        # Objects that will compile the data
        self.fbest = numpy.ndarray((self.nGen, ))
        self.std = numpy.ndarray((self.nGen, self.nParameters))

    def mainLoop(self, fitnessCheck, gameLoop, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass):
        start = 0
        end = 0
        self.iteration = -1

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        halloffame = tools.HallOfFame(1)
        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "std", "min", "avg", "max"
        self.deapSetup(fitnessCheck)

        population = self.toolbox.population(n=self.nActors)
        fStart = time.time()
        self.poolfoo(population, fitnessCheck, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass)
        fEnd = time.time()
        self.fInterval = fEnd-fStart

        for i in range(self.nGen):
            self.iteration += 1
            start = time.time()

            # tournament selection used in this method removes lower fitness individuals
            offspring = self.toolbox.select(population, len(population))  # selects top individual from 3 randomly chosen with replacemnt, as many times as there are members in the population
            offspring = list(map(self.toolbox.clone, offspring))  # Clone creates a copy of each individual so our new list does not reference the prior generation of individuals

            # self.crossBreed(offspring)

            self.gausMutation(offspring)
            # self.zeroMutation(offspring)
            # self.comboMutation(offspring)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]  #the invalid marking saves processing resources
            self.poolfoo(invalid_ind, fitnessCheck, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass)
            population[:] = offspring  # replace old population with new population

            halloffame.update(population)
            record = stats.compile(population)
            self.logbook.record(evals=len(population), gen=self.iteration, **record)
            self.fbest[self.iteration] = halloffame[0].fitness.values[0]
            self.std[self.iteration] = numpy.std(population)

            end = time.time()
            print('it:', self.iteration, 'time:', int(end-start))
            self.calcStats(population)
            print()
        self.plotstuff()

    def calcStats(self, population):
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

    def poolfoo(self, population, fitnessCheck, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass):
        # return_dict = manager.dict()
        # it = [(fitnessCheck, list(population[i]), self.nGames, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass, return_dict, i) for i in range(len(population))]
        # self.toolbox.starmap(worker.worker, it)
        # for i in range(len(population)):
        #     population[i].fitness.values = [return_dict[i]]
        it = [(fitnessCheck, list(population[i]), self.nGames, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass) for i in range(len(population))]
        try:
            fits = self.toolbox.starmap_async(worker.worker, it).get(timeout=self.fInterval)
        except:
            fits = self.toolbox.starmap_async(worker.worker, it).get(timeout=self.fInterval)
        # self.toolbox.poolclose()
        # self.toolbox.pooljoin()
        for i in range(len(population)):
            population[i].fitness.values = [fits[i]]



    def processfoo(self, manager, population, fitnessCheck, Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass):
        return_dict = manager.dict()
        jobs = []
        for i in range(len(population)):
            p = self.toolbox.process(target=worker.worker, args=(fitnessCheck, population[i], Cardclass, DrawPileclass, DiscardPileclass, Gameclass, Playerclass, return_dict, i))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        for i in range(len(population)):
            population[i].fitness.values = [return_dict[i]]

    def plotstuff(self):
        x = list(range(self.nGen))
        avg, max_, min_ = self.logbook.select("avg", "max", "min")
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.semilogy(x, avg, "-b")
        plt.semilogy(x, max_, "-r")
        plt.semilogy(x, min_, "--b")
        # plt.semilogy(x, self.fbest, "-c")
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
