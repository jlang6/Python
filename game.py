# For Up and Down the River project


from deck import Deck
from card import Card
from player import Player
from computer import Computer
from round import Round
import random, os
from time import sleep
from datetime import datetime
import winsound


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Game:

    def __init__(self):
        clear()
        self.numPlayers = 4
        self.roundNumber = 1
        self.cpu1 = Computer("CPU 1")
        self.cpu2 = Computer("CPU 2")
        self.cpu3 = Computer("CPU 3")
        name = ""
        while name == "":
            name = input("What is your name? ")
        self.human = Player(name)
        self.players = [self.cpu1, self.cpu2, self.cpu3, self.human]
        self.playerList = [self.cpu1, self.cpu2, self.cpu3, self.human]  # Copy is made because order will be changed

    def start(self):
        yesPossible = ["Y", "YES"]
        possible = ["Y", "YES", "N", "NO"]
        answer = input("Do you want to read the rules first? (Y/N) ")
        answer = answer.upper()
        while answer not in possible:
            answer = input("Please answer yes or no. ")
            answer = answer.upper()
        if answer in yesPossible:
            self.rules()

    def rules(self):
        clear()
        infile = open("rules.txt", "r", encoding="utf8")
        for line in infile:
            print(line.strip())
        answer = 0
        while answer != "":
            answer = input("Press enter when you're ready to play...")
        clear()

    def updateDisplay(self, roundNumber, trumpSuit, dealer):
        clear()
        print("Round %s | Trump suit: %s" % (roundNumber, trumpSuit))
        for player in self.players:
            if player == dealer:
                print("%-9s (Dealer) - Bets: %d, Tricks: %d, Points: %d" % (
                    player.name, player.bets, player.tricks, player.points))
            else:
                print("%-18s - Bets: %d, Tricks: %d, Points: %d" % (
                    player.name, player.bets, player.tricks, player.points))
        print()

    def pointsDisplay(self, roundNumber, dealer):
        # Once the game's over, we want don't want to output the results here and with end game function
        if self.roundNumber != 16:
            clear()
            print("End of Round %s" % roundNumber)
            for player in self.players:
                if player == dealer:
                    print("%-9s (Dealer) - Points: %d" % (player.name, player.points))
                else:
                    print("%-18s - Points: %d" % (player.name, player.points))
            print()

    def determineWinners(self, players):
        winners = []
        maximum = players[0].points
        winners.append(players[0])
        for i in range(1, len(players)):
            if players[i].points > maximum:
                maximum = players[i].points
                winners = [players[i]]
            elif maximum == players[i].points:
                winners.append(players[i])
        return winners

    def play(self):
        self.start()
        # First 7 rounds (starting at 7, 1 less card each round until 1 card per person)
        for i in range(7):
            r = Round(7 - i, self.playerList)  # Gets the round initialized
            print()
            r.bets()
            sleep(1)
            # One iteration for each trick
            for k in range(7 - i):
                self.updateDisplay(self.roundNumber, r.topCard.getSuit(), r.dealer)
                r.trick()
                sleep(1)
            # self.roundNumber += 1
            r.end()
            self.pointsDisplay(self.roundNumber, r.dealer)
            self.roundNumber += 1
        # Remaining 9 rounds (starting with 1 card, 1 more per round until 10)
        for i in range(9):
            r = Round(i + 2, self.playerList)  # Gets the round initialized
            r.bets()
            sleep(1)
            for k in range(i + 2):
                self.updateDisplay(self.roundNumber, r.topCard.getSuit(), r.dealer)
                r.trick()
                sleep(1)
            # self.roundNumber += 1
            r.end()
            self.pointsDisplay(self.roundNumber, r.dealer)
            self.roundNumber += 1
        self.endGame()

    def endGame(self):
        clear()
        playerWin = False
        winners = self.determineWinners(self.players)
        print("End of the Game")
        for player in self.players:
            print("%-10s - Points: %d" % (player.name, player.points))
        print("\nWinner is... ", end="")
        sleep(1)
        for i in range(len(winners)):
            if winners[i].isHuman:
                playerWin = True
            if i == len(winners) - 1:
                print("%s" % winners[i].name, end="")
            else:
                print("%s, " % winners[i].name, end="")
        print("\n")

        # Winsound only works if you're running windows
        if os.name == 'nt':
            if playerWin:
                winsound.PlaySound("cheers.wav", winsound.SND_ALIAS)
            else:
                winsound.PlaySound("sad_trombone.wav", winsound.SND_ALIAS)

        # The results of the game are recorded to a text file, including time/date, scores, and the winner for
        # concise record keeping.
        outfile = open("scores.txt", "a", encoding="utf8")
        dateTimeObj = datetime.now()
        morningNight = "a.m."
        hour = dateTimeObj.hour
        minute = dateTimeObj.minute
        if minute < 10:
            minute = "0" + str(minute)
        if dateTimeObj.hour == 0:
            hour = 12
        if dateTimeObj.hour >= 12:
            morningNight = "p.m."
            if dateTimeObj.hour > 12:
                hour -= 12
        # Printing to the file starts here
        print("%d-%d-%d, %d:%s %s" % (dateTimeObj.month, dateTimeObj.day, dateTimeObj.year,
                                      hour, minute, morningNight), file=outfile)
        for player in self.players:
            print("%-10s - Points: %d" % (player.name, player.points), file=outfile)
        print("Winner: ", end="", file=outfile)
        for i in range(len(winners)):
            if i == len(winners) - 1:
                print("%s" % winners[i].name, end="", file=outfile)
            else:
                print("%s, " % winners[i].name, end="", file=outfile)
        print("\n", file=outfile)

        # Asks the player if he/she wants to go again and restarts the game if yes
        sleep(1)
        yesPossible = ["Y", "YES"]
        possible = ["Y", "YES", "N", "NO"]
        stop = input("Play Again? (Y/N) ")
        if stop.isalpha():
            stop = stop.upper()
        while stop not in possible:
            stop = input("Please type Y (yes) or N (No). ")
            if stop.isalpha():
                stop = stop.upper()
        # If yes/y --> restart
        if stop in yesPossible:
            self.clearGame()
            self.play()

    # Resets the game (if the player decides to play again)
    def clearGame(self):
        self.roundNumber = 1
        self.cpu1 = Computer("CPU 1")
        self.cpu2 = Computer("CPU 2")
        self.cpu3 = Computer("CPU 3")
        self.human.points = 0
        self.players = [self.cpu1, self.cpu2, self.cpu3, self.human]
        self.playerList = [self.cpu1, self.cpu2, self.cpu3, self.human]


game1 = Game()
game1.play()
# game1.human.points = 50
# game1.cpu1.points = 50
# game1.endGame()
