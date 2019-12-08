import multiprocessing
import time
import random
import multi
from collections import deque
import main
import cProfile
import math
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
    stacks = False
    output = ''
    iteration = 0

    @classmethod
    def handLenRecord(cls):
        if Game.currentPlayer == 0:
            for n, player in enumerate(Player.all_):
                cls.output += 'P' + str(n+1) + ' ' + str(len(player.hand)) + '\t'
            cls.output += '\n'
        # print('player ' + str(Game.currentPlayer))

    @classmethod
    def record(cls, string):
        cls.output += string + '\n'

class Player:
    """Base class for player operations"""
    # deck = [] #holds references to all possible cards
    all_ = [] #holds references to all players created #rename to created?
    bot = None
    parameters = None
    validMoves = {}
    emptySet = set()

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

    # def drawdeque(self):
    #     """Draws a card from the draw pile."""
    #     #add probability distribution updates here
    #     card = DrawPile.draw()
    #     if card != Card.badCard:
    #         self.hand.appendleft(card)

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
        # if ErrorChecking.handLengths:
        #     ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
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

    def chooseWFitness(self):
        #what if valid moves for each potential card combination are memorized
        tF = -math.inf
        tC = Card.badCard
        myHandSize = len(self.hand)
        nextHandSize = len(Player.all_[(Game.currentPlayer + Game.direction) % Game.nPlayers].hand)
        prevHandSize = len(Player.all_[(Game.currentPlayer - Game.direction) % Game.nPlayers].hand)
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                f = self.fitness(card, myHandSize, nextHandSize, prevHandSize)
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
    baseDeck = []
    wilds = set()

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

        # for i in range(4):
        #     for color in set(cls.colors) - {'wild', 'bad'}:
        #         Card(color, 'basic', i)
        #         Card(color, '+4', i)

    # @classmethod
    # def indexGenM(cls):
    #     index = 0
    #     while True:
    #         yield index
    #         index += 1

    def __init__(self, color, value, dup, temp = False):
        """Sets the color and value of the card."""
        self.color = color
        self.value = value
        self.hash = (self.colors.index(color))*1000 + (self.values.index(value))*10 + dup
        if not temp:
            self.allInstances.add(self)

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
            if DiscardPile.cards > 1:
                cls.stack = deque(list(DiscardPile.stack)[1:])
                random.shuffle(cls.stack)
                DiscardPile.stack = deque([DiscardPile.stack[0]])
                # print('Draw pile reupped')
                cls.cardsLeft = len(cls.stack)
            else:
                return Card.badCard
        cls.cardsLeft -= 1
        if ErrorChecking.stacks:
            ErrorChecking.record('DrawPile : ' + str(cls.stack) + ' ' + str(DrawPile.cardsLeft))
        try:
            return cls.stack.pop()
        except:
            print(ErrorChecking.output)
            raise


    # @classmethod
    # def startdealdeque(cls):
    #     """Deals 7 cards to all players."""
    #     for player in Player.all_:
    #         player.hand = deque([cls.draw() for i in range(7)])
    #         cls.cardsLeft -= 7

    @classmethod
    def startdeal(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            player.hand = set([cls.draw() for i in range(7)])
            cls.cardsLeft -= 7


class DiscardPile:
    """Base class representing the discard pile."""
    stack = None #cards discared so far
    cards = 0

    @classmethod
    def add(cls, card):
        """Takes a card and adds it to the discard pile."""
        cls.cards += 1
        if ErrorChecking.stacks:
            ErrorChecking.record('DiscardPile : ' + str(cls.stack) + ' ' + str(DiscardPile.cards))
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
        decks = []
        for i in range(157):
            decks.append(deque(Card.baseDeck.copy()))
            random.shuffle(decks[i])
        i = 0
        while True:
            yield decks[i].copy()
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
        ErrorChecking.output = ''
        cls.currentPlayer = random.randint(0, len(Player.all_) - 1)
        cls.direction = 1
        for player in Player.all_:
            player.hand = set()
        DiscardPile.stack = deque()
        DiscardPile.cards = 0
        DrawPile.stack = next(cls.decks)
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
        if currentPlayer == Player.bot:
            fitFunction = currentPlayer.chooseWFitness
        else:
            fitFunction = currentPlayer.chooseRand
        card = fitFunction()
        if card == Card.badCard:
            currentPlayer.draw()
            card = fitFunction()
        if card != Card.badCard:
            DiscardPile.add(card)
            if card.color == 'wild':
                cls.currentColor = currentPlayer.chooseColor()
            if card.value in {'skip', 'reverse', '+2', '+4'}:
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




class Evo:
    nActors = 8
    itLowerLimit = 5
    thresholdValue = 1
    thresholdLength = 15
    nParameters = 49
    nGames = 100
    parmRange = 100
    nKeep = 2
    #THOUGHTS IDEAS ECT
        #better actors make more children?
        #add mutation rate?
        #lock parameters which have equilibriated
        #perhaps unlock and relock over time
        #clustering algorithim
        #rather than having a coefficient for all possible functional forms, randomize the choice of functional
            #only cross breed species with matching functional forms
            #mutuate children from loners
        #give opposing players parameters from other actors
        #multi threading
        #analyze differences in parameters of time for differerent portions of the top
        #write results to a file
        #increase number of games to test over as iteration number increases
        #discard any actors that perform below average, especially in the beginining
            #each generation keep above average until carry over cap reached
        #do parents need to be retested generation after generation?
        #in cross breeding explore other avenues besides averaging all values
            #some averages
            #some crossovers
            #some mutations
                #any ways to think about what an optimal coefficent of the above would be?
        #random include or drop various nodes to determine which are necesarry?
        #implement graphing of results
        #visualize what the w/l ratio of a single parameter set is across generations. is it consistent? how much so?
        #simultaniuis side evolution to improve accuracy of improvement
        #evo -> stand alone
        #label and group results in viewing
        #incorperate w/l multigenerational record
        #attempt 10 games, 8000 actors
        #probabilistic fitness matching for cross breeding

    #Priority 1
        #SPEED UP UNO GAME SIMULATION!!
            #create list/set of valid moves for every card at the beginning of simulation
            #Potential Solution 1: Vectorize
                #use numpy to multiply binary vectors to find crossover
                #this will require significantly longer lists. Will the speed up overcome this?
            #Potential Solution 2
                #Use set comparision to do the same thing
                #which cards in hand are in set that contains all valid move for the card on top of the discard pile

    #Priority 2
        #rewrite current evolution algorithim using DEAP library

    #Priority 3
        #implement randomization of node function,
            #remove unnessary parameters
            #determine how this will be incorperated into evolution
            #functions:
                # x
                # 1/x
                # + vs - ?
                # x^2
                #combinations of the above



    def __init__(self):

        # actors = [[1 for i in range(nParameters)] for j in range(nActors)]
        # actorHistory = {tuple(actor):(0,0) for actor in actors}
        self.fitHist = []
        # fitAvgMax = 0
        # improvIndex = 0
        self.avgActorHist = []


    def mainLoop(self, fitnessCheck):
        start = 0
        end = 0
        iteration = 0
        continueCond = True
        self.actors = self.createRandActors(self.nActors)
        while continueCond:
            print('it:', iteration, 'time:', int(end-start))
            start = time.time()
            iteration += 1
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            processes = []
            for actor in self.actors:
                p = multiprocessing.Process(target=multi.fitnessCheck, args=(actor, self.nGames, return_dict))
                processes.append(p)
                p.start()

            for process in processes:
                process.join()
            fitPairs = sorted([(key, return_dict[key]) for key in return_dict], key = lambda x: x[1], reverse = True)
            avg, quartAvg, halfAvg, cumAvg = self.calcStats(fitPairs)
            # actorHistoryN = {}
            # for pair in fitPairs[:nActors//nKeep]:
            #     tActor = tuple(pair[0])
            #     if tActor in actorHistory:
            #         actorHistoryN[tActor] = (pair[1] + actorHistory[tActor][0], nGames + actorHistory[tActor][1])
            #     else:
            #         actorHistoryN[tActor] = (pair[1], nGames)
            # actorHistory = actorHistoryN
            if self.nActors//4 > 20:
                step = (self.nActors//4)//20
            else:
                step = 1
            print([fitPairs[i][1] for i in range(0, self.nActors//4, step)], avg, str(quartAvg), str(halfAvg), str(cumAvg))
            # avgActor = [sum([fitPairs[i][0][j] for i in range(nActors//nKeep//2)])/(nActors/nKeep/2) for j in range(nParameters)]
            # avgActorHist.append(avgActor)
            # print([top[0]])
            # print([sum([avgActorHist[i][j] for i in range(len(avgActorHist))])//len(avgActorHist) for j in range(nParameters)])
            top = [fitPairs[i][0] for i in range(self.nActors//2)]
            if self.endCheck(iteration):
                return top[0]

            nNewActors = 3*self.nActors//8
            actors = top + self.createChildren(top) + self.createRandActors(nNewActors)
            end = time.time()


    def createRandActors(self, n):
        # return [[random.random() for i in range(nParameters)] for j in range(n)]
        return [[random.randint(-1*self.parmRange, self.parmRange) for i in range(self.nParameters)] for j in range(n)]


    def createChildren(self, parents):
        # random.shuffle(parents)
        children = []
        for i in range(0, self.nActors//(self.nKeep*2), 2):
            actor = []
            for j in range(self.nParameters):
                actor.append((parents[i][j] + parents[i+1][j])/2)
            children.append(actor)
        # print(children)
        # children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(nActors//2)]
        # actors = top + children + [[random.random() for i in range(nParameters)] for j in range(5*nActors//8)]
        return children


    def calcStats(self, fitPairs):
        top = [fitPairs[i][0] for i in range(self.nActors//self.nKeep)]
        avg = sum([fitPairs[i][1] for i in range(self.nActors//self.nKeep//2)])/(self.nGames*self.nActors/self.nKeep/2/4)
        self.fitHist.append(avg)

        cumAvg = sum(self.fitHist)/len(self.fitHist)
        half = self.fitHist[len(self.fitHist)//2:]
        halfAvg = sum(half)/(len(half))
        quart = self.fitHist[len(self.fitHist)//4:]
        quartAvg = sum(quart)/(len(quart))

        return avg, quartAvg, halfAvg, cumAvg

    def endCheck(self,iteration):
        if iteration > self.itLowerLimit:
            return True
        else:
            return False

            # if runningAvg > fitAvgMax + thresholdValue:
            #     fitAvgMax = runningAvg
            #     improvIndex = iteration
            #
            # if iteration - improvIndex > thresholdLength:
            #     return top[0]

def gameLoop(parameters):
    # print(len(Player.all_))
    Player.parameters = parameters
    Game.reset()
    DrawPile.startdeal()
    Game.init()
    # bot.initPDists()
    while True:
        # ErrorChecking.handLenRecord()
        Game.singlePlay()

        for player in Player.all_: #check length less often? if we take the smalled hand and multiple by four that is the soonest the game can end
            if len(player.hand) == 0:
                return player == Player.bot

if __name__ == '__main__':
    bot = Player()
    main.Player.bot = bot
    p2 = main.Player()
    p3 = main.Player()
    p4 = main.Player()
    main.Game.nPlayers = len(main.Player.all_)
    main.Card.createCards()
    main.Game.decks = main.Game.deckGen()
    # Card.genAllValidMoves()
    first = Evo()
    first.mainLoop(main.fitnessCheck)




# if __name__ == '__main__':
#     start = time.time()
#     return_dict = {}
#     for i in range(100):
#         multi.multiprocessing_func(i, return_dict)
#     end = time.time()
#
#     print(end-start)
#     print([len(return_dict[i]) for i in return_dict])
#     starttime = time.time()
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     processes = []
#     for i in range(0,100):
#         p = multiprocessing.Process(target=multi.multiprocessing_func, args=(i,return_dict))
#         processes.append(p)
#         p.start()
#
#     for process in processes:
#         process.join()
#
#     print('That took {} seconds'.format(time.time() - starttime))
#     print([len(return_dict[i]) for i in return_dict])
