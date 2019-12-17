import pygame
import sys

class UI:

    def __init__(self, UIdeck):
        self.drawMap = {0:self.drawPlayer1, 1:self.drawPlayer2, 2:self.drawPlayer3, 3:self.drawPlayer4}
        self.discardMap = {0:self.discardCardP1, 1:self.discardCardP2, 2:self.discardCardP3, 3:self.discardCardP4}
        pygame.init()
        width = 800
        height = 600
        gameOver = False

        ## makes the screen
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Uno')

        black = (0,0,0)
        white = (255,255,255)
        self.transparent = (0, 0, 0, 0)

        self.cards= ['images/black_+4.png','images/black_+4.png','images/black_+4.png','images/black_+4.png','images/black_wildcard.png','images/black_wildcard.png','images/black_wildcard.png','images/black_wildcard.png',
                 'images/blue_+2.png','images/blue_0.png', 'images/blue_1.png', 'images/blue_2.png', 'images/blue_3.png', 'images/blue_4.png', 'images/blue_5.png', 'images/blue_6.png', 'images/blue_7.png', 'images/blue_8.png', 'images/blue_9.png', 'images/blue_reverse.png', 'images/blue_skip.png',
                 'images/green_+2.png','images/green_0.png', 'images/green_1.png', 'images/green_2.png', 'images/green_3.png', 'images/green_4.png', 'images/green_5.png', 'images/green_6.png', 'images/green_7.png', 'images/green_8.png', 'images/green_9.png', 'images/green_reverse.png', 'images/green_skip.png',
                 'images/red_+2.png','images/red_0.png', 'images/red_1.png', 'images/red_2.png', 'images/red_3.png', 'images/red_4.png', 'images/red_5.png', 'images/red_6.png', 'images/red_7.png', 'images/red_8.png', 'images/red_9.png', 'images/red_reverse.png', 'images/red_skip.png',
                 'images/yellow_+2.png','images/yellow_0.png', 'images/yellow_1.png', 'images/yellow_2.png', 'images/yellow_3.png', 'images/yellow_4.png', 'images/yellow_5.png', 'images/yellow_6.png', 'images/yellow_7.png', 'images/yellow_8.png', 'images/yellow_9.png', 'images/yellow_reverse.png', 'images/yellow_skip.png',]

        for card in UIdeck:
            if card.color == 'wild':
                card.color = 'black'
            if card.value == 'basic':
                card.value = 'wildcard'
        # print(UIdeck)

        self.cardMap = {card:'images/' + card.color + '_' + str(card.value) + '.png' for card in UIdeck}
        self.reverseMap = {'images/' + card.color + '_' + str(card.value) + '.png':card for card in UIdeck}
        self.deck = []
        self.discard = []
        self.player1Hand = []
        self.player2Hand = []
        self.player3Hand = []
        self.player4Hand = []
        self.player1XPoints = []
        self.player2XPoints = []
        self.player3XPoints = []
        self.player4XPoints = []
        self.screen.fill(black)
        self.turnCondition = True
        self.dealDeck(card)



    ## deals all the cards to player 1 and loads them onto the screen, keeping track of what cards are in player 1's hand and where they are on the screen
    def dealPlayer1(self, hand):
        x = 0
        y = 10
        for card in hand:
            image = pygame.image.load(self.cardMap[card])
            self.player1Hand.append(self.cardMap[card])
            self.screen.blit(image, (x,y))
            self.player1XPoints.append(x)
            x += 50

    ## deals all the cards to player 2 and loads them onto the screen, keeping track of what cards are in player 2's hand and where they are on the screen
    def dealPlayer2(self, hand):
        x =  10
        y = 135
        for card in hand:
            image = pygame.image.load(self.cardMap[card])
            self.player2Hand.append(self.cardMap[card])
            self.screen.blit(image, (x,y))
            self.player2XPoints.append(x)
            x += 25

    ## deals all the cards to player 3 and loads them onto the screen, keeping track of what cards are in player 3's hand and where they are on the screen
    def dealPlayer3(self, hand):
        x =  10
        y = 260
        for card in hand:
            image = pygame.image.load(self.cardMap[card])
            self.player3Hand.append(self.cardMap[card])
            self.screen.blit(image, (x,y))
            self.player3XPoints.append(x)
            x += 25

    ## deals all the cards to player 4 and loads them onto the screen, keeping track of what cards are in player 4's hand and where they are on the screen
    def dealPlayer4(self, hand):
        x =  10
        y = 385
        for card in hand:
            image = pygame.image.load(self.cardMap[card])
            self.player4Hand.append(self.cardMap[card])
            self.screen.blit(image, (x,y))
            self.player4XPoints.append(x)
            x += 25

