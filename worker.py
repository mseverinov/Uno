import main
import math
import deque
import random

def worker(gameLoop, parameters, CardClass, DrawPileClass, DiscardPileClass, GameClass, PlayerClass, return_dict, itNum):
    playerInst = PlayerClass(True)
    bot = PlayerClass()
    playerInst.all_append(bot)
    playerInst.bot = bot
    p2 = PlayerClass()
    playerInst.all_append(p2)
    p3 = PlayerClass()
    playerInst.all_append(p3)
    p4 = PlayerClass()
    playerInst.all_append(p4)

    nPlayers = len(bot.all_)
    gameInst = GameClass()
    gameInst.nPlayers = nPlayers
    cardInst = CardClass('', 0, 0, True, True)
    cardInst.createCards()
    gameInst.decks = gameInst.deckGen(cardInst)

    discardPileInst = DiscardPileClass()
    drawPileInst = DrawPileClass()

    return_dict[itNum] = gameLoop(parameters, cardInst, discardPileInst, drawPileInst, gameInst, playerInst)


# def multiprocessing_func(procnum, return_dict):
#     a = [i for i in range(10000)]
#     for i in range(10):
#         random.shuffle(a)
#     return_dict[procnum] = a.copy()
#     if i % 10 == 0: print(i)
