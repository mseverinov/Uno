import pygame
import random
import sys

pygame.init()
width = 800
height = 600
gameOver = False

## makes the screen
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Uno')

black = (0,0,0)
white = (255,255,255)
transparent = (0, 0, 0, 0)

cards= ['images/black_+4.png','images/black_+4.png','images/black_+4.png','images/black_+4.png','images/black_wildcard.png','images/black_wildcard.png','images/black_wildcard.png','images/black_wildcard.png',
         'images/blue_+2.png','images/blue_0.png', 'images/blue_1.png', 'images/blue_2.png', 'images/blue_3.png', 'images/blue_4.png', 'images/blue_5.png', 'images/blue_6.png', 'images/blue_7.png', 'images/blue_8.png', 'images/blue_9.png', 'images/blue_reverse.png', 'images/blue_skip.png',
         'images/green_+2.png','images/green_0.png', 'images/green_1.png', 'images/green_2.png', 'images/green_3.png', 'images/green_4.png', 'images/green_5.png', 'images/green_6.png', 'images/green_7.png', 'images/green_8.png', 'images/green_9.png', 'images/green_reverse.png', 'images/green_skip.png',
         'images/red_+2.png','images/red_0.png', 'images/red_1.png', 'images/red_2.png', 'images/red_3.png', 'images/red_4.png', 'images/red_5.png', 'images/red_6.png', 'images/red_7.png', 'images/red_8.png', 'images/red_9.png', 'images/red_reverse.png', 'images/red_skip.png',
         'images/yellow_+2.png','images/yellow_0.png', 'images/yellow_1.png', 'images/yellow_2.png', 'images/yellow_3.png', 'images/yellow_4.png', 'images/yellow_5.png', 'images/yellow_6.png', 'images/yellow_7.png', 'images/yellow_8.png', 'images/yellow_9.png', 'images/yellow_reverse.png', 'images/yellow_skip.png',]
deck = []
discard = []
player1Hand = []
player2Hand = []
player3Hand = []
player4Hand = []
player1XPoints = []
player2XPoints = []
player3XPoints = []
player4XPoints = []
screen.fill(black)

##class Card:
##    """Base class for card representations."""
##    def __init__(self, color, value):
##        """Sets the color and value of the card."""
##        self.color = color #red, plue, green, yellow, wild
##        self.value = value #0-9, +2, +4, skip, reverse, basic
##        #the normal wild (wild without draw for) has color: wild and value: basic
##
##    def __str__(self):
##        return str(self.color) + ' ' + str(self.value)
##
##    def __repr__(self):
##        return str(self.color) + ' ' + str(self.value)

## deals out the cards to players 1-4 and then puts the rest in the draw pile and flips the first card to start the game
## calls helper functions to deal each player
def deal():
    dealPlayer1()
    dealPlayer2()
    dealPlayer3()
    dealPlayer4()
    dealDeck()

## deals all the cards to player 1 and loads them onto the screen, keeping track of what cards are in player 1's hand and where they are on the screen
def dealPlayer1():
    x = 0
    y = 10
    for i in range(1,8):
        randomCard = random.choice(cards)
        image = pygame.image.load(randomCard)
        cards.remove(randomCard)
        player1Hand.append(randomCard)
        screen.blit(image, (x,y))
        player1XPoints.append(x)
        x += 50

## deals all the cards to player 2 and loads them onto the screen, keeping track of what cards are in player 2's hand and where they are on the screen
def dealPlayer2():
    x =  10
    y = 135
    for i in range(1,8):
        randomCard = random.choice(cards)
        image = pygame.image.load(randomCard)
        ## image = pygame.image.load('images/back.png')
        cards.remove(randomCard)
        player2Hand.append(randomCard)
        screen.blit(image, (x,y))
        player2XPoints.append(x)
        x += 25
        
## deals all the cards to player 3 and loads them onto the screen, keeping track of what cards are in player 3's hand and where they are on the screen
def dealPlayer3():
    x =  10
    y = 260
    for i in range(1,8):
        randomCard = random.choice(cards)
        image = pygame.image.load(randomCard)
        ##image = pygame.image.load('images/back.png')
        cards.remove(randomCard)
        player3Hand.append(randomCard)
        screen.blit(image, (x,y))
        player3XPoints.append(x)
        x += 25
        
## deals all the cards to player 4 and loads them onto the screen, keeping track of what cards are in player 4's hand and where they are on the screen
def dealPlayer4():
    x =  10
    y = 385
    for i in range(1,8):
        randomCard = random.choice(cards)
        image = pygame.image.load(randomCard)
        ##image = pygame.image.load('images/back.png')
        cards.remove(randomCard)
        player4Hand.append(randomCard)
        screen.blit(image, (x,y))
        player4XPoints.append(x)
        x += 25

## after cards are dealt to each player, the remaining cards are displayed as a stack in the center of the screen
## and flips the first card over to start the game
def dealDeck():
    x =  540
    y = 260
    for card in cards:
        randomCard = random.choice(cards)
        deck.append(randomCard)
        image = pygame.image.load('images/back.png')
        cards.remove(randomCard)
        screen.blit(image, (x,y))
    discard.append(deck.pop())
    image = pygame.image.load(discard[0])
    screen.blit(image, (440,260))

