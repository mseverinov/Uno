import random
import time
from collections import deque
import cProfile
import math

from evolution import Evo

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# import multiprocessing
# import worker
#ACTION ITEMS
#general code improvements.
    #memoization repeatedly used results
    #see which lists can be replaced with sets
    #rewrite data storage to modify reference rather than rewrite it for each change/addition
    #turn player progression into an iterable
#end of game detection
#add case to handle draw pile running out
#add probability changes after each discard/draw
#add probability case to handle player drawing a card and whether or not it is put down

class ErrorChecking:
    handLengths = False
    output = ''
    iteration = 0

    @classmethod
    def handLenRecord(cls):
        if Game.currentPlayer == 0:
            for n, player in enumerate(Player.all_):
                cls.output += 'P' + str(n+1) + ' ' + str(len(player.hand)) + '\t'
            cls.output += '\n'

class Player:
    """Base class for player operations"""

    def fitness(self, card, handSizes, colorCounts):
        #potentially incorperate state history
        h = 0
        p = self.strategy
        myHandSize = handSizes['my']
        nextHandSize = handSizes['next']
        prevHandSize = handSizes['prev']

        hBool = not(self.complexity['bot hand only'])
        dBool = not(self.complexity['direct only'])
        cBool = self.complexity['color']

        if card.value in {0,1,2,3,4,5,6,7,8,9}:
            h += p[0] + p[7]*myHandSize + nextHandSize*p[14]*hBool + prevHandSize*p[21]*hBool + p[28]/myHandSize*dBool + 1/nextHandSize*p[35]*hBool*dBool* + hBool*dBool*p[42]/prevHandSize
        elif card.value == 'reverse':
            h += p[1] + p[8]*myHandSize + nextHandSize*p[15]*hBool + prevHandSize*p[22]*hBool + p[29]/myHandSize*dBool + 1/nextHandSize*p[36]*hBool*dBool + hBool*dBool*p[43]/prevHandSize
        elif card.value == 'stop':
            h += p[2] + p[9]*myHandSize + nextHandSize*p[16]*hBool + prevHandSize*p[23]*hBool + p[30]/myHandSize*dBool + 1/nextHandSize*p[37]*hBool*dBool + hBool*dBool*p[44]/prevHandSize
        elif card.value == 'skip':
            h += p[3] + p[10]*myHandSize + nextHandSize*p[17]*hBool + prevHandSize*p[24]*hBool + p[31]/myHandSize*dBool + 1/nextHandSize*p[38]*hBool*dBool + hBool*dBool*p[45]/prevHandSize
        elif card.value == '+2':
            h += p[4] + p[11]*myHandSize + nextHandSize*p[18]*hBool + prevHandSize*p[25]*hBool + p[32]/myHandSize*dBool + 1/nextHandSize*p[39]*hBool*dBool + hBool*dBool*p[46]/prevHandSize
        elif card.value == 'basic':
            h += p[5] + p[12]*myHandSize + nextHandSize*p[19]*hBool + prevHandSize*p[26]*hBool + p[33]/myHandSize*dBool + 1/nextHandSize*p[40]*hBool*dBool + hBool*dBool*p[47]/prevHandSize
        elif card.value == '+4':
            h += p[6] + p[13]*myHandSize + nextHandSize*p[20]*hBool + prevHandSize*p[27]*hBool + p[34]/myHandSize*dBool + 1/nextHandSize*p[41]*hBool*dBool + hBool*dBool*p[48]/prevHandSize
        if card.color in {'yellow', 'red', 'blue', 'green'}:
            h += (p[49]*colorCounts[card.color] + p[50]/colorCounts[card.color])*(p[51]*myHandSize + p[52]/myHandSize)

        return h

    def __init__(self, parameters, complexity = None, container = False):
        """Creates player instance. Adding player to cls.all_"""
        if container:
            self.all_ = []
            self.bot = None
            self.emptySet = set()
        else:
            if complexity != None:
                self.complexity = complexity
            self.strategy = parameters
            for p in parameters:
                if p != 0:
                    self.chooseCard = self.chooseWFitness
                    break
            else:
                self.chooseCard = self.chooseRand



    def initPDists(self):
        """Initializes probability distributions for drawpile and other players' hands.

        drawPdist := dict{CardInstance: int}
        playerPDist := dict{PlayerInstance: dict{CardInstance: int}}"""
        self.drawPDist = {}
        for card in self.deck:
            self.drawPDist[card] = 1/101
        for card in self.hand:
            self.drawPDist[card] = 0

        self.playerPDist = {}
        for other in self.all_:
            if other != self:
                self.playerPDist[other] = self.drawPDist.copy()

    def chooseColor(self):
        """Finds most commom color in hand that is not "wild." """
        counter = {}
        for card in self.hand:
            if card.color not in counter and card.color != 'wild':
                counter[card.color] = 1
            elif card.color != 'wild':
                counter[card.color] +=1

        mostCommon = None
        n = 0
        for color in counter:
            if counter[color] > n:
                mostCommon = color
                n = counter[color]
        if n == 0:
            return random.choice(['yellow', 'red', 'blue', 'green'])
        return mostCommon

    def draw(self, cardInst, discardPileInst, drawPileInst):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = drawPileInst.draw(cardInst, discardPileInst)
        if card != cardInst.badCard:
            self.hand.add(card)

    def chooseRand(self, cardInst, gameInst, playerInst):
        "Chooses a card to play from hand."
        for card in self.hand:
            if card.color == 'wild' or card.color == gameInst.currentColor or card.value == gameInst.currentValue:
                self.hand.remove(card)
                return card
        # if ErrorChecking.handLengths:
        #     ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
        return cardInst.badCard

    def chooseWFitness(self, cardInst, gameInst, playerInst):
        tF = -math.inf
        tC = cardInst.badCard
        handSizes = {}
        handSizes['my'] = len(self.hand)
        handSizes['next'] = len(playerInst.all_[(gameInst.currentPlayer + gameInst.direction) % gameInst.nPlayers].hand)
        handSizes['prev'] = len(playerInst.all_[(gameInst.currentPlayer - gameInst.direction) % gameInst.nPlayers].hand)
        colors = {card.color for card in self.hand}
        colorCounts = {color:sum([card.color == color for card in self.hand]) for color in colors}
        for card in self.hand:
            if card.color == 'wild' or card.color == gameInst.currentColor or card.value == gameInst.currentValue:
                f = self.fitness(card, handSizes, colorCounts)
                if f > tF:
                    tF = f
                    tC = card
        if tF != -math.inf:
            self.hand.remove(tC)
        return tC


