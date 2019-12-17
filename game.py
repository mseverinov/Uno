import random
from collections import deque

class Game:
    """Base containter for running the game."""
    humanCondition = False

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

    def reset(self, objDict):
        # ErrorChecking.output = ''
        self.currentPlayer = random.randint(0, len(objDict['player'].all_) - 1)
        self.direction = 1
        for player in objDict['player'].all_:
            player.hand = set()
        objDict['discard'].stack = deque()
        objDict['discard'].cards = 0
        objDict['draw'].stack = next(self.decks)
        objDict['draw'].cardsLeft = 108

    def firstCardFlip(self, objDict, UI=False):
        """Once cards have been dealt, run this to turn over the first card."""
        drawInst = objDict['draw']
        self.nPlayers = objDict['game'].nPlayers
        card = drawInst.draw(objDict)
        while card.color == 'wild' and card.value == '+4': # the game cannot be stared with a wild +4
            drawInst.stack.append(card)
            random.shuffle(drawInst.stack)
            card = drawInst.draw(objDict)
        objDict['discard'].add(card)
        if card.color == 'wild':
            self.currentColor = objDict['player'].all_[self.currentPlayer].chooseColor()
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
                objDict['player'].all_[self.currentPlayer].draw(objDict)
            self.currentPlayer += self.direction
        self.currentPlayer = self.currentPlayer % self.nPlayers
        if UI: return card

    def singlePlay(self, objDict, UI = False, UIcard = None):
        """Carries out a single play for the next player."""
        # Complete - probability stuff
        # print('i')
        if UI and self.currentPlayer == 0 and not self.humanCondition:
            self.humanCondition = True
            return 'human turn'

        ###########################################
        if UI: actions = []
        currentPlayer = objDict['player'].all_[self.currentPlayer]

        if not self.humanCondition:
            card = currentPlayer.chooseCard(objDict)
            if card == objDict['card'].badCard:
                card = currentPlayer.draw(objDict, UI)
                if UI: actions.append(('draw', self.currentPlayer, card))
                card = currentPlayer.chooseCard(objDict)
            if card != objDict['card'].badCard:
                objDict['discard'].add(card)
                if UI: actions.append(('discard', self.currentPlayer, card))
        else:
            card = UIcard
            print(self.humanCondition)
            print('x', self.currentPlayer)
            print(card)
            objDict['player'].all_[self.currentPlayer].hand.remove(card)
            print('x', self.currentPlayer)
            objDict['discard'].add(card)
            # self.humanCondition = False
        if card.color == 'wild':
            self.currentColor = currentPlayer.chooseColor()
        if card.value in {'skip', 'reverse', '+2', '+4'}:
            whatActionCheckDid = self.actionCheck(card, objDict, UI)
            if UI and card.value in {'+2', '+4'}: actions += whatActionCheckDid
        self.currentValue = card.value
        self.currentPlayer += self.direction
        self.currentPlayer = self.currentPlayer % self.nPlayers
        if UI: return actions
            # print('SP funct', actions)
            # return actions

    def actionCheck(self, card, objDict, UI = False):
        """Carries out any effects triggered by an action card."""
        if card.value == 'reverse':
            self.direction *= -1
        elif card.value == 'skip':
            self.currentPlayer += self.direction
        elif card.value == '+2' or card.value == '+4':
            self.currentPlayer += self.direction
            self.currentPlayer = self.currentPlayer % self.nPlayers
            if UI: actions = []
            for i in range(int(card.value[-1])):
                card = objDict['player'].all_[self.currentPlayer].draw(objDict, UI)
                if UI: actions.append(('draw', self.currentPlayer, card))
            if UI: return actions
