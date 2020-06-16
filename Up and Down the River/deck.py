# For Up and Down the River project
# Borrowed from Lab 4

import random
from card import Card


class Deck:

    def __init__(self):
        self.thedeck = []
        self.thedeck = self.populate()

    def draw(self):
        if not self.isEmpty():
            return self.thedeck.pop()

    def populate(self):
        deck = []
        infile = open('deck.csv', 'r')
        infile.readline()  # clear first line (headers)
        temp = infile.readlines()
        for line in temp:
            card = line.split(',')
            x = Card(card[1], card[0])
            deck.append(x)
        # save number of cards or something
        return deck

    def add(self, c):
        self.thedeck.append(c)

    def dshuffle(self):
        random.shuffle(self.getDeck())

    def peek(self):
        return self.thedeck[-1]

    def clearDeck(self):
        self.thedeck = []

    def isEmpty(self):
        return self.size() == 0

    def size(self):
        return len(self.thedeck)

    def getDeck(self):
        return self.thedeck

    def replace(self, olddeck):
        self.thedeck = olddeck

    def __len__(self):
        return len(self.thedeck)

    def __iter__(self):
        return _DeckIterator(self.thedeck)

    def __str__(self):
        if self.size() == 1:
            return "Deck has 1 card"
        else:
            return "Deck has " + str(self.size()) + " cards"


class _DeckIterator:

    def __init__(self, theList):
        self._bagItems = theList  # an alias to the list
        self._curItem = 0  # loop index variable

    def __iter__(self):
        return self  # return a reference to the object itself

    def __next__(self):
        if self._curItem < len(self._bagItems):
            item = self._bagItems[self._curItem]  # reference to the indicated item
            self._curItem += 1
            return item
        else:
            raise StopIteration