class Card:
    """Base class for card representations."""

    def createCards(self):
        self.badCard = Card('bad', 'bad', 0, True)
        for color in set(self.colors) - {'wild', 'bad'}:
            for i in range(10):
                self.baseDeck.append(Card(color, i, 0))
            for i in range(1,10):
                self.baseDeck.append(Card(color, i, 1))
            for i in range(2):
                self.baseDeck.append(Card(color, 'skip', i))
                self.baseDeck.append(Card(color, 'reverse', i))
                self.baseDeck.append(Card(color, '+2', i))
        for i in range(4):
            wild = Card('wild', 'basic', i)
            self.baseDeck.append(wild)
            self.wilds.add(wild)
            wild = Card('wild', '+4', i)
            self.baseDeck.append(wild)
            self.wilds.add(wild)

    def __init__(self, color, value, dup, temp = False, container = False):
        """Sets the color and value of the card."""
        if not container:
            self.color = color
            self.value = value
            self.hash = (['yellow', 'red', 'blue', 'green', 'wild', 'bad'].index(color))*1000 + ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', '+4', 'skip', 'reverse', 'basic', 'bad'].index(value))*10 + dup
        else:
            self.badCard = None
            self.baseDeck = []
            self.colors = ['yellow', 'red', 'blue', 'green', 'wild', 'bad']
            self.values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', '+4', 'skip', 'reverse', 'basic', 'bad']
            self.wilds = set()

    def __str__(self):
        return str(self.color) + ' ' + str(self.value)

    def __repr__(self):
        return 'Card(' + self.color + ', ' + str(self.value) + ')'

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __hash__(self):
        return self.hash


