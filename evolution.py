import random
import time
from collections import deque
from deap import base
from deap import creator
from deap import tools



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

class Evo:

    def __init__(self):
        self.fitHist = []
        self.avgActorHist = []
        self.nActors = 8
        self.itLowerLimit = 5
        self.thresholdValue = 1
        self.thresholdLength = 15
        self.nParameters = 49
        self.nGames = 100
        self.parmRange = 100
        self.nKeep = 2

    def deapSetup(self, fitnessCheck):
        # deap class creation
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox() #toolbox container contains the individual, the population, as well as : functions, operators, and arguements
        self.toolbox.register("evaluate", fitnessCheck, self.nGames)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("zeroMutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("gausMutate", tools.mutGaussian, mu=0, sigma=10, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # creating our population container
        # self.toolbox.register("attr_bool", self.zeroFoo)
        self.toolbox.register("attr_bool", random.randint, -self.parmRange, self.parmRange)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.nParameters) #initReapeat calsl the function container with a generator function corresponding to the calling n times the function .
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual) #create a population contains unfixed amount of individuals

        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        self.CXPB, self.MUTPB = 0.5, 0.2

    def mainLoop(self, fitnessCheck):
        start = 0
        end = 0
        iteration = 0
        continueCond = True

        population = self.toolbox.population(n=self.nActors)
        fitnesses = list(map(self.toolbox.evaluate, population))  # Evaluates the entire population
        for ind, fit in zip(population, fitnesses):
            fit = [fit]
            ind.fitness.values = fit

        fits = [ind.fitness.values[0] for ind in population]

        while continueCond:
            print('it:', iteration, 'time:', int(end-start))
            start = time.time()
            iteration += 1
            # tournament selection used in this method removes lower fitness individuals
            offspring = self.toolbox.select(population, len(population))  # selects top individual from 3 randomly chosen with replacemnt, as many times as there are members in the population
            offspring = list(map(self.toolbox.clone, offspring))  # Clone creates a copy of each individual so our new list does not reference the prior generation of individuals

            self.crossBreed(offspring)

            # self.gausMutation(offspring)
            # self.zeroMutation(offspring)
            # self.comboMutation(offspring)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]  #the invalid marking saves processing resources
            fitnesses = map(self.toolbox.evaluate, invalid_ind) # Evaluate the individuals with an invalid fitness
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = [fit]

            population[:] = offspring  # replace old population with new population

            fits = [ind.fitness.values[0] for ind in population]
            self.calcStats(population, fits)
            print()
            end = time.time()

    def calcStats(self, population, fits):
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
        for mutant in offspring:    #also sigma should decrease with iteration numnber
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
