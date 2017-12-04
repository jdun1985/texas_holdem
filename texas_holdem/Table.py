from texas_holdem.Deck import Deck
from texas_holdem.Player import Player
from texas_holdem.Card import Card

from texas_holdem.PokerHandParser import PokerHandParser

from random import choice
from collections import OrderedDict
from itertools import combinations

import sympy
import time
import multiprocessing
import os
from _operator import itemgetter
from enum import IntEnum

def partitionList(p_list, n):
    '''
    Return a list of lists partitioned into n lists
    partition([0, 1, 2, 3, 4, 5, 6, 7, 8], 4)
    returns: [[0, 1], [2, 3], [4, 5], [6, 7, 8]]
    '''
    ret = []
    assert (n > 0)
    l = len(p_list)
    assert (l > 0 and l >= n)
    p_size = len(p_list)//n
    ret.append(p_list[:p_size])
    for i in range(1, n - 1):
        ret.append(p_list[p_size*i:p_size*(i+1)])
    ret.append(p_list[p_size*(n-1):])
    return ret


    

'''
What has been will be again, what has been done will be done again; there is nothing new under the sun.
'''

'''Code conventions:

Using return None

This tells that the function is indeed meant to return a value for later use, and in this case it returns None.
This value None can then be used elsewhere. return None is never used if there are no other possible return values from the function.

Using return

This is used for the same reason as break in loops. The return value doesn't matter and you only want to exit the whole function.

Using no return at all

This will also return None, but that value is not meant to be used or caught. It simply means that the function ended successfully.
'''

'''
the size of the raise must be at least twice the size of the bet preceding it.
'''