class DrawPile:

    def __init__(self):
        self.stack = []
        self.cardsLeft = 108

    def draw(self, cardInst, discardPileInst):
        """Draws a single card."""
        if self.cardsLeft == 0:
            if discardPileInst.cards > 1:
                self.stack = deque(list(discardPileInst.stack)[1:])
                random.shuffle(self.stack)
                discardPileInst.stack = deque([discardPileInst.stack[0]])
                # print('Draw pile reupped')
                self.cardsLeft = len(self.stack)
            else:
                return cardInst.badCard
        self.cardsLeft -= 1
        return self.stack.pop()

    def startdeal(self, cardInst, discardPileInst, playerInst):
        """Deals 7 cards to all players."""
        for player in playerInst.all_:
            player.hand = set([self.draw(cardInst, discardPileInst) for i in range(7)])
            self.cardsLeft -= 7


class DiscardPile:
    """Base class representing the discard pile."""

    def __init__(self):
        self.stack = deque() #cards discarded so far
        self.cards = 0

    def add(self, card):
        """Takes a card and adds it to the discard pile."""
        self.cards += 1
        # if ErrorChecking.stacks:
        #     ErrorChecking.record('DiscardPile : ' + str(cls.stack) + ' ' + str(DiscardPile.cards))
        self.stack.append(card)


class Game:
    """Base containter for running the game."""

    def __init__(self):
        self.nPlayers = None
        self.currentPlayer = None
        self.currentColor = None
        self.currentValue = None
        self.direction = 1 #1 for normal, -1 for reversed
        self.decks = None

    def deckGen(self, cardInst):
        decks = []
        for i in range(157):
            decks.append(deque(cardInst.baseDeck.copy()))
            random.shuffle(decks[i])
        i = 0
        while True:
            yield decks[i].copy()
            i += 1
            if i == 157:
                i = 0

    def reset(self, discardPileInst, drawPileInst, playerInst):
        # ErrorChecking.output = ''
        self.currentPlayer = random.randint(0, len(playerInst.all_) - 1)
        self.direction = 1
        for player in playerInst.all_:
            player.hand = set()
        discardPileInst.stack = deque()
        discardPileInst.cards = 0
        drawPileInst.stack = next(self.decks)
        drawPileInst.cardsLeft = 108

    def init(self, cardInst, discardPileInst, drawPileInst, playerInst):
        """Once cards have been dealt, run this to turn over the first card."""
        self.nPlayers = len(playerInst.all_)
        card = drawPileInst.draw(cardInst, discardPileInst)
        while card.color == 'wild' and card.value == '+4': #the game cannot be stared with a wild +4
            drawPileInst.stack.append(card)
            random.shuffle(drawPileInst.stack)
            card = drawPileInst.draw(cardInst, discardPileInst)
        discardPileInst.add(card)
        if card.color == 'wild':
            self.currentColor = playerInst.all_[self.currentPlayer].chooseColor()
        else:
            self.currentColor = card.color

        self.currentValue = card.value
        if card.value == 'reverse':
            self.direction *= -1
            self.currentPlayer += self.direction
        elif card.value == 'skip':
            self.currentPlayer += self.direction
        elif card.value == '+2':
            for i in range(2):
                playerInst.all_[self.currentPlayer].draw(cardInst, discardPileInst, drawPileInst)
            self.currentPlayer += self.direction
        self.currentPlayer = self.currentPlayer % len(playerInst.all_)

    def singlePlay(self, cardInst, discardPileInst, drawPileInst, gameInst, playerInst):
        """Carries out a single play for the next player."""
        #Complete - probability stuff.
        currentPlayer = playerInst.all_[self.currentPlayer]
        card = currentPlayer.chooseCard(cardInst, gameInst, playerInst)
        if card == cardInst.badCard:
            currentPlayer.draw(cardInst, discardPileInst, drawPileInst)
            card = currentPlayer.chooseCard(cardInst, gameInst, playerInst)
        if card != cardInst.badCard:
            discardPileInst.add(card)
            if card.color == 'wild':
                self.currentColor = currentPlayer.chooseColor()
            if card.value in {'skip', 'reverse', '+2', '+4'}:
                self.actionCheck(card, cardInst, discardPileInst, drawPileInst, playerInst)
            self.currentValue = card.value
        self.currentPlayer += self.direction
        self.currentPlayer = self.currentPlayer % self.nPlayers

    def actionCheck(self, card, cardInst, discardPileInst, drawPileInst, playerInst):
        """Carries out any effects triggered by an action card."""
        if card.value == 'reverse':
            self.direction *= -1
        elif card.value == 'skip':
            self.currentPlayer += self.direction
        elif card.value == '+2' or card.value == '+4':
            self.currentPlayer += self.direction
            self.currentPlayer = self.currentPlayer % self.nPlayers
            for i in range(int(card.value[-1])):
                playerInst.all_[self.currentPlayer].draw(cardInst, discardPileInst, drawPileInst)

