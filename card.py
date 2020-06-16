# For Up and Down the River project
# Borrowed from Lab 4


class Card:

    def __init__(self, csuit, cval):
        self.suit = csuit
        self.val = cval
        self.color = ""
        black = ["S", "C"]
        if self.suit in black:
            self.color = "black"
        else:
            self.color = "red"

    def getSuit(self):
        if self.suit == "C":
            return "Clubs"
        elif self.suit == "H":
            return "Hearts"
        elif self.suit == "S":
            return "Spades"
        else:
            return "Diamonds"

    def getVal(self):
        if self.val == "A":
            return int(14)
        elif self.val == "K":
            return int(13)
        elif self.val == "Q":
            return int(12)
        elif self.val == "J":
            return int(11)
        else:
            return int(self.val)

    def convertVal(self):
        if self.val == "A":
            return "Ace"
        elif self.val == "K":
            return "King"
        elif self.val == "Q":
            return "Queen"
        elif self.val == "J":
            return "Jack"
        else:
            return str(self.val)

    def getcolor(self):
        return self.color

    # I adjusted the equals function to check value and suit. I had issues with the wrong card being removed
    # if a player had two of the same value and played the rightmost one. Problem solved finally!
    def __eq__(self, card):
        return (self.getVal() == card.getVal()) and (self.getSuit() == card.getSuit())

    def __str__(self):
        return self.convertVal() + " of " + self.getSuit()

    def __lt__(self, card):
        return self.getVal() < card.getVal()

    def __le__(self, card):
        return self.getVal() <= card.getVal()

    def __gt__(self, card):
        return self.getVal() > card.getVal()

    def __ge__(self, card):
        return self.getVal() >= card.getVal()
