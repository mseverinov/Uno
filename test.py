import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

#evaluation operator
def evalOneMax(individual):
    return sum(individual)


def setup():
    #all defined classes part of creator container
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax, strategy=None)
    creator.create("Strategy", list)

    #toolbox container contains the individual, the population, as well as : functions, operators, and arguements
    toolbox = base.Toolbox()

    #to add stuff .register() method
    #to remove stuff .unregister() method
    #registering stuff to the toolbox freezes their arguements
        #this can be used to freeze some arguement so we only need to pass the changing ones when calling
    #the first arguement is the container
    toolbox.register("attr_bool", random.randint, 10, 99) #creates the generator toolbox.attr_bool() it is composed of the randint() function with arguements frozen to 0 & 1
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 10) #creates an individual that has had the initReap method applied to it 100 times
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #create a population contains unfixed amount of individuals

    #the operators required for our evolution
    toolbox.register("evaluate", evalOneMax)
    toolbox.register("evaluate", benchmarks.sphere)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutESLogNormal, c=1.0, indpb=0.03)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

def main():
    random.seed()
    MU, LAMBDA = 10, 100
    pop = toolbox.population(n=MU)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    hof = tools.HallOfFame(1)
    for i in pop:
        i.strategy = creator.Strategy(random.uniform(.5, 3) for _ in range(10))
    # for i in pop:
    #     toolbox.mutate(i)

    pop, logbook = algorithms.eaMuCommaLambda(pop, toolbox, mu=MU, lambda_=LAMBDA, cxpb=0.6, mutpb=0.3, ngen=500, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

toolbox = setup()
x,y,z = main()
for i in [x,y,z]:
    for j in i:
        print(j)
