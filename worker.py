import main


def fitnessCheck(parameters, nGames, return_dict):
    return_dict[parameters] = sum([gameLoop(parameters) for i in range(nGames)])


# def multiprocessing_func(procnum, return_dict):
#     a = [i for i in range(10000)]
#     for i in range(10):
#         random.shuffle(a)
#     return_dict[procnum] = a.copy()
#     if i % 10 == 0: print(i)
