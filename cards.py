import random
from collections import deque

class Card:
    """Base class for card representations."""

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

    def createCards(self, UI = False):
        if UI: self.UIdeck = set()
        self.badCard = Card('bad', 'bad', 0, True)
        for color in set(self.colors) - {'wild', 'bad'}:
            for i in range(10):
                self.baseDeck.append(Card(color, i, 0))
                if UI: self.UIdeck.add(Card(color, i, 0))
            for i in range(1,10):
                self.baseDeck.append(Card(color, i, 1))
            for i in range(2):
                self.baseDeck.append(Card(color, 'skip', i))
                self.baseDeck.append(Card(color, 'reverse', i))
                self.baseDeck.append(Card(color, '+2', i))
            if UI: self.UIdeck.add(Card(color, 'skip', 0))
            if UI: self.UIdeck.add(Card(color, 'reverse', 0))
            if UI: self.UIdeck.add(Card(color, '+2', 0))
        for i in range(4):
            wild = Card('wild', 'basic', i)
            self.baseDeck.append(wild)
            self.wilds.add(wild)
            wild = Card('wild', '+4', i)
            self.baseDeck.append(wild)
            self.wilds.add(wild)
        if UI: self.UIdeck.add(Card('wild', 'basic', 0))
        if UI: self.UIdeck.add(Card('wild', '+4', 0))



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

    def draw(self, objDict):
        """Draws a single card."""
        discardInst = objDict['discard']
        if self.cardsLeft == 0:
            if discardInst.cards > 1:
                self.stack = deque(list(discardInst.stack)[1:])
                random.shuffle(self.stack)
                discardInst.stack = deque([discardInst.stack[0]])
                # print('Draw pile reupped')
                self.cardsLeft = len(self.stack)
            else:
                return objDict['card'].badCard
        self.cardsLeft -= 1
        return self.stack.pop()

    def startdeal(self, objDict):
        """Deals 7 cards to all players."""
        for player in objDict['player'].all_:
            player.hand = set([self.draw(objDict) for i in range(7)])
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