## after cards are dealt to each player, the remaining cards are displayed as a stack in the center of the screen
## and flips the first card over to start the game
    def dealDeck(self, card = None):
        x =  540
        y = 260
        image = pygame.image.load('images/back.png')
        self.screen.blit(image, (x,y))
        # image = pygame.image.load(self.cardMap[card])
        # self.screen.blit(image, (440,260))

    def draw(self, player, card):
        self.drawMap[player](card)

    def drawPlayer1(self, card):
        self.player1Hand.append(self.cardMap[card])
        size1X = len(self.player1XPoints)
        nextPoint = self.player1XPoints[size1X-1] + 25
        self.player1XPoints.append(nextPoint)
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (nextPoint,10))
        pygame.display.update()

    ## when called, will draw a card from the draw pile and add it to player 2's hand
    def drawPlayer2(self, card):
        self.player2Hand.append(self.cardMap[card])
        size2X = len(self.player2XPoints)
        nextPoint = self.player2XPoints[size2X-1] + 25
        self.player2XPoints.append(nextPoint)
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (nextPoint,135))
        pygame.display.update()

    ## when called, will draw a card from the draw pile and add it to player 3's hand
    def drawPlayer3(self, card):
        self.player3Hand.append(self.cardMap[card])
        size3X = len(self.player3XPoints)
        nextPoint = self.player3XPoints[size3X-1] + 25
        self.player3XPoints.append(nextPoint)
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (nextPoint,260))
        pygame.display.update()

    ## when called, will draw a card from the draw pile and add it to player 4's hand
    def drawPlayer4(self, card):
        self.player4Hand.append(self.cardMap[card])
        size4X = len(self.player4XPoints)
        nextPoint = self.player4XPoints[size4X-1] + 25
        self.player4XPoints.append(nextPoint)
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (nextPoint,385))
        pygame.display.update()

    def discardfoo(self, player, card):
        # print(self.player1Hand)
        # print(self.player2Hand)
        # print(self.player3Hand)
        # print(self.player4Hand)
        # print(card)
        # print(self.cardMap[card])
        print('p'+str(player+1), 'discarded', card)
        self.discardMap[player](card)

    def discardCardP1(self, card):
        self.discard.append(self.cardMap[card])
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (440,260))
        pygame.display.update()
        self.player1Hand.remove(self.cardMap[card])
        lastI = len(self.player1XPoints)-1
        self.player1XPoints.remove(self.player1XPoints[lastI])
        pygame.draw.rect(self.screen, self.transparent,(0,10,600,125))
        pygame.display.update()

        for x_point in self.player1XPoints:
            index = self.player1XPoints.index(x_point)
            card = self.player1Hand[index]
            image = pygame.image.load(card)
            self.screen.blit(image, (x_point,10))
            pygame.display.update()

    def discardCardP2(self, card):
        self.discard.append(self.cardMap[card])
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (440,260))
        pygame.display.update()

        self.player2Hand.remove(self.cardMap[card])
        lastI = len(self.player2XPoints)-1
        self.player2XPoints.remove(self.player2XPoints[lastI])
        pygame.draw.rect(self.screen, self.transparent,(10,135,600,125))
        pygame.display.update()

        for x_point in self.player2XPoints:
            index = self.player2XPoints.index(x_point)
            card = self.player2Hand[index]
            image = pygame.image.load(card)
            self.screen.blit(image, (x_point,135))
            pygame.display.update()

    def discardCardP3(self, card):
        # print(card)
        # print(self.cardMap[card])
        self.discard.append(self.cardMap[card])
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (440,260))
        pygame.display.update()

        self.player3Hand.remove(self.cardMap[card])
        lastI = len(self.player3XPoints)-1
        self.player3XPoints.remove(self.player3XPoints[lastI])
        pygame.draw.rect(self.screen, self.transparent, (10,260,400,125))
        pygame.display.update()

        for x_point in self.player3XPoints:
            index = self.player3XPoints.index(x_point)
            card = self.player3Hand[index]
            image = pygame.image.load(card)
            self.screen.blit(image, (x_point,260))
            pygame.display.update()

    def discardCardP4(self, card):
        self.discard.append(self.cardMap[card])
        image = pygame.image.load(self.cardMap[card])
        self.screen.blit(image, (440,260))
        pygame.display.update()

        self.player4Hand.remove(self.cardMap[card])
        lastI = len(self.player4XPoints)-1
        self.player4XPoints.remove(self.player4XPoints[lastI])
        pygame.draw.rect(self.screen, self.transparent,(10,385,600,125))
        pygame.display.update()

        for x_point in self.player4XPoints:
            index = self.player4XPoints.index(x_point)
            card = self.player4Hand[index]
            image = pygame.image.load(card)
            self.screen.blit(image, (x_point,385))
            pygame.display.update()



    def humanTurn(self, drawnCard = None):
        print('v')
        events = []
        drawn = False
        while True:
            # print('y')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('quitted')
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: ## if there is a mouse click
                    if not drawn:
                        print('sdf')
                        if event.pos[0] > 540 and event.pos[0] < 600:
                            if event.pos[1] > 265 and event.pos[1] < 365: ## if the click is on the draw pile -> player 1 gets that card in it's hand
                                if self.turnCondition: return 'draw a card'
                                drawn = True
                                self.player1Hand.append(self.cardMap[drawnCard])
                                size1X = len(self.player1XPoints)
                                nextPoint = self.player1XPoints[size1X-1] + 50
                                self.player1XPoints.append(nextPoint)
                                print(self.cardMap[drawnCard])
                                image = pygame.image.load(self.cardMap[drawnCard])
                                self.screen.blit(image, (nextPoint,10))
                                pygame.display.update()

                    if event.pos[1] > 10 and event.pos[1] < 110:
                        for xPos in self.player1XPoints:
                            if event.pos[0] > xPos and event.pos[0] < xPos + 50:
                                index = self.player1XPoints.index(xPos)
                                selectedCard = self.player1Hand[index]
                                self.discard.append(selectedCard)
                                image = pygame.image.load(selectedCard)
                                self.screen.blit(image, (440,260))
                                pygame.display.update()
                                self.player1Hand.remove(selectedCard)
                                lastI = len(self.player1XPoints)-1
                                self.player1XPoints.remove(self.player1XPoints[lastI])
                                pygame.draw.rect(self.screen, self.transparent,(0,10,600,125))
                                pygame.display.update()

                                for x_point in self.player1XPoints:
                                    index = self.player1XPoints.index(x_point)
                                    card = self.player1Hand[index]
                                    image = pygame.image.load(card)
                                    self.screen.blit(image, (x_point,10))
                                    pygame.display.update()

                                return ('discard', self.reverseMap[selectedCard])
