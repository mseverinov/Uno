import main
import math
from collections import deque
import random

<<<<<<< HEAD
def worker(gameLoop, parameters, CardClass, DrawPileClass, DiscardPileClass, GameClass, PlayerClass, return_dict, itNum):
    nGames = 1000
    playerInst = PlayerClass(True)
    bot = PlayerClass()
    bot.parameters = parameters
    playerInst.all_.append(bot)
    playerInst.bot = bot
    p2 = PlayerClass()
    playerInst.all_.append(p2)
    p3 = PlayerClass()
    playerInst.all_.append(p3)
    p4 = PlayerClass()
    playerInst.all_.append(p4)

    nPlayers = len(playerInst.all_)
    gameInst = GameClass()
    gameInst.nPlayers = nPlayers
    cardInst = CardClass('', 0, 0, True, True)
    cardInst.createCards()
    gameInst.decks = gameInst.deckGen(cardInst)
=======

def fitnessCheck(parameters, nGames, return_dict):
    return_dict[parameters] = sum([gameLoop(parameters) for i in range(nGames)])
>>>>>>> 9bef32c93d48e5e1068f25ceea464158883bdded

    discardPileInst = DiscardPileClass()
    drawPileInst = DrawPileClass()

    return_dict[itNum] = [gameLoop(parameters, cardInst, discardPileInst, drawPileInst, gameInst, playerInst) for i in range(nGames)]

# def multiprocessing_func(procnum, return_dict):
#     a = [i for i in range(10000)]
#     for i in range(10):
#         random.shuffle(a)
#     return_dict[procnum] = a.copy()
#     if i % 10 == 0: print(i)
