# For Up and Down the River project
# A player will hold cards, bet on the number of tricks they think they will win, and play cards during each trick
# to either win/lose the trick.


from deck import Deck
from card import Card
import random


class Computer:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.cardsPlayed = []
        self.bets = 0
        self.tricks = 0
        self.points = 0
        self.leader = False
        self.isHuman = False

    # Sorts from smallest to largest values, ignoring suit (since the CPU's cards won't be displayed); uses
    # insertion sort (code borrowed from Canvas)
    def sortCards(self):
        for i in range(len(self.cards)):
            minIndex = i
            for j in range(i + 1, len(self.cards)):
                if self.cards[j] < self.cards[minIndex]:
                    minIndex = j
            if minIndex != i:
                temp = self.cards[i]
                self.cards[i] = self.cards[minIndex]
                self.cards[minIndex] = temp

    # Adds a card to hand
    def addCard(self, card):
        self.cards.append(card)

    # ADJUST TRUMP CARDS AND SYSTEM FOR BETS
    def makeBet(self, trumpSuit, roundNumber, betSum, dealer):
        trumpCards = 0
        if roundNumber >= 7:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                if card.suit != trumpSuit and card.getVal() > 10:
                    self.bets += 1
                elif card.suit == trumpSuit and card.getVal() > 9:
                    self.bets += 1
        if roundNumber == 6:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                if card.suit != trumpSuit and card.getVal() > 9:
                    self.bets += 1
                elif card.suit == trumpSuit and card.getVal() > 8:
                    self.bets += 1
        if roundNumber == 5:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                if card.suit != trumpSuit and card.getVal() > 10:
                    self.bets += 1
                elif card.suit == trumpSuit and card.getVal() > 6:
                    self.bets += 1
        if roundNumber == 4:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                if card.suit != trumpSuit and card.getVal() > 11:
                    self.bets += 1
                elif card.suit == trumpSuit and card.getVal() > 5:
                    self.bets += 1
        if roundNumber == 3:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                if card.suit != trumpSuit and card.getVal() > 11:
                    self.bets += 1
                elif card.suit == trumpSuit:
                    self.bets += 1
        if dealer and roundNumber == 1 or roundNumber == 2:
            for card in self.cards:
                if card.getVal() > 12:
                    self.bets += 1
        if roundNumber == 1 or roundNumber == 2:
            for card in self.cards:
                if card.suit == trumpSuit:
                    trumpCards += 1
                    self.bets += 1
        if self.bets > round(roundNumber / 2):
            self.bets = round(roundNumber / 2)
        if dealer and self.bets == roundNumber - betSum:
            # If the bet is equal to the number of cards, go down 1 (you can't win more tricks than # of total tricks)
            if self.bets == roundNumber:
                self.bets -= 1
            # Negative bets will never be matched
            elif self.bets == 0:
                self.bets += 1
            else:
                if self.bets >= round(roundNumber / 2):
                    self.bets -= 1
                else:
                    if trumpCards > roundNumber // 2:
                        self.bets += 1
                    else:
                        self.bets -= 1

    # Check for whether a CPU has made its bet or not, which determines whether its strategy will be to win or lose
    # upcoming tricks.
    def madeBet(self):
        return self.tricks >= self.bets

    def checkSuit(self, suit):
        for c in self.cards:
            if c.suit == suit:
                return True
        return False

    # Returns largest card of the winning suit that is smaller than the current winner
    def getSuitMaxLose(self, currentWinner):
        self.sortCards()
        for i in range(len(self.cards)):
            # Once it finds first card that's bigger, it iterates backwards to get next smallest of same suit
            if self.cards[i].suit == currentWinner.suit and self.cards[i] > currentWinner:
                for j in range(i, -1, -1):
                    if self.cards[j].suit == currentWinner.suit:
                        return self.cards[j]
        # If all your cards are smaller than the winner, you can play the biggest one and still lose the trick
        for k in range(len(self.cards)-1, -1, -1):
            if self.cards[k].suit == currentWinner.suit:
                return self.cards[k]

    # Returns smallest card in your hand (non-trump if possible)
    def getAbsoluteMinimum(self, trumpSuit):
        self.sortCards()
        if self.checkSuit(trumpSuit):
            for c in self.cards:
                if c.suit != trumpSuit:
                    return c
        return self.cards[0]

    # Returns the smallest card of a given suit
    def getSmallestSuit(self, givenSuit):
        self.sortCards()
        for c in self.cards:
            if c.suit == givenSuit:
                return c

    # Returns smallest card that beats the current winning card (whether it's trump or a different
    # suit)
    def getSmallestToWin(self, currentWinner):
        winningSuit = currentWinner.suit
        self.sortCards()
        for c in self.cards:
            if c.suit == winningSuit and c > currentWinner:
                return c

    # Returns the largest non-trump card
    def getLargestNonTrump(self, trumpSuit):
        self.sortCards()
        for i in range(len(self.cards) - 1, -1, -1):
            if self.cards[i].suit != trumpSuit:
                return self.cards[i]

    # Returns the largest card of the given suit
    def getLargestToWin(self, ledSuit, currentWinner):
        maximum = self.cards[0]
        for card in self.cards:
            # If the card is the correct suit and will beat the current winner
            if card.suit == ledSuit and card > currentWinner:
                if maximum.suit == ledSuit and card > maximum:
                    maximum = card
                elif maximum.suit != ledSuit:
                    maximum = card
        return maximum

    # Returns the largest card in hand
    def getLargestCard(self):
        self.sortCards()
        return self.cards[-1]

    # Returns the largest card of the given suit
    def getLargestSuit(self, givenSuit):
        self.sortCards()
        for i in range(len(self.cards)-1, -1, -1):
            if self.cards[i].suit == givenSuit:
                return self.cards[i]

    # Given the cards played and trump suit: returns which card is currently winning (since the round may not be over)
    def getCurrentWinner(self, cardsPlayed, trumpSuit):
        if len(cardsPlayed) == 0:
            return None
        winner = cardsPlayed[0]
        for card in cardsPlayed:
            if winner.suit != trumpSuit and card.suit == trumpSuit:
                winner = card
            elif winner.suit == trumpSuit and card.suit != trumpSuit:
                pass
            else:
                if card > winner:
                    winner = card
        return winner

    def playCard(self, cardsPlayed, trumpSuit):
        if len(cardsPlayed) == 0:
            ledSuit = None
        else:
            ledSuit = cardsPlayed[0].suit

        if len(self.cards) == 1:
            return self.cards[0]

        currentWinner = self.getCurrentWinner(cardsPlayed, trumpSuit)
        # When no more tricks need to be won
        if self.madeBet():
            # Play lowest non-trump card
            if self.leader:
                card = self.getAbsoluteMinimum(trumpSuit)
                self.cards.remove(card)
                return card
            # Play lowest card of led suit; if no cards of led suit, play lowest non-trump card
            else:
                # When you have a card of the led suit (and thus must play one)
                if self.checkSuit(ledSuit):
                    # If led suit is not trump or the current winner is not trump, and you have a led suit card,
                    # you should play the biggest card smaller than the current winner.
                    # Or if the led suit is trump,
                    if currentWinner.suit != trumpSuit or ledSuit == trumpSuit:
                        card = self.getSuitMaxLose(currentWinner)
                        # If none of your cards is smaller
                        if card is None:
                            card = self.getSmallestSuit(ledSuit)
                            self.cards.remove(card)
                            return card
                        # If none of your cards is smaller
                        else:
                            self.cards.remove(card)
                            return card
                    # If the current winner is a trump but the led suit isn't, then play your largest led suit card
                    # (because you want to get rid of big cards without winning if you've matched your bet)
                    else:
                        card = self.getLargestSuit(ledSuit)
                        self.cards.remove(card)
                        return card
                # If you can play any card, play your smallest trump that will lose
                # (if currentWinner is trump) or largest non-trump
                elif currentWinner.suit == trumpSuit and self.checkSuit(trumpSuit):
                    card = self.getSuitMaxLose(currentWinner)
                    # If none of your cards is smaller
                    if card is not None:
                        self.cards.remove(card)
                        return card
                # If you don't have smaller trump cards (and currentWinner is trump), play your largest non-trump
                card = self.getLargestNonTrump(trumpSuit)
                self.cards.remove(card)
                return card
        # When tricks still need to be won
        else:
            # When you're the leader
            if self.leader:
                # Play your largest card possible
                card = self.getLargestCard()
                self.cards.remove(card)
                return card
            # When you're not the leader
            else:
                # If you have a card of the led suit
                if self.checkSuit(ledSuit):
                    # If you have to play a led card when someone's already played trump, you will automatically lose
                    if ledSuit != trumpSuit and currentWinner.suit == trumpSuit:
                        card = self.getSmallestSuit(ledSuit)
                        self.cards.remove(card)
                        return card
                    # If you can win the trick as the last player, play the smallest card you can win with (if you
                    # can't win, getSmallestToWin returns getSmallestSuit (following led suit)
                    elif currentWinner.suit == ledSuit and len(cardsPlayed) == 3:
                        card = self.getSmallestToWin(currentWinner)
                        # If there is no card bigger than the leader, you can't win --> play smallest card of led suit
                        if card is None:
                            card = self.getSmallestSuit(ledSuit)
                            self.cards.remove(card)
                            return card
                        else:
                            self.cards.remove(card)
                            return card
                    # If you could win, play biggest card of the led suit (if it will win), else play smallest of
                    # led suit
                    elif currentWinner.suit == ledSuit and len(cardsPlayed) < 3:
                        card = self.getLargestSuit(ledSuit)
                        # Play if able to win
                        if card > currentWinner:
                            self.cards.remove(card)
                            return card
                    # If no card from your hand can beat the currentWinner, then play the smallest card possible
                    # (following led suit)
                    card = self.getSmallestSuit(ledSuit)
                    self.cards.remove(card)
                    return card
                # If you don't have a card of the led suit, you're free to play any card
                else:
                    if self.checkSuit(trumpSuit):
                        if currentWinner.suit == trumpSuit:
                            # In this case, play your smallest trump that will still win
                            if self.bets - self.tricks > 1 and len(cardsPlayed) == 3:
                                card = self.getSmallestToWin(currentWinner)
                                # If you have no trump that can win --> play smallest card possible
                                if card is None:
                                    card = self.getAbsoluteMinimum(trumpSuit)
                                    self.cards.remove(card)
                                    return card
                                else:
                                    self.cards.remove(card)
                                    return card
                            else:
                                card = self.getLargestSuit(trumpSuit)
                                if card > currentWinner:
                                    self.cards.remove(card)
                                    return card
                                # If none of your trump cards can beat the current winning trump, play lowest card
                                else:
                                    card = self.getAbsoluteMinimum(trumpSuit)
                                    self.cards.remove(card)
                                    return card
                        # Else, if the current winner is not trump but you have trump, you can win
                        else:
                            # If you have at least 2 tricks left to win (and should save trump cards for later rounds)
                            # or are last (and thus know any trump will win), play the smallest trump in your hand
                            if self.bets - self.tricks > 1 and len(cardsPlayed) == 3:
                                card = self.getSmallestSuit(trumpSuit)
                                self.cards.remove(card)
                                return card
                            # Else, if you're not last to play or need only 1 trick, then play your largest trump
                            # card (in case next person has a bigger trump or to prevent having bigger trump cards
                            # left in your hand when you've already made your bet)
                            else:
                                card = self.getLargestSuit(trumpSuit)
                                self.cards.remove(card)
                                return card
                    # If you have no trump or led suit cards, throw away your lowest card
                    else:
                        card = self.getAbsoluteMinimum(trumpSuit)
                        self.cards.remove(card)
                        return card

    # Function used only when the playCard function returns a null value (because of an undiscovered error)
    def simplePlay(self, cardsPlayed):
        lsuit = False
        ledSuit = None
        if len(cardsPlayed) != 0:
            ledSuit = cardsPlayed[0].suit
            if self.checkSuit(ledSuit):
                lsuit = True
        if self.madeBet():
            for card in self.cards:
                if lsuit:
                    if card.suit == ledSuit:
                        return card
                else:
                    return card
        else:
            for i in range(len(self.cards), 0, -1):
                if lsuit:
                    if self.cards[i].suit == ledSuit:
                        return self.cards[i]
                else:
                    return self.cards[i]

    def winTrick(self):
        self.tricks += 1

    def clearRound(self):
        self.cards = []
        self.cardsPlayed = []
        self.bets = 0
        self.tricks = 0
        self.leader = False

    def changePoints(self):
        if self.tricks == self.bets:
            self.points += 5 + (5 * self.bets)
        else:
            lostPoints = abs(self.tricks - self.bets)
            self.points -= lostPoints * 5
