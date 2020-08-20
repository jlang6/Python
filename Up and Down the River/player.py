# For Up and Down the River project
# A player will hold cards, bet on the number of tricks they think they will win, and play cards during each trick
# to either win/lose the trick.


from deck import Deck
from card import Card


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.cardsPlayed = []
        self.bets = 0
        self.tricks = 0
        self.points = 0
        self.leader = False
        self.isHuman = True

    # Sorts from smallest to largest values for each suit; combination of insertion sort and my own sorting
    # method (insertion sort code borrowed from Canvas)
    def sortCards(self):
        for to_insert in range(1, len(self.cards)):
            i = to_insert
            while i > 0 and self.cards[i - 1] > self.cards[i]:
                # swap
                temp = self.cards[i]
                self.cards[i] = self.cards[i - 1]
                self.cards[i - 1] = temp
                i -= 1
        suits = ["D", "S", "H", "C"]
        newList = []
        for s in suits:
            for i in self.cards:
                if i.suit == s:
                    newList.append(i)
        self.cards = newList

    def addCard(self, card):
        self.cards.append(card)

    def checkSuit(self, suit):
        for card in self.cards:
            if card.suit == suit:
                return True
        return False

    def makeBet(self, trumpSuit, roundNumber, betSum, dealer):
        c = Card(trumpSuit, "2")
        print("Your hand: ", end="")
        for k in range(len(self.cards) - 1):
            print("%s, " % self.cards[k], end="")
        print("%s" % self.cards[-1], end="")
        print("\nTrump suit:", c.getSuit())

        cannotBet = roundNumber - betSum
        if cannotBet >= 0 and dealer:
            print("You may not bet %d this round\n" % cannotBet)
        bet = input("How many tricks do you think you'll win? ")
        if dealer:
            while not bet.isnumeric() or int(bet) < 0 or (int(bet) + betSum == roundNumber):
                bet = input("Please type the number of bets you think you'll win. You may not bet %s "
                            "this round. " % cannotBet)
        else:
            while not bet.isnumeric() or int(bet) < 0:
                bet = input("Please type the number of bets you think you'll win. ")
        self.bets = int(bet)

    def playCard(self, cardsPlayed, trumpSuit):
        ledCard = None
        if len(cardsPlayed) != 0:
            ledCard = cardsPlayed[0]
        if len(self.cards) == 1:
            return self.cards.pop()
        if self.leader:
            print("Your hand: ", end="")
            for i in range(len(self.cards)-1):
                print("%s (%d), " % (self.cards[i], i + 1), end="")
            print("%s (%d) " % (self.cards[-1], len(self.cards)))
            index = input("Which card to play? (Type the number) ")
            while not index.isnumeric() or int(index) < 0 or int(index) > len(self.cards):
                index = input("Please type the number of the card you wish to play. ")
            card = self.cards[int(index) - 1]
            self.cards.remove(card)
            return card
        else:
            print("You must play a %s if you have one." % ledCard.getSuit()[:-1])
            print("Your hand: ", end="")
            for i in range(len(self.cards) - 1):
                print("%s (%d), " % (self.cards[i], i + 1), end="")
            print("%s (%d) " % (self.cards[-1], len(self.cards)))
            self.widget()
            index = input("\nWhich card to play? (Type the number) ")
            while not index.isnumeric() or int(index) < 0 or int(index) > len(self.cards):
                index = input("Please type the number of the card you wish to play. ")
            print("")
            card = self.cards[int(index) - 1]
            if not self.checkSuit(ledCard.suit):
                self.cards.remove(card)
                return card
            elif self.checkSuit(ledCard.suit) and card.suit == ledCard.suit:
                self.cards.remove(card)
                return card
            else:
                return self.playCard(cardsPlayed, trumpSuit)

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
            diff = abs(self.tricks - self.bets)
            self.points -= diff * 5
            
            
