import random
import time
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
            h += p[0] + nCards*p[7] + nCardsNext*p[14] + nCardsPrev*p[21] + 1/nCards*p[28] + 1/nCardsNext*p[35] + 1/nCardsPrev*p[42]
        elif card.value == 'reverse':
            h += p[1] + nCards*p[8] + nCardsNext*p[15] + nCardsPrev*p[22] + 1/nCards*p[29] + 1/nCardsNext*p[36] + 1/nCardsPrev*p[43]
        elif card.value == 'stop':
            h += p[2] + nCards*p[9] + nCardsNext*p[16] + nCardsPrev*p[23] + 1/nCards*p[30] + 1/nCardsNext*p[37] + 1/nCardsPrev*p[44]
        elif card.value == 'skip':
            h += p[3] + nCards*p[10] + nCardsNext*p[17] + nCardsPrev*p[24] + 1/nCards*p[31] + 1/nCardsNext*p[38] + 1/nCardsPrev*p[45]
        elif card.value == '+2':
            h += p[4] + nCards*p[11] + nCardsNext*p[18] + nCardsPrev*p[25] + 1/nCards*p[32] + 1/nCardsNext*p[39] + 1/nCardsPrev*p[46]
        elif card.value == 'basic':
            h += p[5] + nCards*p[12] + nCardsNext*p[19] + nCardsPrev*p[26] + 1/nCards*p[33] + 1/nCardsNext*p[40] + 1/nCardsPrev*p[47]
        elif card.value == '+4':
            h += p[6] + nCards*p[13] + nCardsNext*p[20] + nCardsPrev*p[27] + 1/nCards*p[34] + 1/nCardsNext*p[41] + 1/nCardsPrev*p[48]
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

    def draw(self):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = DrawPile.draw()
        if card != False:
            self.hand.appendleft(card)


    def chooseRand(self):
        "Chooses a card to play from hand."
        #insert foward searching here
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                self.hand.remove(card)
                return card
        if ErrorChecking.handLengths:
            ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
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
        tF = -1*(100)**2
        tC = None
        for card in self.hand:
            if card.color == 'wild' or card.color == Game.currentColor or card.value == Game.currentValue:
                f = self.fitness(card)
                if f > tF:
                    tF = f
                    tC = card
        if tF > -1*(100)**2:
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
    def deckGen(cls):
        i = 0
        while True:
            yield cls.decks[i]
            i += 1
            if i == 157:
                i = 0

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
        if ErrorChecking.handLengths:
            ErrorChecking.output = ''

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
                try:
                    Player.all_[cls.currentPlayer].draw()
                except:
                    cls.currentPlayer += cls.direction
                    cls.currentPlayer = cls.currentPlayer % cls.nPlayers
                    print('Player', cls.currentPlayer, 'used +2 or +4')

                    raise

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

        for player in Player.all_:
            if len(player.hand) == 0:
                return player == Player.bot


def fitnessCheck(parameters, nGames):
    # ErrorChecking.iteration += 1
    # if ErrorChecking.iteration % 40 == 0:
    #     print(ErrorChecking.iteration)
    return sum([gameLoop(parameters) for i in range(nGames)])





def evo():
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


    #Monday
        #label and group results in viewing

    #Tuesday
        #simultanios side evolution

    #Wednesday
        #incorperate w/l multigenerational record

    #Thursday
        #probabilistic fitness matching for cross breeding

    nActors = 160
    itLowerLimit = 100
    thresholdValue = 1
    thresholdLength = 100
    nParameters = 49
    nGames = 500

    bot = Player()
    Player.bot = bot
    p2 = Player()
    p3 = Player()
    p4 = Player()
    Game.createCards()
    decks = []
    for i in range(157):
        decks.append(Game.cards.copy())
        random.shuffle(decks[i])
    Game.decks = decks

    # actors = [[random.random() for i in range(nParameters)] for j in range(nActors)]
    actors = [[random.randint(-100,100) for i in range(nParameters)] for j in range(nActors)]
    # actors = [[1 for i in range(nParameters)] for j in range(nActors)]
    # actorHistory = {tuple(actor):(0,0) for actor in actors}

    fitHist = []
    iteration = 0
    condition = True
    # runningAvg = 0
    # fitAvgMax = 0
    # improvIndex = 0
    avgActorHist = []
    nKeep = 2
    start = 0
    end = 0
    while condition:
        print('it:', iteration, 'time:', int(end-start))
        iteration += 1
        start = time.time()
        fitPairs = sorted([(actor, fitnessCheck(actor, nGames)) for actor in actors], key = lambda x: x[1], reverse = True)
        end = time.time()

        # actorHistoryN = {}
        # for pair in fitPairs[:nActors//nKeep]:
        #     tActor = tuple(pair[0])
        #     if tActor in actorHistory:
        #         actorHistoryN[tActor] = (pair[1] + actorHistory[tActor][0], nGames + actorHistory[tActor][1])
        #     else:
        #         actorHistoryN[tActor] = (pair[1], nGames)
        # actorHistory = actorHistoryN

        top = [fitPairs[i][0] for i in range(nActors//nKeep)]
        avg = sum([fitPairs[i][1] for i in range(nActors//nKeep//2)])/(nGames*nActors/nKeep/2/4)
        fitHist.append(avg)

        cumAvg = sum(fitHist)/len(fitHist)
        half = fitHist[len(fitHist)//2:]
        halfAvg = sum(half)/(len(half))
        quart = fitHist[len(fitHist)//4:]
        quartAvg = sum(quart)/(len(quart))

        if nActors//4 > 20:
            step = (nActors//4)//20
        else:
            step = 1
        print([fitPairs[i][1] for i in range(0, nActors//4, step)], avg, str(quartAvg), str(halfAvg), str(cumAvg))
        # avgActor = [sum([fitPairs[i][0][j] for i in range(nActors//nKeep//2)])/(nActors/nKeep/2) for j in range(nParameters)]
        # avgActorHist.append(avgActor)
        # print([top[0]])
        # print([sum([avgActorHist[i][j] for i in range(len(avgActorHist))])//len(avgActorHist) for j in range(nParameters)])


        if iteration > itLowerLimit:
            return top[0]

            # if runningAvg > fitAvgMax + thresholdValue:
            #     fitAvgMax = runningAvg
            #     improvIndex = iteration
            #
            # if iteration - improvIndex > thresholdLength:
            #     return top[0]



        # random.shuffle(top)
        children = []
        for i in range(0, nActors//(nKeep*2), 2):
            actor = []
            for j in range(nParameters):
                actor.append((top[i][j] + top[i+1][j])/2)
            children.append(actor)
        # print(children)
        # children = [ [(topHalf[i][j] + topHalf[i+1][j])/2 for j in range(nParameters)] for i in range(nActors//2)]
        # actors = top + children + [[random.random() for i in range(nParameters)] for j in range(5*nActors//8)]
        actors = top + children + [[random.randint(-100,100) for i in range(nParameters)] for j in range(3*nActors//8)]


        # print(actors)

# cProfile.run('evo()',sort='tottime')
bot = Player()
Player.bot = bot
p2 = Player()
p3 = Player()
p4 = Player()
Game.createCards()
decks = []
for i in range(157):
    decks.append(Game.cards.copy())
    random.shuffle(decks[i])
Game.decks = decks
