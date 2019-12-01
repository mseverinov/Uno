import random
# from evolution import fitnessCheck
# from heuristic import fitness
from collections import deque
import cProfile
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


class Player:
    """Base class for player operations"""
    deck = [] #holds references to all possible cards
    all_ = [] #holds references to all players created
    bot = None
    parameters = None

    def fitness(self, card):
        #potentially incorperate state history
        h = 0
        p = self.parameters
        nCards = len(self.hand)
        nCardsNext = len(Player.all_[(Game.currentPlayer + Game.direction) % Game.nPlayers].hand)
        nCardsPrev = len(Player.all_[(Game.currentPlayer - Game.direction) % Game.nPlayers].hand)
        if card.value in {0,1,2,3,4,5,6,7,8,9}:
            h += p[0] + nCards*p[7] + nCardsNext*p[14] + nCardsNext*p[21]
        elif card.value == 'reverse':
            h += p[1] + nCards*p[8] + nCardsNext*p[15] + nCardsNext*p[22]
        elif card.value == 'stop':
            h += p[2] + nCards*p[9] + nCardsNext*p[16] + nCardsNext*p[23]
        elif card.value == 'skip':
            h += p[3] + nCards*p[10] + nCardsNext*p[17] + nCardsNext*p[24]
        elif card.value == '+2':
            h += p[4] + nCards*p[11] + nCardsNext*p[18] + nCardsNext*p[25]
        elif card.value == 'basic':
            h += p[5] + nCards*p[12] + nCardsNext*p[19] + nCardsNext*p[26]
        elif card.value == '+4':
            h += p[6] + nCards*p[13] + nCardsNext*p[20] + nCardsNext*p[27]
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
        return mostCommon

    def draw(self):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        self.hand.append(DrawPile.draw())


    def chooseRand(self):
        "Chooses a card to play from hand."
        #insert foward searching here
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                self.hand.remove(card)
                return card
        return False

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
        tF = 0
        tC = None
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                f = self.fitness(card)
                if f > tF:
                    tF = f
                    tC = card
        if tF != 0:
            self.hand.remove(tC)
            return tC
        return False

    # def chooseWFitness(self):
    #     validMoves = self.genValidMoves()
    #     if validMoves == []:
    #         return False
    #     tF = 0
    #     tC = None
    #     for card in validMoves:
    #         f = fitness(card)
    #         if f > tF:
    #             tF = f
    #             tC = card
    #     self.hand.remove(tC)
    #     return tC






class Card:
    """Base class for card representations."""
    def __init__(self, color, value):
        """Sets the color and value of the card."""
        self.color = color #red, plue, green, yellow, wild
        self.value = value #0-9, +2, +4, skip, reverse, basic
        #the normal wild (wild without draw for) has color: wild and value: basic

    def __str__(self):
        return str(self.color) + ' ' + str(self.value)

    def __repr__(self):
        return str(self.color) + ' ' + str(self.value)