class Table():
    MAX_PLAYERS = 10
    MIN_PLAYERS = 2
    PLAY_TIME_LIMIT = 180  # (Seconds) The player time limit to act.

    deck = Deck()

    def __init__(self, big_blind):
        
        self.players = OrderedDict()
        self.players_list = []
        
        self.dealer_name = None  # Name of the player who is the dealer_name
        self.dealer_index = None  # Index into players_list which indicates which player is the dealer_name
        self.small_blind_player = None  # Name of the player responsible for the small blind
        self.big_blind_player = None  # Name of the player responsible for the big blind
        self.action_player = None # Name of player that needs to perform an action
        self.split_players = [] # Contains the names of the blind players who couldn't meet the blind

        self.big_blind = None #big_blind
        self.small_blind = None #self.big_blind // 2  # As per WSOP, standard convention for setting the small blind is 1/2 the big blind.
        self.buy_in = None #20 * big_blind  # As per WSOP, standard convention for setting the buy in is 20 times the big blind.
        self.pot = None

        self.burn_pile = []
        self.community_cards = []        

        self.is_split_pot = False

        self.hand_index = None # Index of the current hand, i.e. The first hand of the game is 0, the second is 1 etc.
        
        self.setupGame(big_blind)
        
    def setupGame(self, big_blind):
        """Adds the players to the table, and determines the first dealer.
        
        TODO add file input, user input
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        
        self.big_blind = big_blind
        self.small_blind = self.big_blind // 2  # As per WSOP, standard convention for setting the small blind is 1/2 the big blind.
        self.buy_in = 20 * big_blind  # As per WSOP, standard convention for setting the buy in is 20 times the big blind.
        self.pot = 0
        
        self.hand_index = 0
        
        self.addPlayer(Player("John"))
        self.addPlayer(Player("Jim"))
        self.addPlayer(Player("Johan"))
        self.addPlayer(Player("Johna"))
        self.addPlayer(Player("Joanne"))
        self.addPlayer(Player("John James"))
        self.addPlayer(Player("Jojo"))
        self.addPlayer(Player("Jarvis"))
        self.addPlayer(Player("Juan"))
        self.addPlayer(Player("Jason"))
        
        self.printPlayers()
                
        self.setFirstDealer()
        
        self.printCurrentDealer()

    def dealPlayerCard(self, player):
        assert len(player.hole_cards) < 2
        assert len(player.hole_cards) >= 0
        
        player.hole_cards.append(Table.deck.dealCard())
        
    def dealCommunityCard(self):
        assert len(self.community_cards) < 5
        assert len(self.community_cards) >= 0
        
        self.community_cards.append(Table.deck.dealCard())
                
    def addPlayer(self, player):
        assert not (player.name in self.players)
        assert len(self.players) <= self.MAX_PLAYERS

        self.players[player.name] = player
        self.players_list = list(self.players)            
        self.players[player.name].stack = self.buy_in 

    def removePlayer(self, player):
        assert player.name in self.players
        assert len(self.players) >= 2
        
        self.players.pop(player.name)
        self.players_list = list(self.players)

    def printPlayers(self):
        for x in self.players:
            print("Player: " + self.players[x].name + ", Stack Size: " + str(self.players[x].stack))

    def setFirstDealer(self):
        assert len(self.players) >= 2
        assert len(self.players) <= 10
        self.dealer_name = choice(list(self.players))
        for i in range(0, len(self.players_list)):
            if self.players_list[i] == self.dealer_name:
                self.dealer_index = i
                
    def setNextDealer(self):
        assert len(self.players) >= 2
        assert len(self.players) <= 10
        self.dealer_index = (self.dealer_index + 1) % len(self.players_list)
        self.dealer_name = self.players_list[self.dealer_index]
        
    def printCurrentDealer(self):
        print("Current dealer_name is player: " + self.dealer_name)

    def determineBlindPlayers(self):
        assert not (self.dealer_name is None)
        assert len(self.players) >= 2

        if len(self.players_list) > 2:
            self.small_blind_player = self.players_list[(self.dealer_index + 1) % len(self.players_list)]
            self.big_blind_player = self.players_list[(self.dealer_index + 2)% len(self.players_list)]
        else:
            assert len(self.players_list) == 2
            self.small_blind_player = self.players_list[self.dealer_index]
            self.big_blind_player = self.players_list[self.dealer_index + 1]
    
    def printBlindPlayers(self):
        print('Small Blind player: %s, Big Blind player: %s' % (self.small_blind_player, self.big_blind_player)) 

    def setupHand(self):
        """Establishes blinds and makes sure responsible players post their blinds.
        
        Determines which players are responsible for the blinds.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        for p in self.players:
            #self.players[p].hand_index = self.hand_index
            self.players[p].setupHand(self.hand_index)

        self.pot = 0
        
        self.determineBlindPlayers()
        
        posted_small_blind = self.players[self.small_blind_player].postBlind(self.small_blind, 'small', self.hand_index)
        
        assert posted_small_blind <= self.small_blind
        assert posted_small_blind > 0
        
        if posted_small_blind < self.small_blind:
            self.split_players.append(self.small_blind_player)
            self.is_split_pot = True
            
        self.pot = self.pot + posted_small_blind
        
        posted_big_blind = self.players[self.big_blind_player].postBlind(self.big_blind, 'big', self.hand_index)
        
        assert posted_big_blind <= self.big_blind
        assert posted_big_blind > 0
        
        if posted_big_blind < self.big_blind:
            self.split_players.append(self.big_blind_player)
            self.is_split_pot = True
        
        self.pot = self.pot + posted_big_blind
        
    def printCurrentBets(self):
        for p in self.players_list:
            self.players[p].printBets()
        
    def dealHoleCards(self):
        ''' TODO research itertools cycle , maybe enumerate list which gives indexes? '''
        for i in range(2):
            for j in range(len(self.players_list)):
                self.dealPlayerCard(self.players[self.players_list[(j + self.dealer_index + 1) % len(self.players_list)]])
                self.players[self.players_list[(j + self.dealer_index + 1) % len(self.players_list)]].printHoleCards()

    def conductBettingRound(self):
        pass
    
    def startGame(self):
        done = False
            
        while not done:
            pass
            
def main():
    
    table = Table(50)
    
    table.determineBlindPlayers()
    
    table.printBlindPlayers()
    table.deck.printDeck()
    table.deck.shuffleDeck()
    
    table.dealHoleCards()
    
    table.setupHand()
    table.players[table.small_blind_player].printBets()
    table.players[table.big_blind_player].printBets()
    
    print(table.pot)
    




    
if __name__ == "__main__":
    main()
