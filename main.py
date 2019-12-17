import random
import time
from collections import deque
import cProfile
import math

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import player
import cards
import game
import worker
import evolution
import draw

# import pygame

#ACTION ITEMS
#general code improvements.
    #memoization repeatedly used results?
#add probability changes after each discard/draw
#add probability case to handle player drawing a card and whether or not it is put down

def gameLoop(objDict, UI = False):
    """Plays a single game. Returns whether or not the player of interest won."""
    gInst = objDict['game']
    pContainer = objDict['player']
    if UI: ui = draw.UI(objDict['card'].baseDeck)

    gInst.reset(objDict)
    objDict['draw'].startdeal(objDict)
    if UI: ui.dealPlayer1(pContainer.all_[0].hand)
    if UI: ui.dealPlayer2(pContainer.all_[1].hand)
    if UI: ui.dealPlayer3(pContainer.all_[2].hand)
    if UI: ui.dealPlayer4(pContainer.all_[3].hand)

    card = gInst.firstCardFlip(objDict)
    # if UI: ui.dealDeck(card)

    while True:
        # ErrorChecking.handLenRecord()
        # print(UI)
        gInst.humanCondition = False
        actions = gInst.singlePlay(objDict, UI)
        # print(repr(actions))
        if UI:
            print('x')
            if actions == 'human turn':
                print('u')
                whatHappened = ui.humanTurn()
                print(whatHappened)
                print('w')
                if whatHappened == 'draw a card':
                    ui.turnCondition = False
                    print('bb')
                    card = objDict['player'].bot.draw(objDict, UI = True)
                    print('cc')
                    whatHappened = ui.humanTurn(card)
                    ui.turnCondition = False
                    card = whatHappened[1]
                    actions = gInst.singlePlay(objDict, UIcard = card)
            else:
                # for action in actions:
                #     print(action)
                print('aaprime')
                for action in actions:
                    # print(action)
                    if action != 'human turn':
                        actionType, pIndex, card = action
                        if actionType == 'draw':
                            ui.draw(pIndex, card)
                        if actionType == 'discard':
                            # print(ui, pIndex, card)
                            ui.discardfoo(pIndex, card)




        for player in objDict['player'].all_: #check length less often? if we take the smalled hand and multiple by four that is the soonest the game can end
            if len(player.hand) == 0:
                return player == objDict['player'].bot


def fitnessCheck(nGames, objDict, UI = False):
    """Returns number of wins.
    Exists so that gameLoop can be used in other locations than worker."""
    return sum([gameLoop(objDict, UI) for i in range(nGames)])

def UIGame():
    eInst = evolution.Evo()
    strategies = [[0 for i in range(eInst.nParameters)] for i in range(4)]
    classDict = {'Card':cards.Card, 'DrawPile':cards.DrawPile, 'DiscardPile':cards.DiscardPile, 'Game':game.Game, 'Player':player.Player}
    worker.thread(fitnessCheck, strategies, 1, classDict, eInst.complexity, UI = True)

