def fitness(parameters, card):
    #potentially incorperate state history
    h = 0
    p = parameters
    # #game winning cases
    # if len(state.bot.hand) == 1:
    #     if True in [card.color == 'wild' for card in hand]:
    #         return p[0] #should be highest fitness
    #     if hand[0].color == Game.currentColor:
    #         return p[0]
    #
    # #action cards are valuable
    # # add situational awareness
    #     #next player has uno
    #     #next next player has uno
    # for card in hand:
    #     if card.value in ['+2', 'reverse', 'skip', 'wild']: #later add parameter for each card type
    #         #p1 represents value of an action card
    #         #p2 modifies that based on how many are left
    #         #p3 modifies bases on info known about next player
    #         mod = p[1]
    #         mod *= p[2]*info_on_number_of_cards_left()
    #         mod *= len(Player.all_[layer_index + direction].hand)*p[3]
    #         h += mod


    if card.value in {0,1,2,3,4,5,6,7,8,9}:
        h += p[0]
    elif card.value == 'reverse':
        h += p[1]
    elif card.value == 'stop':
        h += p[2]
    elif card.value == 'skip':
        h += p[3]
    elif card.value == '+2':
        h += p[4]
    elif card.value == 'basic':
        h += p[5]
    elif card.value == '+4':
        h += p[6]
    return h
    #
    #
    #
    #
    # #being unable to play a card
    # if len(bot.genValidMoves) == 0:
    #     h += p[4]
    #
    # #modify based on hand handsize
    # h += len(bot.hand)*p[5]
    #
    #
    #
    # #modifywildvalue by relative color rarity
    # if True in [card.color == 'wild' for card in hand]:
    #     potentialIncrease = value
    #     for portionOfCardsHeld in colors:
    #         modify(potentialIncrease)
    #     increase(heuristic by potentialIncrease)
    #
    # #incorperate knowledge about players hands
    # if known that next player does not have color:
    #     if you have a wild:
    #         increase(heuistic)
    #         modifyby(handsize)
    #
    #
    #
    # #modify by your hand size relative to others
    # for player in all_:
    #     base *= len(player.hand)/len(hand)
