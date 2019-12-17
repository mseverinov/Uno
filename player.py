import random
import math
import numpy

class Player:
    """Base class for player operations"""

    def __init__(self, strategy, complexity = None, container = False):
        """Creates player instance. Adding player to cls.all_"""
        if container:
            self.all_ = []
            self.bot = None
            self.emptySet = set()
        else:
            self.chooseCard = self.chooseRand
            if len(numpy.nonzero(strategy)) == 0:
                self.chooseCard = self.chooseWFitness
            self.strategy = strategy

            if complexity is not None:
                self.complexity = complexity

    def fitness(self, card, handSizes, colorCounts):
        #potentially incorperate state history
        h = 0
        p = self.strategy
        myHandSize = handSizes['my']
        nextHandSize = handSizes['next']
        prevHandSize = handSizes['prev']

        hBool = not(self.complexity['bot hand only'])
        dBool = not(self.complexity['direct only'])
        cBool = self.complexity['color']

        if card.value in {0,1,2,3,4,5,6,7,8,9}:
            h += p[0] + p[7]*myHandSize + nextHandSize*p[14]*hBool + prevHandSize*p[21]*hBool + p[28]/myHandSize*dBool + 1/nextHandSize*p[35]*hBool*dBool* + hBool*dBool*p[42]/prevHandSize
        elif card.value == 'reverse':
            h += p[1] + p[8]*myHandSize + nextHandSize*p[15]*hBool + prevHandSize*p[22]*hBool + p[29]/myHandSize*dBool + 1/nextHandSize*p[36]*hBool*dBool + hBool*dBool*p[43]/prevHandSize
        elif card.value == 'stop':
            h += p[2] + p[9]*myHandSize + nextHandSize*p[16]*hBool + prevHandSize*p[23]*hBool + p[30]/myHandSize*dBool + 1/nextHandSize*p[37]*hBool*dBool + hBool*dBool*p[44]/prevHandSize
        elif card.value == 'skip':
            h += p[3] + p[10]*myHandSize + nextHandSize*p[17]*hBool + prevHandSize*p[24]*hBool + p[31]/myHandSize*dBool + 1/nextHandSize*p[38]*hBool*dBool + hBool*dBool*p[45]/prevHandSize
        elif card.value == '+2':
            h += p[4] + p[11]*myHandSize + nextHandSize*p[18]*hBool + prevHandSize*p[25]*hBool + p[32]/myHandSize*dBool + 1/nextHandSize*p[39]*hBool*dBool + hBool*dBool*p[46]/prevHandSize
        elif card.value == 'basic':
            h += p[5] + p[12]*myHandSize + nextHandSize*p[19]*hBool + prevHandSize*p[26]*hBool + p[33]/myHandSize*dBool + 1/nextHandSize*p[40]*hBool*dBool + hBool*dBool*p[47]/prevHandSize
        elif card.value == '+4':
            h += p[6] + p[13]*myHandSize + nextHandSize*p[20]*hBool + prevHandSize*p[27]*hBool + p[34]/myHandSize*dBool + 1/nextHandSize*p[41]*hBool*dBool + hBool*dBool*p[48]/prevHandSize
        if card.color in {'yellow', 'red', 'blue', 'green'}:
            h += (p[49]*colorCounts[card.color] + p[50]/colorCounts[card.color])*(p[51]*myHandSize + p[52]/myHandSize)

        return h

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

    def chooseColor(self):
        """Finds most commom color in hand that is not "wild." """
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

    def draw(self, objDict, UI = False):
        """Draws a card from the draw pile."""
        #add probability distribution updates here
        card = objDict['draw'].draw(objDict)
        if card != objDict['card'].badCard:
            self.hand.add(card)
        if UI: return card

    def chooseRand(self, objDict):
        "Chooses a card to play from hand."
        for card in self.hand:
            if card.color == 'wild' or card.color == objDict['game'].currentColor or card.value == objDict['game'].currentValue:
                self.hand.remove(card)
                return card
        # if ErrorChecking.handLengths:
        #     ErrorChecking.output += Game.currentColor +' '+ str(Game.currentValue) +' '+ 'Player ' + str(Game.currentPlayer) + str(Player.all_[Game.currentPlayer].hand) + '\n'
        return objDict['card'].badCard

    def chooseWFitness(self, objDict):
        gContainer = objDict['game']
        tF = -math.inf
        tC = objDict['card'].badCard
        handSizes = {}
        handSizes['my'] = len(self.hand)
        handSizes['next'] = len(objDict['player'].all_[(gContainer.currentPlayer + gContainer.direction) % gContainer.nPlayers].hand)
        handSizes['prev'] = len(objDict['player'].all_[(gContainer.currentPlayer - gContainer.direction) % gContainer.nPlayers].hand)
        colors = {card.color for card in self.hand}
        colorCounts = {color:sum([card.color == color for card in self.hand]) for color in colors}
        for card in self.hand:
            if card.color == 'wild' or card.color == gContainer.currentColor or card.value == gContainer.currentValue:
                f = self.fitness(card, handSizes, colorCounts)
                if f > tF:
                    tF = f
                    tC = card
        if tF != -math.inf:
            self.hand.remove(tC)
        return tC
