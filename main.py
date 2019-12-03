import random
import time
from collections import deque
import cProfile
import math
from evolution import *
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
    # deck = [] #holds references to all possible cards
    all_ = [] #holds references to all players created #rename to created?
    bot = None
    parameters = None
    validMoves = {}
    emptySet = set()

    @classmethod
    def genAllValidMoves(cls):
        for card1 in Card.allInstances:
            if card1.color != 'wild':
                cls.validMoves[card1] = set([card2 for card2 in Card.allInstances if card2.color == 'wild' or card2.color == card1.color or card2.value == card1.value])
        wilds = [Card(color, value, 0) for color in {'red', 'yellow', 'green', 'blue'} for value in {'basic', '+4'}]
        for wild in wilds:
            cls.validMoves[wild] = set([card2 for card2 in Card.allInstances if card2.color == 'wild' or card2.color == card1.color])

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

    def drawdeque(self):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = DrawPile.draw()
        if card != Card.badCard:
            self.hand.appendleft(card)

    def draw(self):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = DrawPile.draw()
        if card != Card.badCard:
            self.hand.add(card)

    def chooseRand(self):
        "Chooses a card to play from hand."
        #insert foward searching here
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                self.hand.remove(card)
                return card
        if ErrorChecking.handLengths:
            ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
        return Card.badCard

    # def chooseRand(self):
    #     "Chooses a card to play from hand."
    #     #insert foward searching here
    #     validMoves = self.genValidMoves()
    #     if validMoves == []:
    #         return False
    #     card = validMoves[0]
    #     self.hand.remove(card)
    #     return card

    # def chooseWFitnessOld(self):
    #     #what if valid mo es for each potential top card are memlrized and rather than check for color or value we do a set comparision with hand
    #     tF = -1*(100)**2 #another potential speed up: each hand is a vector of all possible cards with value 1 for have, 0 for not. then multiply this against the vector of all potentially valid moves
    #     tC = None
    #     for card in self.hand:
    #         if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
    #             f = self.fitness(card)
    #             if f > tF:
    #                 tF = f
    #                 tC = card
    #     if tF > -1*(100)**2:
    #         self.hand.remove(tC)
    #         return tC
    #     return False

    def chooseWFitnessdeque(self):
        hand = set(self.hand)
        tempCard = Card(Game.currentColor, Game.currentValue, 0)
        try:
            validMoves = hand & self.validMoves[tempCard]
        except:
            print(self.validMoves)
            raise
        del tempCard
        if validMoves == self.emptySet:
            return Card.badCard
        tF = -math.inf
        tC = None
        for card in validMoves:
            f = self.fitness(card)
            if f > tF:
                tF = f
                tC = card
        self.hand.remove(tC)
        return tC

    def chooseWFitness(self):
        validMoves = self.hand & self.validMoves[Card(Game.currentColor, Game.currentValue, 0, True)] #why is this faster
        if validMoves == self.emptySet:
            return Card.badCard
        tF = -math.inf
        tC = None
        myHandSize = len(self.hand)
        nextHandSize = len(Player.all_[(Game.currentPlayer + Game.direction) % Game.nPlayers].hand)
        prevHandSize = len(Player.all_[(Game.currentPlayer - Game.direction) % Game.nPlayers].hand)
        for card in validMoves:
            f = self.fitness(card, myHandSize, nextHandSize, prevHandSize)
            if f > tF:
                tF = f
                tC = card
        self.hand.remove(tC)
        return tC

    def chooseWFitnessfail(self):
        tF = -math.inf
        tC = Card.badCard
        for card in self.hand & self.validMoves[Card(Game.currentColor, Game.currentValue, 0, True)]:
            f = self.fitness(card)
            if f > tF:
                tF = f
                tC = card
        if tF != -math.inf:
            self.hand.remove(tC)
        return tC

class Card:
    """Base class for card representations."""
    colors = ['yellow', 'red', 'blue', 'green', 'wild', 'bad']
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', '+4', 'skip', 'reverse', 'basic', 'bad']
    badCard = None
    allInstances = set()



    def __init__(self, color, value, dup, temp = False):
        """Sets the color and value of the card."""
        self.color = color
        self.value = value
        self.hash = (self.colors.index(color))*1000 + (self.values.index(value))*10 + dup
        if not temp:
            self.allInstances.add(self)
        #the normal wild (wild without draw for) has color: wild and value: basic

    def __str__(self):
        return str(self.color) + ' ' + str(self.value)

    def __repr__(self):
        return 'Card(' + self.color + ', ' + str(self.value) + ')'

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __hash__(self):
        return self.hash