# deal()
# chooseCardP2(random.choice(player2Hand))
# chooseCardP3(random.choice(player3Hand))
# chooseCardP4(random.choice(player4Hand))
# ##drawPlayer3()
# ##drawPlayer4()

# pygame.display.update()
# while not gameOver:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN: ## if there is a mouse click
#             if event.pos[0] > 540 and event.pos[0] < 600:
#                 if event.pos[1] > 265 and event.pos[1] < 365: ## if the click is on the draw pile -> player 1 gets that card in it's hand
#                     card = deck.pop()
#                     player1Hand.append(card)
#                     size1X = len(player1XPoints)
#                     nextPoint = player1XPoints[size1X-1] + 50
#                     player1XPoints.append(nextPoint)
#                     image = pygame.image.load(card)
#                     screen.blit(image, (nextPoint,10))
#                     pygame.display.update()
#
#             if event.pos[1] > 10 and event.pos[1] < 110:
#                 for xPos in player1XPoints:
#                     if event.pos[0] > xPos and event.pos[0] < xPos + 50:
#                         index = player1XPoints.index(xPos)
#                         selectedCard = player1Hand[index]
#
#                         discard.append(selectedCard)
#                         image = pygame.image.load(selectedCard)
#                         screen.blit(image, (440,260))
#                         pygame.display.update()
#                         player1Hand.remove(selectedCard)
#                         lastI = len(player1XPoints)-1
#                         player1XPoints.remove(player1XPoints[lastI])
#                         pygame.draw.rect(screen, self.transparent,(0,10,600,125))
#                         pygame.display.update()
#
#                         for x_point in player1XPoints:
#                             index = player1XPoints.index(x_point)
#                             card = player1Hand[index]
#                             image = pygame.image.load(card)
#                             screen.blit(image, (x_point,10))
#                             pygame.display.update()
#
#                         break
#
#
# pygame.display.update()

##pygame.quit()
##quit()
