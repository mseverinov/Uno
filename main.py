import random
import time
from collections import deque
import cProfile
import math
from evolution import *
import numpy as np
#comment: genValidMove now relizes on arrys, discard pile -> set, consolidation of card methods
#ACTION ITEMS
#improve end of game detection
#add probability changes after each discard/draw
#add probability case to handle player drawing a card and whether or not it is put down

#TO DO FROM END OF LAST SESSION
    #resume randCard method update. need to determine how to randomly pick a card from a binary array
    #submit a build once numpy move checking is Complete
    #commment consolidated card methods & attributes,validMoves detection moved from set comparision to arrayProduct
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
    all_ = [] #holds references to all players created #rename to created?
    bot = None
    parameters = None
    validMoves = {}
    emptySet = set()
    emptyArray = np.array([], dtype='int32')

    def fitness(self, card, myHandSize, nextHandSize, prevHandSize):
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

    def __init__(self):
        """Creates player instance. Adding player to cls.all_"""
        self.all_.append(self)

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


    def genValidMoves(self):
        """Returns list of cards that match color or value of drawpile.
        Wilds are always added."""
        pass

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
        for i,v in enumerate(self.hand):
            if v == 1:
                card = Card.indexToCardMap[i]
                # print('index:',i, 'value:',v)
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

    def draw(self):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = DrawPile.draw()
        if card != Card.badCard:
            # print(self.hand)
            self.hand[card.index] = 1

    def chooseRand(self):
        "Chooses a card to play from hand."
        # if 1 == int(sum(self.hand)):
        #     # print('y')
        #     cardt = Card(Game.currentColor, Game.currentValue, 0, True)
        #     validMoves = self.hand*Card.validMoves[Card(Game.currentColor, Game.currentValue, 0, True)]
        #     cards = [Card.indexToCardMap[i] for i in np.nonzero(validMoves)[0]]
        #     print('\t', 'Valid Moves:', cards)
        validMoves = self.hand*Card.validMoves[Card(Game.currentColor, Game.currentValue, 0, True)]
        # print(validMoves)
        indices = np.nonzero(validMoves)[0]
        # if 1 == int(sum(self.hand)):
            # print('\t', indices, indices.shape)
        if np.array_equiv(indices.shape, self.emptyArray.shape):
            # if 1 == int(sum(self.hand)):
                # print('\t', self.emptyArray.shape)
            return Card.badCard
        card = Card.indexToCardMap[np.random.choice(indices)]
        self.hand[card.index] = 0
        return card
        # if ErrorChecking.handLengths:
        #     ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'

    # def chooseRand(self):
    #     "Chooses a card to play from hand."
    #     #insert foward searching here
    #     validMoves = self.genValidMoves()
    #     if validMoves == []:
    #         return False
    #     card = validMoves[0]
    #     self.hand.remove(card)
    #     return card

    def chooseWFitness(self):
        validMoves = self.hand*Card.validMoves[Card(Game.currentColor, Game.currentValue, 0, True)]
        indices = np.nonzero(validMoves)[0]
        if np.array_equiv(indices, self.emptyArray):
            return Card.badCard
        tF = -math.inf #does this slow down performance at all?
        tC = None
        myHandSize = len(self.hand)
        nextHandSize = len(Player.all_[(Game.currentPlayer + Game.direction) % Game.nPlayers].hand)
        prevHandSize = len(Player.all_[(Game.currentPlayer - Game.direction) % Game.nPlayers].hand)
        for i in indices:
            card = Card.indexToCardMap[i]
            f = self.fitness(card, myHandSize, nextHandSize, prevHandSize)
            if f > tF:
                tF = f
                tC = card
        self.hand[tC.index] = 0
        return tC