class DrawPile:
    """Base class representing the draw pile."""
    stack = []
    cardsLeft = 108

    @classmethod
    def draw(cls):
        """Draws a single card."""
        if cls.cardsLeft == 0:
            random.shuffle(DiscardPile.stack)
            cls.stack = deque(DiscardPile.stack)
            DiscardPile.stack = deque()
            # print('Draw pile reupped')
            cls.cardsLeft = len(cls.stack)
        cls.cardsLeft -= 1
        return cls.stack.pop()

    @classmethod
    def startdeal(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            player.hand = deque([cls.draw() for i in range(7)])
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
    def reset(cls):
        cls.currentPlayer = 0
        cls.direction = 1
        for player in Player.all_:
            player.hand = []
        DiscardPile.stack = deque()
        DrawPile.stack = random.choice(Game.decks)
        DrawPile.stack = deque(DrawPile.stack)
        DrawPile.cardsLeft = 108

    @classmethod
    def createCards(cls):
        for color in ['red', 'blue', 'yellow', 'green']:
            for i in range(10):
                cls.cards.append(Card(color, i))
            for i in range(1,10):
                cls.cards.append(Card(color, i))
            for i in range(2):
                cls.cards.append(Card(color, 'skip'))
                cls.cards.append(Card(color, 'reverse'))
                cls.cards.append(Card(color, '+2'))
            cls.cards.append(Card('wild', 'basic'))
            cls.cards.append(Card('wild', '+4'))

    @classmethod
    def init(cls):
        """Once cards have been dealt, run this to turn over the first card."""
        #this is basically complete
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
        if card == False:
            currentPlayer.draw()
            card = currentPlayer.chooseRand()
        if card != False:
            DiscardPile.add(card)
            if card.color == 'wild':
                cls.currentColor = currentPlayer.chooseColor()
            action = cls.actionCheck(card)
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
            return True
        if card.value == 'skip':
            cls.currentPlayer += cls.direction
            return True
        if card.value == '+2' or card.value == '+4':
            cls.currentPlayer += cls.direction
            cls.currentPlayer = cls.currentPlayer % cls.nPlayers
            for i in range(int(card.value[-1])):
                Player.all_[cls.currentPlayer].draw()
            return True
        return False

class State:
    def __init__(self):
        pass

def gameLoop(parameters):
    Player.parameters = parameters
    Game.reset()
    DrawPile.startdeal()
    Game.init()
    # bot.initPDists()
    # print(len(Player.all_))
    while True:
        # output = ''
        # for n, player in enumerate(Player.all_):
        #     output += 'P' + str(n+1) + ' ' + str(len(player.hand)) + '\t'
        # print(output)
        # print('player ' + str(Game.currentPlayer))
        Game.singlePlay()
        # print(Game.currentColor, Game.currentValue)
        # print()

        for player in Player.all_:
            if len(player.hand) == 0:
                return player == Player.bot


def fitnessCheck(parameters, nGames):
    return sum([gameLoop(parameters) for i in range(nGames)])





def evo():
    #better actors make more children?
    #add mutation rate?
    #use max of running average rather than cumulative average
    #keep track of w/l ratio of survivors over the course of generations
    #lock parameters which have equilibriated
    #perhaps unlock and relock over time
    nActors = 640
    itLowerLimit = 10
    thresholdValue = .01
    thresholdLength = 5
    nParameters = 28
    nGames = 50

    bot = Player()
    Player.bot = bot
    p2 = Player()
    p3 = Player()
    p4 = Player()
    Game.createCards()
    decks = []
    for i in range(100):
        decks.append(Game.cards.copy())
        random.shuffle(decks[i])
    Game.decks = decks

    actors = [[random.random() for i in range(nParameters)] for j in range(nActors)]

    fitHist = []
    iteration = 0
    condition = True
    fitAvgMax = 0
    improvIndex = 0
    while condition:
        print(iteration)
        iteration += 1
        fitPairs = sorted([(actor, fitnessCheck(actor, nGames)) for actor in actors], key = lambda x: x[1], reverse = True)  #add record keeping for all wins for all parameter sets across iteration.
        # print(fitPairs)
        avg = sum([fitPairs[i][1] for i in range(nActors//4)])/(nGames*nActors/4/4) #subtract placebo
        fitHist.append(avg)
        print([fitPairs[i][1] for i in range(0, nActors//4, 4)], avg, sum(fitHist)/len(fitHist))
        # print([sum([fitPairs[i][0][j] for i in range(nActors//2)])/(nActors//2) for j in range(nParameters)])

        topHalf = [fitPairs[i][0] for i in range(nActors//4)]
        # t = sum([fitPairs[i][1] for i in range(nActors//2)])
        # avg = t/(nActors/2)
        # tup = (fitPairs[0][1], avg)
        # fitHist.append(tup)

        if iteration > itLowerLimit:
            if avg > fitAvgMax + thresholdValue:
                fitAvgMax = avg
                improvIndex = iteration

            if iteration - improvIndex > thresholdLength:
                return topHalf[0]



        random.shuffle(topHalf)
        children = []
        for i in range(0, nActors//4, 2):
            actor = []
            for j in range(nParameters):
                actor.append((topHalf[i][j] + topHalf[i+1][j])/2)
            children.append(actor)
        # children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(nActors//2)]
        actors = topHalf + children + [[random.random() for i in range(nParameters)] for j in range(5*nActors//8)]


        # print(actors)

# cProfile.run('evo()',sort='tottime')
evo()
