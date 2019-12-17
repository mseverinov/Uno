# import main
import math
from collections import deque
import random

def thread(fitnessCheck, strategies, nGames, classDict, complexity, UI = False):
    """Self contained. To be used by pool. Runs nGames. Returns number of wins.

    Basically just a wrapper made for compatibility with multithreading."""
    CardClass = classDict['Card']
    DrawPileClass = classDict['DrawPile']
    DiscardPileClass = classDict['DiscardPile']
    PlayerClass = classDict['Player']
    GameClass = classDict['Game']

    pContainer = PlayerClass(None, container = True)
    gInst = GameClass()
    cContainer = CardClass('', 0, 0, True, True)

    pContainer.bot = PlayerClass(strategies[0], complexity = complexity)
    pContainer.all_.append(pContainer.bot)
    for i in range(3): pContainer.all_.append(PlayerClass(strategies[i+1]))

    cContainer.createCards(UI)

    gInst.nPlayers = len(pContainer.all_)
    gInst.decks = gInst.deckGen(cContainer)

    discardInst = DiscardPileClass()
    drawInst = DrawPileClass()

    objDict = {'card':cContainer, 'discard':discardInst, 'draw':drawInst, 'game':gInst, 'player':pContainer}

    # return_dict[itNum] = fitnessCheck(parameters, nGames, cardInst, discardPileInst, drawPileInst, gameInst, playerInst)
    return fitnessCheck(nGames, objDict, UI)