class Card:
    """Base class for card representations."""
    colors = ['yellow', 'red', 'blue', 'green', 'wild', 'bad']
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', '+4', 'skip', 'reverse', 'basic', 'bad']
    badCard = None
    allInstances = set()
    baseDeck = []
    decks = None
    wilds = set()
    validMoves = {}
    indexToCardMap = {}
    indexGen = None

    @classmethod
    def indexGenM(cls):
        index = 0
        while True:
            yield index
            index += 1

    @classmethod
    def createCards(cls):
        cls.badCard = Card('bad', 'bad', 0, True)
        for color in set(cls.colors) - {'wild', 'bad'}:
            for i in range(10):
                cls.baseDeck.append(Card(color, i, 0))
            for i in range(1,10):
                cls.baseDeck.append(Card(color, i, 1))
            for i in range(2):
                cls.baseDeck.append(Card(color, 'skip', i))
                cls.baseDeck.append(Card(color, 'reverse', i))
                cls.baseDeck.append(Card(color, '+2', i))
        for i in range(4):
            wild = Card('wild', 'basic', i)
            cls.baseDeck.append(wild)
            cls.wilds.add(wild)
            wild = Card('wild', '+4', i)
            cls.baseDeck.append(wild)
            cls.wilds.add(wild)

        for i in range(4):
            for color in set(cls.colors) - {'wild', 'bad'}:
                Card(color, 'basic', i)
                Card(color, '+4', i)

    @classmethod
    def genAllValidMoves(cls):
        for card1 in cls.allInstances:
            if card1.value != 'basic' or card1.value != '+4':
                # print(card1)
                # array = np.array([card2.color == 'wild' or card2.color == card1.color or card2.value == card1.value for card2 in cls.baseDeck])
                # print([Card.indexToCardMap[i] for i in np.nonzero(array)[0]])
                cls.validMoves[card1] = np.array([card2.color == 'wild' or card2.color == card1.color or card2.value == card1.value for card2 in cls.baseDeck])
            else:
                cls.validMoves[card1] = np.array([card2 for card2 in Card.baseDeck if card2.color == 'wild' or card2.color == card1.color])

    def __init__(self, color, value, dup, temp = False):
        """Sets the color and value of the card."""
        self.color = color
        self.value = value
        self.hash = (self.colors.index(color))*1000 + (self.values.index(value))*10 + dup
        if not temp:
            self.allInstances.add(self)
            self.index = next(self.indexGen)
            self.indexToCardMap[self.index] = self
        #the normal wild (wild without draw for) has color: wild and value: basic

    def __str__(self):
        return str(self.color) + ' ' + str(self.value)

    def __repr__(self):
        return 'Card(' + self.color + ', ' + str(self.value) + ', ' + str(self.hash) + ')'

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __hash__(self):
        return self.hash


