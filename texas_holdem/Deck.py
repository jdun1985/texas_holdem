from texas_holdem.Card import Card
from random import shuffle

class Deck():
    suits = ['h', 'd', 'c', 's']
    faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    
    def __init__(self):
        self.deck = []
        for suit in Deck.suits:
            for i in range(len(Deck.faces)):
                self.deck.append(Card(self.faces[i], self.ranks[i], suit))

    def __iter__(self):
        return iter(self.deck)
    
    def __next__(self):
        self.it.__next__()
      
    def shuffleDeck(self):
        shuffle(self.deck)
        
    def dealCard(self):
        return self.deck.pop()
    
    def printDeck(self):
        for card in self.deck:
            card.printCard()
        print()