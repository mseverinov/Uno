import random

from deap import base
from deap import creator
from deap import tools

#evaluation operator
def evalOneMax(individual):
    return sum(individual)


def main():
    pop = toolbox.population(n=300) #creates our population, this is why n was not fixed earlier

    fitnesses = list(map(toolbox.evaluate, pop)) # Evaluates the entire population
    for ind, fit in zip(pop, fitnesses):
        fit = [fit]
        # print(ind.fitness.values, fit)
        ind.fitness.values = fit #used the fitness attribute we created earlier, assignes the generated fit value to it
        # print(ind.fitness.values, fit)
    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2


    fits = [ind.fitness.values[0] for ind in pop] # Extracting all the fitnesses

    g = 0 # Variable keeping track of the number of generations
    while max(fits) < 100 and g < 1000: # Begin the evolution
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        offspring = toolbox.select(pop, len(pop)) #selects all individuals in the population
        offspring = list(map(toolbox.clone, offspring)) # Clone creates a copy of each individual so our new list does not reference the prior generation of individuals

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2) #are child1 & child2 modified? are they the parents? do they become the children? are the both?
                del child1.fitness.values #why delete these
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant) #modifes the individual in place
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]  #the invalid marking saves processing resources
        fitnesses = map(toolbox.evaluate, invalid_ind) # Evaluate the individuals with an invalid fitness
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = [fit]

        pop[:] = offspring #replace old population with new population

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)






#all defined classes part of creator container
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

#toolbox container contains the individual, the population, as well as : functions, operators, and arguements
toolbox = base.Toolbox()

#to add stuff .register() method
#to remove stuff .unregister() method
#registering stuff to the toolbox freezes their arguements
    #this can be used to freeze some arguement so we only need to pass the changing ones when calling
#the first arguement is the container
toolbox.register("attr_bool", random.randint, 0, 1) #creates the generator toolbox.attr_bool() it is composed of the randint() function with arguements frozen to 0 & 1
toolbox.register("individual", tools.initRepeat, creator.Individual,toolbox.attr_bool, 100) #creates an individual that has had the initReap method applied to it 100 times
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #create a population contains unfixed amount of individuals

#the operators required for our evolution
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

main()