class DrawPile: #do these need to be que's? Would it be random enough if they were just sets?
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
                DiscardPile.stack = deque([DiscardPile.stack[0]])
                # print('Draw pile reupped')
                cls.cardsLeft = len(cls.stack)
            else:
                return False
        cls.cardsLeft -= 1
        return cls.stack.pop()


    @classmethod
    def startdealdeque(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            player.hand = deque([cls.draw() for i in range(7)])
            cls.cardsLeft -= 7

    @classmethod
    def startdeal(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            player.hand = set([cls.draw() for i in range(7)])
            cls.cardsLeft -= 7


class DiscardPile:
    """Base class representing the discard pile."""
    stack = None #cards discared so far

    @classmethod
    def topcard(cls):
        """Returns the card currently at the top of the pile."""
        return cls.stack[-1]

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
    cards = []
    decks = None
    nPlayers = None

    @classmethod
    def deckGen(cls):
        i = 0
        while True:
            yield cls.decks[i]
            i += 1
            if i == 157:
                i = 0

    # @classmethod
    # def reset(cls):
    #     cls.currentPlayer = 0
    #     cls.direction = 1
    #     for player in Player.all_:
    #         player.hand = []
    #     DiscardPile.stack = deque()
    #     DrawPile.stack = random.choice(Game.decks)
    #     DrawPile.stack = deque(DrawPile.stack)
    #     DrawPile.cardsLeft = 108
    #     if ErrorChecking.handLengths:
    #         ErrorChecking.output = ''

    @classmethod
    def reset(cls):
        cls.currentPlayer = 0
        cls.direction = 1
        for player in Player.all_:
            player.hand = set()
        DiscardPile.stack = deque()
        DrawPile.stack = random.choice(Game.decks)
        DrawPile.stack = deque(DrawPile.stack)
        DrawPile.cardsLeft = 108
        if ErrorChecking.handLengths:
            ErrorChecking.output = ''

    @classmethod
    def createCards(cls):
        Card.badCard = Card('bad', 'bad', 0)
        for color in set(Card.colors) - {'wild', 'bad'}:
            for i in range(10):
                cls.cards.append(Card(color, i, 0))
            for i in range(1,10):
                cls.cards.append(Card(color, i, 1))
            for i in range(2):
                cls.cards.append(Card(color, 'skip', i))
                cls.cards.append(Card(color, 'reverse', i))
                cls.cards.append(Card(color, '+2', i))
        for i in range(4):
            cls.cards.append(Card('wild', 'basic', i))
            cls.cards.append(Card('wild', '+4', i))


    @classmethod
    def init(cls):
        """Once cards have been dealt, run this to turn over the first card."""
        cls.nPlayers = len(Player.all_)
        cls.currentPlayer = random.randint(0, len(Player.all_) - 1)
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
        if currentPlayer != Player.bot:
            card = currentPlayer.chooseWFitness()
        else:
            card = currentPlayer.chooseRand()
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
    DrawPile.startdeal()
    Game.init()
    # bot.initPDists()
    while True:
        if ErrorChecking.handLengths:
            ErrorChecking.handLenRecord()

        Game.singlePlay()
        # except:
        #     print(ErrorChecking.output)
        #     print(Game.currentPlayer, Game.currentColor, Game.currentValue)
        #     for player in Player.all_:
        #         print(player.hand)
        #
        #     raise
        # print(Game.currentColor, Game.currentValue)
        # print()

        for player in Player.all_: #check length less often? if we take the smalled hand and multiple by four that is the soonest the game can end
            if len(player.hand) == 0:
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
    Game.createCards()
    Player.genAllValidMoves()
    decks = []
    for i in range(157):
        decks.append(Game.cards.copy())
        random.shuffle(decks[i])
    Game.decks = decks

    first = Evo()
    first.mainLoop(fitnessCheck)

print(cProfile.run('main()',sort='tottime'))