def makegraphs():
    recordHistorys = False
    nActors = [5,50,500]
    nTestGames = [10,100,1000]
    mutationRates = [.1, .2, .4, .8, 1.6, 3.2]
    colors = ['-b',  '-g', '-r', '-c', '-m', '-y', '-k', '-w']
    complexity = [{'bot hand only':True, 'positive only':True, 'direct only':True, 'color':False},
                    {'bot hand only':False, 'positive only':True, 'direct only':True, 'color':False},
                    {'bot hand only':False, 'positive only':False, 'direct only':True, 'color':False},
                    {'bot hand only':False, 'positive only':False, 'direct only':False, 'color':False},
                    {'bot hand only':False, 'positive only':False, 'direct only':False, 'color':True}]
    nRepeats = 32
    checkPoints = [1,2,4,8,16,32]
    filePrefix = 'complexity '
    interest = complexity
    title = 'Fitness Function Complexity'
    if True in [isinstance(i, dict) for i in interest]:
        dictCondition = True
        logbooks = {tuple([(i,j) for i,j in element.items()]):[] for element in interest}
    else:
        dictCondition = False
        logbooks = {element:[] for element in interest}

    if recordHistorys: allHistories = []

    for nR in range(nRepeats):
        nR += 1
        start = time.time()

        if recordHistorys: repeatHistory = {}
        for element in interest:
            evoInst = evolution.Evo(complexity = element)
            classDict = {'Card':cards.Card, 'DrawPile':cards.DrawPile, 'DiscardPile':cards.DiscardPile, 'Game':game.Game, 'Player':player.Player}
            logbook, genHistories = evoInst.mainLoop(fitnessCheck, gameLoop, classDict, recordHistorys)
            a, ma, mi = logbook.select("avg", "max", "min")
            nTG = 1
            if recordHistorys: repeatHistory[element] = genHistories
            if dictCondition:
                logbooks[tuple([(i,j) for i,j in element.items()])].append([[i/nTG for i in a], [i/nTG for i in ma], [i/nTG for i in mi]])
            else:
                if interest == nTestGames:
                    nTG = element
                logbooks[element].append([[i/nTG for i in a], [i/nTG for i in ma], [i/nTG for i in mi]])
            end = time.time()
            print(nR, element, end-start, time.ctime(time.time()))
        if nR in checkPoints:
            checkSlice = checkPoints[:checkPoints.index(nR)+1]
            if dictCondition:
                avg = {k:{tuple([(a,b) for a,b in n.items()]):[sum([logbooks[tuple([(a,b) for a,b in n.items()])][i][0][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}
                max_ = {k:{tuple([(a,b) for a,b in n.items()]):[sum([logbooks[tuple([(a,b) for a,b in n.items()])][i][1][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}
                min_ = {k:{tuple([(a,b) for a,b in n.items()]):[sum([logbooks[tuple([(a,b) for a,b in n.items()])][i][2][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}
            else:
                avg = {k:{n:[sum([logbooks[n][i][0][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}
                max_ = {k:{n:[sum([logbooks[n][i][1][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}
                min_ = {k:{n:[sum([logbooks[n][i][2][j] for i in range(k)])/k for j in range(evoInst.nGen)] for n in interest} for k in checkSlice}

            x = list(range(evoInst.nGen))
            plt.figure()

            for i,checkpoint in enumerate(checkSlice):
                ax = plt.subplot(len(checkSlice), 1, i+1)
                ax.ticklabel_format(style='sci', axis='both', scilimits=(-5,5))
                plt.yscale('linear')
                plt.ylabel('Games Won')
                if interest == nTestGames:
                    print('triggered')
                    ax.yaxis.set_major_formatter(PercentFormatter(1))
                # ax=fig.add_axes
                if i == 0:
                    plt.title(title)
                if i == len(checkSlice) - 1:
                    plt.xlabel('Generations')

                for n in range(len(interest)):
                    plt.ylabel('Games Won')
                    thickness = 1/checkPoints.index(nRepeats)*(checkPoints.index(nRepeats)-checkPoints.index(nR))+.5
                    if dictCondition:
                        ax.plot(x, avg[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], '-' + colors[n], linewidth = thickness)
                        ax.plot(x, max_[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], colors[n], linewidth = thickness)
                        ax.plot(x, min_[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], colors[n], linewidth = thickness)
                    else:
                        ax.plot(x, avg[checkpoint][interest[n]], '-' + colors[n], linewidth = thickness)
                        ax.plot(x, max_[checkpoint][interest[n]], colors[n], linewidth = thickness)
                        ax.plot(x, min_[checkpoint][interest[n]], colors[n], linewidth = thickness)
                    plt.grid(True)
            filename = filePrefix + str(nR) + 'multi' + '.png'
            plt.savefig(filename, dpi=300)
            print("MultiPlot ", str(nR) + ' saved')
            plt.show()
            plt.figure()
            ax = plt.subplot(1,1,1)
            plt.ylabel('Games Won')
            plt.title(title)
            plt.xlabel('Generations')
            if interest == nTestGames:
                print('triggered')
                ax.yaxis.set_major_formatter(PercentFormatter(1))
            for n in range(len(interest)):
                if dictCondition:
                    ax.plot(x, avg[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], '-' + colors[n], linewidth = 1)
                    ax.plot(x, max_[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], colors[n], linewidth = 1)
                    ax.plot(x, min_[checkpoint][tuple([(a,b) for a,b in interest[n].items()])], colors[n], linewidth = 1)
                else:
                    ax.plot(x, avg[checkpoint][interest[n]], '-' + colors[n], linewidth = 1)
                    ax.plot(x, max_[checkpoint][interest[n]], colors[n], linewidth = 1)
                    ax.plot(x, min_[checkpoint][interest[n]], colors[n], linewidth = 1)
            plt.grid(True)
            filename = filePrefix + str(nR) + 'single'+'.png'
            plt.savefig(filename, dpi=300)
            plt.show()
            print("Singleplot ", str(nR) + ' saved')
        if recordHistorys: allHistories.append(repeatHistory)


##############
if __name__ == '__main__':
    makegraphs()
    # UIGame()
############################################
