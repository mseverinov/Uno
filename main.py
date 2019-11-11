import random

class Player:
    deck = []
    all_ = []

    def __init__(self):
        self.all_.append(self)

    def initPDists(self):
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
        validMoves = []
        for card in self.hand:
            if card.color == 'wild':
                validMoves.append(card)
            elif card.color == Game.currentColor:
                validMoves.append(card)
            elif card.value == Game.currentValue:
                validMoves.append(card)


    def chooseColor(self):
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
        hand.append(DrawPile.draw())


    def chooseCard(self):
        validMoves = self.genValidMoves()
        card = random.choice(validMoves)
        self.hand.remove(card)
        return card


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return str(self.color) + ' ' + str(self.value)

    def __repr__(self):
        return str(self.color) + ' ' + str(self.value)


class DrawPile:
    contents = []
    @classmethod
    def init(cls):
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
        card = cls.contents[0]
        cls.contents = cls.contents[1:]
        return card

    @classmethod
    def startdeal(cls):
        for player in Player.all_:
            player.hand = [cls.draw() for i in range(7)]


class DiscardPile:
    stack = []

    @classmethod
    def topcard(cls):
        return cls.stack[-1]

    @classmethod
    def add(cls, card):
        cls.stack.append(card)

class Game:
    currentPlayer = 0
    currentColor = None
    currentValue = None
    direction = 1

    @classmethod
    def init(cls):
        card = DrawPile.draw()
        while card.color == 'wild' and card.value == '+4':
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
        card = Player.all_[cls.currentPlayer].chooseCard()
        DiscardPile.add(card)
        if card.color == 'wild':
            cls.currentColor = Player.all_[cls.currentPlayer].chooseColor()
        action = cls.actionCheck(card)
        cls.currentValue = card.valye
        cls.currentPlayer += cls.direction


    @classmethod
    def actionCheck(cls, card):
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