class DrawPile:
    """Base class representing the draw pile."""
    stack = []
    cardsLeft = 108

    @classmethod
    def draw(cls):
        """Draws a single card."""
        if cls.cardsLeft == 0:
            if len(DiscardPile.stack) > 1:
                cls.stack = deque(list(DiscardPile.stack)[1:])
                random.shuffle(cls.stack)
                cls.cardsLeft = len(cls.stack)
            else:
                return False
        cls.cardsLeft -= 1
        # print(cls.stack, cls.cardsLeft)
        return cls.stack.pop()

    @classmethod
    def startdeal(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            for i in range(7):
                player.draw()


class DiscardPile:
    """Base class representing the discard pile."""
    #could this be speed up by turning contents into a set
        #only concern is randomization
    stack = None

    @classmethod
    def add(cls, card):
        """Takes a card and adds it to the discard pile."""
        cls.stack.append(card)


class Game:
    """Base containter for running the game."""
    currentPlayer = 0 #index of Player.all_ list the references the current player
    currentColor = None
    currentValue = None
    direction = 1 #1 for normal, -1 for reversed
    decks = None
    nPlayers = None

    @classmethod
    def deckGen(cls):
        decks = []
        for i in range(157):
            decks.append(deque(Card.baseDeck.copy()))
            random.shuffle(decks[i])
        i = 0
        while True:
            # print(i, [len(deck) for deck in decks])
            yield decks[i].copy()
            i += 1
            if i == 157:
                i = 0

    @classmethod
    def reset(cls):
        cls.currentPlayer = random.randint(0, len(Player.all_) - 1)
        cls.direction = 1
        for player in Player.all_:
            player.hand = np.zeros((108,))
        DiscardPile.stack = deque()
        DrawPile.stack = next(cls.decks)
        # print(DrawPile.stack)
        # print(DrawPile.stack)
        DrawPile.cardsLeft = 108
        if ErrorChecking.handLengths:
            ErrorChecking.output = ''

    @classmethod
    def init(cls):
        """Once cards have been dealt, run this to turn over the first card."""
        card = DrawPile.draw()
        while card.color == 'wild' and card.value == '+4': #the game cannot be stared with a wild +4
            DrawPile.stack.append(card)
            random.shuffle(DrawPile.stack)
            card = DrawPile.draw()
        DiscardPile.add(card)
        if card.color == 'wild':
            cls.currentColor = Player.all_[cls.currentPlayer].chooseColor()
        else:
            cls.currentColor = card.color

        cls.currentValue = card.value
        if card.value == 'reverse':
            cls.direction *= -1
            cls.currentPlayer += cls.direction
        elif card.value == 'skip':
            cls.currentPlayer += cls.direction
        elif card.value == '+2':
            for i in range(2):
                Player.all_[cls.currentPlayer].draw()
            cls.currentPlayer += cls.direction
        cls.currentPlayer = cls.currentPlayer % len(Player.all_)

    @classmethod
    def singlePlay(cls):
        """Carries out a single play for the next player."""
        #Complete - probability stuff.
        currentPlayer = Player.all_[cls.currentPlayer]
        # if 1 == int(sum(currentPlayer.hand)):
        #     # print([Card.indexToCardMap[i] for i in np.nonzero(currentPlayer.hand)[0]])
        #     print(cls.currentPlayer, cls.currentColor, cls.currentValue)
            # print([Card.indexToCardMap[i] for i in np.nonzero(Card.validMoves[Card(cls.currentColor, cls.currentValue, 0, 1)])[0]])
        if currentPlayer == Player.bot:
            card = currentPlayer.chooseWFitness()
        else:
            card = currentPlayer.chooseRand()
            # if 1 == int(sum(currentPlayer.hand)):
            #     print(card)
        if card == Card.badCard:
            currentPlayer.draw()
            card = currentPlayer.chooseRand()
        if card != Card.badCard:
            DiscardPile.add(card)
            if card.color == 'wild':
                cls.currentColor = currentPlayer.chooseColor()
            cls.actionCheck(card)
            cls.currentValue = card.value
        cls.currentPlayer += cls.direction
        cls.currentPlayer = cls.currentPlayer % cls.nPlayers

    @classmethod
    def playRound(cls):
        startPlayer = Player.all_[cls.currentPlayer]
        cls.singlePlay()
        currentPlayer = Player.all_[cls.currentPlayer]
        while startPlayer != currentPlayer:
            cls.singlePlay()
            currentPlayer = Player.all_[cls.currentPlayer]

    @classmethod
    def actionCheck(cls, card):
        """Carries out any effects triggered by an action card."""
        if card.value == 'reverse':
            cls.direction *= -1
        elif card.value == 'skip':
            cls.currentPlayer += cls.direction
        elif card.value == '+2' or card.value == '+4':
            cls.currentPlayer += cls.direction
            cls.currentPlayer = cls.currentPlayer % cls.nPlayers
            for i in range(int(card.value[-1])):
                Player.all_[cls.currentPlayer].draw()

def gameLoop(parameters):
    Player.parameters = parameters
    Game.reset()
    # print(DrawPile.stack)
    DrawPile.startdeal()
    Game.init()
    # bot.initPDists()
    i = 0
    while True:
        if ErrorChecking.handLengths:
            ErrorChecking.handLenRecord()
        # print(i, sum([sum(player.hand) for player in Player.all_]), [sum(player.hand) for player in Player.all_])
        # if 1 in [int(sum(player.hand)) for player in Player.all_]:
            # print('x')
            # for player in Player.all_:
            #     a = np.nonzero(player.hand)[0]
            #     print([Card.indexToCardMap[i] for i in a])
        i+=1
        Game.singlePlay()
        for player in Player.all_: #check length less often? if we take the smallest hand and multiple by four that is the soonest the game can end
            if not player.hand.any():
                # print('end')
                return player == Player.bot


def fitnessCheck(parameters, nGames):
    # ErrorChecking.iteration += 1
    # if ErrorChecking.iteration % 40 == 0:
    #     print(ErrorChecking.iteration)
    return sum([gameLoop(parameters) for i in range(nGames)])



def main():
    bot = Player()
    Player.bot = bot
    p2 = Player()
    p3 = Player()
    p4 = Player()
    Game.nPlayers = len(Player.all_)
    Card.indexGen = Card.indexGenM()
    Card.createCards()
    Card.genAllValidMoves()
    Game.decks = Game.deckGen()
    first = Evo()
    # print([Card.indexToCardMap[i] for i in np.nonzero(Card.validMoves[Card('red', 0, 0, 1)])[0]])
    first.mainLoop(fitnessCheck)

print(cProfile.run('main()',sort='tottime'))
