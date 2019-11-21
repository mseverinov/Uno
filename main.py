import random
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
    deck = [] #holds a references to all possible cards
    all_ = [] #holds references to all players created

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
        Wilds are always added.

        validMoves := list[CardInstance,...]"""
        validMoves = []
        for card in self.hand:
            if card.color == 'wild':
                validMoves.append(card)
            elif card.color == Game.currentColor:
                validMoves.append(card)
            elif card.value == Game.currentValue:
                validMoves.append(card)
        return validMoves


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

    def chooseCard(self):
        "Chooses a card to play from hand."
        #insert foward searching here
        validMoves = self.genValidMoves()
        if len(validMoves) == 0:
            return False
        card = random.choice(validMoves)
        self.hand.remove(card)
        return card



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
    contents = []
    @classmethod
    def init(cls):
        """Creates all cards, gives a copy to the Player class, and shuffles the deck."""
        for color in ['red', 'blue', 'yellow', 'green']:
            for i in range(10):
                cls.contents.append(Card(color, i))
            for i in range(1,10):
                cls.contents.append(Card(color, i))
            for i in range(2):
                cls.contents.append(Card(color, 'skip'))
                cls.contents.append(Card(color, 'reverse'))
                cls.contents.append(Card(color, '+2'))
            cls.contents.append(Card('wild', 'basic'))
            cls.contents.append(Card('wild', '+4'))
            Player.deck = cls.contents
            random.shuffle(cls.contents)

    @classmethod
    def draw(cls):
        """Draws a single card."""
        card = cls.contents[0]
        cls.contents = cls.contents[1:]
        return card

    @classmethod
    def startdeal(cls):
        """Deals 7 cards to all players."""
        for player in Player.all_:
            player.hand = [cls.draw() for i in range(7)]


class DiscardPile:
    """Base class representing the discard pile."""
    stack = [] #cards discared so far

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

    @classmethod
    def init(cls):
        """Once cards have been dealt, run this to turn over the first card."""
        #this is basically complete
        cls.currentPlayer = random.randint(0, len(Player.all_))
        card = DrawPile.draw()
        while card.color == 'wild' and card.value == '+4': #the game cannot be stared with a wild +4
            DrawPile.contents.append(card)
            random.shuffle(DrawPile.contents)
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
        card = currentPlayer.chooseCard()
        if card == False:
            currentPlayer.draw()
            card = currentPlayer.chooseCard()
        if card != False:
            DiscardPile.add(card)
            if card.color == 'wild':
                cls.currentColor = currentPlayer.chooseColor()
            action = cls.actionCheck(card)
            cls.currentValue = card.value
        cls.currentPlayer += cls.direction
        cls.currentPlayer = cls.currentPlayer % len(Player.all_)

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
        #complete
        if card.value == 'reverse':
            cls.direction *= -1
            return True
        if card.value == 'skip':
            cls.currentPlayer += cls.direction
            return True
        if card.value == '+2' or card.value == '+4':
            cls.currentPlayer += cls.direction
            cls.currentPlayer = cls.currentPlayer % len(Player.all_)
            for i in range(int(card.value[-1])):
                Player.all_[cls.currentPlayer].draw()
            return True
        return False


def multIt(it):
    t = 1
    for i in it:
        t *= i
    return t


def pColorDist(color):
    dist = []
    for n in range(1,8):
        if n == 7:
            print('x')
        dist.append(colorDistRecurs(0, 1, n))
    return dist


def colorDistRecurs(iteration, depth, n):
    start = iteration + depth
    end = 7 - n + depth
    if n == 6:
        print(start, end)
    #n is number of successes
    pT = 0
    for iteration, i in enumerate(range(start, end + 1)): #index of success
        if end == 7:
            sLst = [m for m in range(26-n, 26)]
            successNum = multIt(sLst)
            # for m in range(26-n, 26):
            #     #as many successes as n
            #     successNum *= m
            fLst = [m for m in range(84-i+n,84)]
            failNum = multIt(fLst)
            # for m in range(84-i+n,84):
            #     failNum *= m
            dLst = [m for m in range(109-i, 109)]
            denom = multIt(dLst)
            # for m in range(109-i, 109):
            #     denom *= m
            pi = successNum*failNum/denom
            # print(pi)
            if n == 6:
                print(pi, n, i)
                print(sLst, fLst, dLst)
                print(start, end)
                # raise
        else:
            pi = colorDistRecurs(iteration, depth + 1, n)
        pT += pi
    return pT


    def pColorNonRecurs(color):
        dist = []
        for n in range(1,8):
            pn = 0
            indicies = [i for i in range(1,1+n)]:
            while condition:
                sLst = [m for m in range(26-n, 26)]
                successNum = multIt(sLst)

                fLst = [m for m in range(84-indicies[-1]+n,84)]
                failNum = multIt(fLst)

                dLst = [m for m in range(109-indicies[-1], 109)]
                denom = multIt(dLst)

                pn += successNum*failNum/denom

                indicies[-1] += 1

                i = n-1
                cond2 = True
                while cond2:
                    if indicies[i] > 7:
                        indicies[i] = indicies[i-1] + 2
                        indicies[i-1] += 1
                    i -= 1

def Heuristic(bot):
    h = 0
    #game winning cases
    if len(hand) == 1:
        if True in [card.color == 'wild' for card in hand]:
            return max
        if hand[0].color == Game.currentColor:
            return max

    #action cards are valuable
    for card in hand:
        if card.value in ['+2', 'reverse', 'skip', 'wild']:
            h += value * number remaining #having action cards when others don't is increasingly valuabe
            if len(Player.all_[layer_index + direction].hand) == 1:
                return high

    #being unable to play a card
    if True not in [card.color == game.currentColor for card in hand]:
        lower(heuristic)
        if True in [card.color == 'wild' for card in hand]:
            increase(heuristic)

    #rarity of color for others vs for you
    if True [card.color == game.currentColor for card in hand]:
        increase(hueristic)
        modifyby(nColorCardsledt/nColorCardsyouhave)

    #modifywildvalue by relative color rarity
    if True in [card.color == 'wild' for card in hand]:
        potentialIncrease = value
        for portionOfCardsHeld in colors:
            modify(potentialIncrease)
        increase(heuristic by potentialIncrease)

    #incorperate knowledge about players hands
    if known that next player does not have color:
        if you have a wild:
            increase(heuistic)
            modifyby(handsize)


            
    #modify by your hand size relative to others
    for player in all_:
        base *= len(player.hand)/len(hand)

    #



bot = Player()
p2 = Player()
p3 = Player()
p4 = Player()


DrawPile.init()
DrawPile.startdeal()
Game.init()
bot.initPDists()
while 0 not in [len(player.hand) for player in Player.all_]:
    output = ''
    for n, player in enumerate(Player.all_):
        output += 'P' + str(n+1) + ' ' + str(len(player.hand)) + '\t'
    print(output)
    print('player ' + str(Game.currentPlayer))
    Game.singlePlay()
    print(Game.currentColor, Game.currentValue)
    print()