def gameLoop(parameters, cardInst, discardPileInst, drawPileInst, gameInst, playerInst):
    # print(len(Player.all_))
    playerInst.parameters = parameters
    gameInst.reset(discardPileInst, drawPileInst, playerInst)
    drawPileInst.startdeal(cardInst, discardPileInst, playerInst)
    gameInst.init(cardInst, discardPileInst, drawPileInst, playerInst)
    while True:
        # ErrorChecking.handLenRecord()
        gameInst.singlePlay(cardInst, discardPileInst, drawPileInst, gameInst, playerInst)
        for player in playerInst.all_: #check length less often? if we take the smalled hand and multiple by four that is the soonest the game can end
            if len(player.hand) == 0:
                return player == playerInst.bot


def fitnessCheck(parameters, nGames, cardInst, discardPileInst, drawPileInst, gameInst, playerInst):
    # ErrorChecking.iteration += 1
    # if ErrorChecking.iteration % 40 == 0:
    #     print(ErrorChecking.iteration)
    return sum([gameLoop(parameters, cardInst, discardPileInst, drawPileInst, gameInst, playerInst) for i in range(nGames)])

# def plotFoo(checkSlice, interest, )


if __name__ == '__main__':
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
    filePrefix = 'nGames '
    interest = nTestGames
    title = 'Games Per Generation (10, 100, 1000)'
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
            evoInst = Evo(nGames = element)
            classDict = {'Card':Card, 'DrawPile':DrawPile, 'DiscardPile':DiscardPile, 'Game':Game, 'Player':Player}
            logbook, genHistories = evoInst.mainLoop(fitnessCheck, gameLoop, classDict, recordHistorys)
            a, ma, mi = logbook.select("avg", "max", "min")

            if recordHistorys: repeatHistory[element] = genHistories
            if dictCondition:
                logbooks[tuple([(i,j) for i,j in element.items()])].append([[i/nTG for i in a], [i/nTG for i in ma], [i/nTG for i in mi]])
            else:
                nTG = 1
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
            # plt.show()
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
            print("Singleplot ", str(nR) + ' saved')
        if recordHistorys: allHistories.append(repeatHistory)

    # print([sum(return_dict.values()[i]) for i in range(nActors)])

# print(cProfile.run('main()',sort='tottime'))
