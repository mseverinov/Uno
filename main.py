import random
#ACTION ITEMS
#create Player function to check if a the card drawn is playable. This is for the instance when there are no legal moves.
#create function that plays a single round. starting at the bot. Keep going until it is the bot's turn again.
#set up while loop that will run a game to completion

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
        for other in self.all:
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
            if card.color not in counter and color != 'wild':
                counter[card.color] = 1
            elif color != 'wild':
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
        hand.append(DrawPile.draw())


    def chooseCard(self):
        "Chooses a card to play from hand."
        #insert foward searching here
        validMoves = self.genValidMoves()
        card = random.choice(validMoves)
        self.hand.remove(card)
        return card


class Card:
    """Base class for card representations."""
    def __init__(self, color, value):
        """Sets the color and value of the card."""
        self.color = color #red, plue, green, yellow, wild
        self.value = value #0-9, +2, +4, skip, reverse, basic

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
        card = DrawPile.draw()
        while card.color == 'wild' and card.value == '+4': #the game cannot be stared with a wild +4
            Drawpile.contents.append(card)
            random.shuffle(DrawPile.contents)
            card = Drawpile.draw()
        DiscardPile.add(card)
        if card.color == 'wild':
            cls.currentColor = Player.all_[currentPlayer].chooseColor()
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

    @classmethod
    def singlePlay(cls):
        """Carries out a single play for the next player."""
        #Incomplete, probability stuff will probably be added here.
        card = Player.all_[cls.currentPlayer].chooseCard()
        DiscardPile.add(card)
        if card.color == 'wild':
            cls.currentColor = Player.all_[cls.currentPlayer].chooseColor()
        action = cls.actionCheck(card)
        cls.currentValue = card.valye
        cls.currentPlayer += cls.direction


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
            for i in range(int(card.value[-1])):
                Player.all_[cls.currentPlayer + cls.direction].draw()
            cls.currentPlayer += cls.direction
            return True
        return False



bot = Player()
p2 = Player()
p3 = Player()
p4 = Player()

DrawPile.startdeal()
bot.initPDists()

print(bot.drawPDist)