## when called, will draw a card from the draw pile and add it to player 2's hand
def drawPlayer2():
    card = deck.pop()
    player2Hand.append(card)
    size2X = len(player2XPoints)
    nextPoint = player2XPoints[size2X-1] + 25
    player2XPoints.append(nextPoint)
    image = pygame.image.load('images/back.png')
    screen.blit(image, (nextPoint,135))
    pygame.display.update()

## when called, will draw a card from the draw pile and add it to player 3's hand
def drawPlayer3():
    card = deck.pop()
    player3Hand.append(card)
    size3X = len(player3XPoints)
    nextPoint = player3XPoints[size3X-1] + 25
    player3XPoints.append(nextPoint)
    image = pygame.image.load('images/back.png')
    screen.blit(image, (nextPoint,260))
    pygame.display.update()

## when called, will draw a card from the draw pile and add it to player 4's hand
def drawPlayer4():
    card = deck.pop()
    player4Hand.append(card)
    size4X = len(player4XPoints)
    nextPoint = player4XPoints[size4X-1] + 25
    player4XPoints.append(nextPoint)
    image = pygame.image.load('images/back.png')
    screen.blit(image, (nextPoint,385))
    pygame.display.update()

def chooseCardP2(selectedCard):
    discard.append(selectedCard)
    image = pygame.image.load(selectedCard)
    screen.blit(image, (440,260))
    pygame.display.update()

    player2Hand.remove(selectedCard)
    lastI = len(player2XPoints)-1
    player2XPoints.remove(player2XPoints[lastI])
    pygame.draw.rect(screen, transparent,(10,135,600,125))
    pygame.display.update()

    for x_point in player2XPoints:
        index = player2XPoints.index(x_point)
        card = player2Hand[index]
        image = pygame.image.load(card)
        screen.blit(image, (x_point,135))
        pygame.display.update()

    
def chooseCardP3(selectedCard):
    discard.append(selectedCard)
    image = pygame.image.load(selectedCard)
    screen.blit(image, (440,260))
    pygame.display.update()

    player3Hand.remove(selectedCard)
    lastI = len(player3XPoints)-1
    player3XPoints.remove(player3XPoints[lastI])
    pygame.draw.rect(screen, transparent,(10,260,400,125))
    pygame.display.update()

    for x_point in player3XPoints:
        index = player3XPoints.index(x_point)
        card = player3Hand[index]
        image = pygame.image.load(card)
        screen.blit(image, (x_point,260))
        pygame.display.update()

def chooseCardP4(selectedCard):
    discard.append(selectedCard)
    image = pygame.image.load(selectedCard)
    screen.blit(image, (440,260))
    pygame.display.update()

    player4Hand.remove(selectedCard)
    lastI = len(player4XPoints)-1
    player4XPoints.remove(player4XPoints[lastI])
    pygame.draw.rect(screen, transparent,(10,385,600,125))
    pygame.display.update()

    for x_point in player4XPoints:
        index = player4XPoints.index(x_point)
        card = player4Hand[index]
        image = pygame.image.load(card)
        screen.blit(image, (x_point,385))
        pygame.display.update()
    
deal()
chooseCardP2(random.choice(player2Hand))
chooseCardP3(random.choice(player3Hand))
chooseCardP4(random.choice(player4Hand))
##drawPlayer3()
##drawPlayer4()

pygame.display.update()
while not gameOver: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: ## if there is a mouse click
            if event.pos[0] > 540 and event.pos[0] < 600: 
                if event.pos[1] > 265 and event.pos[1] < 365: ## if the click is on the draw pile -> player 1 gets that card in it's hand
                    card = deck.pop()
                    player1Hand.append(card)
                    size1X = len(player1XPoints)
                    nextPoint = player1XPoints[size1X-1] + 50
                    player1XPoints.append(nextPoint)
                    image = pygame.image.load(card)
                    screen.blit(image, (nextPoint,10))
                    pygame.display.update()
                    
            if event.pos[1] > 10 and event.pos[1] < 110:
                for xPos in player1XPoints:
                    if event.pos[0] > xPos and event.pos[0] < xPos + 50:
                        index = player1XPoints.index(xPos)
                        selectedCard = player1Hand[index]
                        
                        discard.append(selectedCard)
                        image = pygame.image.load(selectedCard)
                        screen.blit(image, (440,260))
                        pygame.display.update()
                        player1Hand.remove(selectedCard)
                        lastI = len(player1XPoints)-1
                        player1XPoints.remove(player1XPoints[lastI])
                        pygame.draw.rect(screen, transparent,(0,10,600,125))
                        pygame.display.update()
                    
                        for x_point in player1XPoints:
                            index = player1XPoints.index(x_point)
                            card = player1Hand[index]
                            image = pygame.image.load(card)
                            screen.blit(image, (x_point,10))
                            pygame.display.update()

                        break
                        

pygame.display.update()

##pygame.quit()
##quit()
