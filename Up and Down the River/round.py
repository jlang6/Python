# For Up and Down the River project
# At the beginning of the round, the deck will be shuffled, cards dealt out, and the top card will be the trump
# suit. During each rounds, players will bet on the number of tricks they'll win, play cards and win/lose tricks, and
# either lose or gain points depending on if they meet their bets or not.


from deck import Deck
from card import Card
from player import Player
from computer import Computer
from time import sleep
from datetime import datetime
import random, os, winsound


class Round:

    def __init__(self, roundNumber, playerList):
        self.roundNumber = roundNumber
        self.trumpSuit = None
        self.deck = Deck()
        self.dealer = playerList[-1]
        self.playerList = playerList

        playerList[0].leader = True
        self.deck.dshuffle()
        count = 0
        while self.deck.size() >= len(playerList) and count != roundNumber:  # Cards dealt evenly & until the round #
            for player in self.playerList:
                player.addCard(self.deck.draw())
            count += 1
        for player in self.playerList:
            player.sortCards()
        self.topCard = self.deck.draw()  # After cards are dealt, top card is revealed and determines trump suit
        self.trumpSuit = self.topCard.suit
        self.sounds = True
        if os.name != 'nt':
            self.sounds = False

    def bets(self):
        # We keep track of the sum of bets since it cannot be the same as the amount of cards players start with for
        # the round (as in at least one person will fail to meet his/her bet).
        if self.sounds:
            winsound.PlaySound("shuffle.wav", winsound.SND_ALIAS)
        betSum = 0
        print("%s is the dealer and bets last.\n" % self.dealer.name)
        for i in range(len(self.playerList)):
            if i == len(self.playerList) - 1:
                self.playerList[i].makeBet(self.trumpSuit, self.roundNumber, betSum, True)
            else:
                self.playerList[i].makeBet(self.trumpSuit, self.roundNumber, betSum, False)
            print("%s bets: %d\n" % (self.playerList[i].name, self.playerList[i].bets))
            betSum += self.playerList[i].bets
        sleep(2)

    # The list will remove the last person and insert him/her at the front until the front person is the leader.
    def reorganize(self, winner):
        while self.playerList[0] != winner:
            back = self.playerList.pop()
            self.playerList.insert(0, back)

    def updateCards(self, card):
        for player in self.playerList:
            player.cardsPlayed.append(card)

    def trick(self):
        # The leader starts the trick. Here the suit in the playCard function doesn't matter. Cards are stored in
        # a list and compared at the end of the trick.

        # FOR TESTING PURPOSES
        # for i in range(len(self.playerList)):
        #     self.playerList[i].sortCards()
        #     print(self.playerList[i].name, ":", end="")
        #     for j in self.playerList[i].cards:
        #         print(j, ", ", end="")
        #     print()

        # Each player plays a card, following the suit of the leader's card.
        cards = []
        for i in range(0, len(self.playerList)):
            temp = self.playerList[i].playCard(cards, self.trumpSuit)
            if temp is None:
                # Back-up function that plays the first eligible card
                temp = self.playerList[i].simplePlay(cards)
                self.errorLog(cards, self.playerList[i], temp)
            self.updateCards(temp)
            cards.append(temp)
            if self.sounds:
                winsound.PlaySound("flop.wav", winsound.SND_ALIAS)
            print("%s plays %s\n" % (self.playerList[i].name, temp))

        highCard = self.determineHighestCard(self.trumpSuit, cards)  # Function for getting high card
        winner = self.playerList[cards.index(highCard)]  # Winner is highest card
        winner.winTrick()  # Winner's tricks increase by 1
        print("%s wins the trick with %s!" % (winner.name, highCard))
        self.playerList[0].leader = False
        winner.leader = True
        self.reorganize(winner)  # The player list is organized so the leader is always first and order is maintained
        sleep(2)

    # Once a round is over, scores are updated for each player and their cards, bets, and tricks are reset.
    def end(self):
        for i in self.playerList:
            i.changePoints()
            i.clearRound()
        while self.dealer != self.playerList[-2]:  # List is rotated so order is maintained and leader is first item
            back = self.playerList.pop()
            self.playerList.insert(0, back)

    # Similar to the recursive function for getting the maximum of a list that we designed in Lab 9. The first
    # card in the list is set as the max, and then it is compared one at a time with each other item in the list.
    def determineHighestCard(self, trumpSuit, cardList, maximum=0, i=0):
        # Base case: once i is the length of the card list, the list has been checked and the max is returned
        if i == len(cardList):
            return maximum
        # First card is automatically the max. Every recursion the current max is checked against the next item.
        if i == 0:
            maximum = cardList[0]
        else:
            if maximum.suit == trumpSuit or cardList[i].suit == trumpSuit:
                # If only one of the cards is trump suit, it wins. Else, values are compared
                if maximum.suit == trumpSuit and cardList[i].suit != trumpSuit:
                    pass
                elif maximum.suit != trumpSuit and cardList[i].suit == trumpSuit:
                    maximum = cardList[i]
                else:
                    temp = max(maximum.getVal(), cardList[i].getVal())
                    if temp == maximum.getVal():
                        pass
                    else:
                        maximum = cardList[i]
            elif cardList[i].suit != cardList[0].suit:
                # If next card isn't the lead suit, it loses (since first card is automatically the max and lead suit)
                pass
            else:
                temp = max(maximum.getVal(), cardList[i].getVal())  # If both are from lead suit, we check values
                if temp == maximum.getVal():
                    pass
                else:
                    maximum = cardList[i]
        return self.determineHighestCard(trumpSuit, cardList, maximum, i + 1)

    def errorLog(self, cards, player, simplePlay):
        # Prints error log with trump, cards played, and error player's hand
        outfile = open("Error Log.txt", "a", encoding="utf8")
        dateTimeObj = datetime.now()
        print("%d-%d-%d, %d:%s" % (dateTimeObj.month, dateTimeObj.day, dateTimeObj.year,
                                   dateTimeObj.hour, dateTimeObj.minute), file=outfile)
        print("Value Error: playCard function returned a null value instead of a card", file=outfile)
        print("Trump suit: ", self.trumpSuit, file=outfile)
        print("Cards already played (in order): ", cards, file=outfile)
        print("%s's cards: " % player.name, end="", file=outfile)
        for c in range(len(player.cards) - 1):
            print(player.cards[c], ", ", end="", file=outfile)
        print(player.cards[-1], file=outfile)
        print("Card played using simplePlay: %s" % simplePlay, file=outfile)
        print("\n", file=outfile)

