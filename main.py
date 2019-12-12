import random
import time
from collections import deque
import cProfile
import math

from evolution import Evo

import multiprocessing
import worker
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
        # print('player ' + str(Game.currentPlayer))

class Player:
    """Base class for player operations"""

    def fitness(self, card, myHandSize, nextHandSize, prevHandSize):
        #potentially incorperate state history
        h = 0
        p = self.parameters
        if card.value in {0,1,2,3,4,5,6,7,8,9}:
            h += p[0] + myHandSize*p[7] + nextHandSize*p[14] + prevHandSize*p[21] + 1/myHandSize*p[28] + 1/nextHandSize*p[35] + 1/prevHandSize*p[42]
        elif card.value == 'reverse':
            h += p[1] + myHandSize*p[8] + nextHandSize*p[15] + prevHandSize*p[22] + 1/myHandSize*p[29] + 1/nextHandSize*p[36] + 1/prevHandSize*p[43]
        elif card.value == 'stop':
            h += p[2] + myHandSize*p[9] + nextHandSize*p[16] + prevHandSize*p[23] + 1/myHandSize*p[30] + 1/nextHandSize*p[37] + 1/prevHandSize*p[44]
        elif card.value == 'skip':
            h += p[3] + myHandSize*p[10] + nextHandSize*p[17] + prevHandSize*p[24] + 1/myHandSize*p[31] + 1/nextHandSize*p[38] + 1/prevHandSize*p[45]
        elif card.value == '+2':
            h += p[4] + myHandSize*p[11] + nextHandSize*p[18] + prevHandSize*p[25] + 1/myHandSize*p[32] + 1/nextHandSize*p[39] + 1/prevHandSize*p[46]
        elif card.value == 'basic':
            h += p[5] + myHandSize*p[12] + nextHandSize*p[19] + prevHandSize*p[26] + 1/myHandSize*p[33] + 1/nextHandSize*p[40] + 1/prevHandSize*p[47]
        elif card.value == '+4':
            h += p[6] + myHandSize*p[13] + nextHandSize*p[20] + prevHandSize*p[27] + 1/myHandSize*p[34] + 1/nextHandSize*p[41] + 1/prevHandSize*p[48]
        return h

    def __init__(self, container = False):
        """Creates player instance. Adding player to cls.all_"""
        if container:
            self.all_ = []
            self.bot = None
            self.parameters = None
            self.emptySet = set()

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


    # def genValidMoves(self):
    #     """Returns list of cards that match color or value of drawpile.
    #     Wilds are always added.
    #
    #     validMoves := list[CardInstance,...]"""
    #     return [card for card in self.hand if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue]


    # def genValidMoves(self, gen = True):
    #     """Returns list of cards that match color or value of drawpile.
    #     Wilds are always added.
    #
    #     validMoves := list[CardInstance,...]"""
    #     if gen == True:
    #         return (card for card in self.hand if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue)
    #     else:
    #         return [card for card in self.hand if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue]


    def chooseColor(self):
        """Finds most commom color in hand that is not "wild." """
        #Currently basic af. Needs to be updated be improved, but is not a priority for a while.
        #May be taken care of by foward searching algorithim.
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

    # def drawdeque(self):
    #     """Draws a card from the draw pile."""
    #     #add probability distribution updates here
    #     card = DrawPile.draw()
    #     if card != Card.badCard:
    #         self.hand.appendleft(card)

    def draw(self, cardInst, discardPileInst, drawPileInst):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = drawPileInst.draw(cardInst, discardPileInst)
        if card != cardInst.badCard:
            self.hand.add(card)

    def chooseRand(self, cardInst, gameInst, playerInst):
        "Chooses a card to play from hand."
        #insert foward searching here
        for card in self.hand:
            if card.color == 'wild' or card.color == gameInst.currentColor or card.value == gameInst.currentValue:
                self.hand.remove(card)
                return card
        # if ErrorChecking.handLengths:
        #     ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
        return cardInst.badCard

    # def chooseRand(self):
    #     "Chooses a card to play from hand."
    #     #insert foward searching here
    #     validMoves = self.genValidMoves()
    #     if validMoves == []:
    #         return False
    #     card = validMoves[0]
    #     self.hand.remove(card)
    #     return card

    def chooseWFitness(self, cardInst, gameInst, playerInst):
        #what if valid moves for each potential card combination are memorized
        tF = -math.inf
        tC = cardInst.badCard
        myHandSize = len(self.hand)
        nextHandSize = len(playerInst.all_[(gameInst.currentPlayer + gameInst.direction) % gameInst.nPlayers].hand)
        prevHandSize = len(playerInst.all_[(gameInst.currentPlayer - gameInst.direction) % gameInst.nPlayers].hand)
        for card in self.hand:
            if card.color == 'wild' or card.color == gameInst.currentColor or card.value == gameInst.currentValue:
                f = self.fitness(card, myHandSize, nextHandSize, prevHandSize)
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
        if currentPlayer == playerInst.bot:
            fitFunction = currentPlayer.chooseWFitness
        else:
            fitFunction = currentPlayer.chooseRand
        card = fitFunction(cardInst, gameInst, playerInst)
        if card == cardInst.badCard:
            currentPlayer.draw(cardInst, discardPileInst, drawPileInst)
            card = fitFunction(cardInst, gameInst, playerInst)
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


def fitnessCheck(parameters, nGames):
    # ErrorChecking.iteration += 1
    # if ErrorChecking.iteration % 40 == 0:
    #     print(ErrorChecking.iteration)
    return sum([gameLoop(parameters) for i in range(nGames)])



if __name__ == '__main__':
    nActors = 100
    evoInst = Evo()
    parameterSets = evoInst.createRandActors(nActors)
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(nActors):
        p = multiprocessing.Process(target=worker.worker, args=(gameLoop, parameterSets[i], Card, DrawPile, DiscardPile, Game, Player, return_dict, i))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    print([sum(return_dict.values()[i]) for i in range(nActors)])

# print(cProfile.run('main()',sort='tottime'))
