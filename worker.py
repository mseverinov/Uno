# import main
import math
from collections import deque
import random

def worker(fitnessCheck, parameters, nGames, classDict, complexity):
    CardClass = classDict['Card']
    DrawPileClass = classDict['DrawPile']
    DiscardPileClass = classDict['DiscardPile']
    PlayerClass = classDict['Player']
    playerInst = PlayerClass(None, container = True)
    bot = PlayerClass(parameters[0], complexity = complexity)
    playerInst.all_.append(bot)
    playerInst.bot = bot
    p2 = PlayerClass(parameters[1])
    playerInst.all_.append(p2)
    p3 = PlayerClass(parameters[2])
    playerInst.all_.append(p3)
    p4 = PlayerClass(parameters[3])
    playerInst.all_.append(p4)

    nPlayers = len(playerInst.all_)
    gameInst = classDict['Game']()
    gameInst.nPlayers = nPlayers
    cardInst = CardClass('', 0, 0, True, True)
    cardInst.createCards()
    gameInst.decks = gameInst.deckGen(cardInst)

    discardPileInst = DiscardPileClass()
    drawPileInst = DrawPileClass()

    # return_dict[itNum] = fitnessCheck(parameters, nGames, cardInst, discardPileInst, drawPileInst, gameInst, playerInst)
    return fitnessCheck(parameters, nGames, cardInst, discardPileInst, drawPileInst, gameInst, playerInst)


# def multiprocessing_func(procnum, return_dict):
#     a = [i for i in range(10000)]
#     for i in range(10):
#         random.shuffle(a)
#     return_dict[procnum] = a.copy()
#     if i % 10 == 0: print(i)
