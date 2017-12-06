import unittest

from texas_holdem.PokerHandParser import PokerHandParser
from texas_holdem.Deck import Deck
from texas_holdem.Card import Card

from itertools import combinations

'''
Poker Hand Probabilities from wikipedia -> "Poker Probability"
Hand     Distinct hands     Frequency     Probability     Cumulative probability     Odds     Mathematical expression of absolute frequency

Royal flush
10 of spades Jack of spades Queen of spades King of spades Ace of spades
    1     4     0.000154%     0.000154%     649,739 : 1     ( 4 1 ) {\displaystyle {4 \choose 1}} {4 \choose 1}

Straight flush (excluding royal flush)
4 of hearts 5 of hearts 6 of hearts 7 of hearts 8 of hearts
    9     36     0.00139%     0.0015%     72,192 : 1     ( 10 1 ) ( 4 1 ) − ( 4 1 ) {\displaystyle {10 \choose 1}{4 \choose 1}-{4 \choose 1}} {10 \choose 1}{4 \choose 1}-{4 \choose 1}

Four of a kind
Ace of hearts Ace of diamonds Ace of clubs Ace of spades 4 of diamonds
    156     624     0.0240%     0.0256%     4,164 : 1     ( 13 1 ) ( 12 1 ) ( 4 1 ) {\displaystyle {13 \choose 1}{12 \choose 1}{4 \choose 1}} {13 \choose 1}{12 \choose 1}{4 \choose 1}

Full house
8 of hearts 8 of diamonds 8 of clubs King of hearts King of spades
    156     3,744     0.1441%     0.17%     693 : 1     ( 13 1 ) ( 4 3 ) ( 12 1 ) ( 4 2 ) {\displaystyle {13 \choose 1}{4 \choose 3}{12 \choose 1}{4 \choose 2}} {13 \choose 1}{4 \choose 3}{12 \choose 1}{4 \choose 2}

Flush (excluding royal flush and straight flush)
10 of clubs 4 of clubs Queen of clubs 7 of clubs 2 of clubs
    1,277     5,108     0.1965%     0.367%     508 : 1     ( 13 5 ) ( 4 1 ) − ( 10 1 ) ( 4 1 ) {\displaystyle {13 \choose 5}{4 \choose 1}-{10 \choose 1}{4 \choose 1}} {13 \choose 5}{4 \choose 1}-{10 \choose 1}{4 \choose 1}

Straight (excluding royal flush and straight flush)
7 of clubs 8 of hearts 9 of diamonds 10 of hearts Jack of spades
    10     10,200     0.3925%     0.76%     254 : 1     ( 10 1 ) ( 4 1 ) 5 − ( 10 1 ) ( 4 1 ) {\displaystyle {10 \choose 1}{4 \choose 1}^{5}-{10 \choose 1}{4 \choose 1}} {10 \choose 1}{4 \choose 1}^{5}-{10 \choose 1}{4 \choose 1}

Three of a kind
Queen of hearts Queen of clubs Queen of diamonds 5 of spades Ace of diamonds
    858     54,912     2.1128%     2.87%     46.3 : 1     ( 13 1 ) ( 4 3 ) ( 12 2 ) ( 4 1 ) 2 {\displaystyle {13 \choose 1}{4 \choose 3}{12 \choose 2}{4 \choose 1}^{2}} {13 \choose 1}{4 \choose 3}{12 \choose 2}{4 \choose 1}^{2}

Two pair
3 of hearts 3 of diamonds 6 of clubs 6 of hearts King of spades
    858     123,552     4.7539%     7.62%     20.0 : 1     ( 13 2 ) ( 4 2 ) 2 ( 11 1 ) ( 4 1 ) {\displaystyle {13 \choose 2}{4 \choose 2}^{2}{11 \choose 1}{4 \choose 1}} {13 \choose 2}{4 \choose 2}^{2}{11 \choose 1}{4 \choose 1}

One pair
5 of hearts 5 of spades 2 of clubs Jack of clubs Ace of diamonds
    2,860     1,098,240     42.2569%     49.9%     1.37 : 1     ( 13 1 ) ( 4 2 ) ( 12 3 ) ( 4 1 ) 3 {\displaystyle {13 \choose 1}{4 \choose 2}{12 \choose 3}{4 \choose 1}^{3}} {13 \choose 1}{4 \choose 2}{12 \choose 3}{4 \choose 1}^{3}

No pair / High card
2 of diamonds 5 of spades 6 of spades Jack of hearts Ace of clubs
    1,277     1,302,540     50.1177%     100%     0.995 : 1     [ ( 13 5 ) − 10 ] [ ( 4 1 ) 5 − 4 ] {\displaystyle \left[{13 \choose 5}-10\right]\left[{4 \choose 1}^{5}-4\right]} \left[{13 \choose 5}-10\right]\left[{4 \choose 1}^{5}-4\right]

Total     7,462     2,598,960     100%     ---     0 : 1     ( 52 5 ) {\displaystyle {52 \choose 5}} {52 \choose 5}
'''

class Test(unittest.TestCase):
    '''The class variables below are:
    deck: This is a regular deck of 52 cards
    
    high, pair, ... , sflush: These are lists meant to contain
    every permutation of a given hand type.  These lists are constructed
    in the setUpClass() method.
    
    The class methods are:
    testPHPCompOpHighCard(), testPHPCompOpPair(), ... , testPHPCompOpSFlush():
    These test the comparison operators of the PokerHandParser class.
    They all follow the same methodology:
        Construct the highest raking hand, a middle ranking hand, and the lowest
        ranking hand of the given type.
        Test <, >, ==, and != operators against the hand types.
        
        Then they compare the high and low hand against all possible permutations
        of the given hand, and verify that the expected number of results.
     
    '''
    
    deck = Deck()
        
    high = []
    pair = []
    tpair = []
    three = []
    strt = []
    flush = []
    full = []
    four = []
    sflush = []
    
    count = 0

    @classmethod
    def setUpClass(cls):
        
        for combo in combinations(Test.deck, 5):
            
            Test.count += 1

            hand_id = PokerHandParser(combo).identity

            if hand_id[0]   == PokerHandParser.HIGH:
                Test.high.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.PAIR:
                Test.pair.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.TPAIR:
                Test.tpair.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.THREE:
                Test.three.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.STRT:
                Test.strt.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.FLUSH:
                Test.flush.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.FULL:
                Test.full.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.FOUR:
                Test.four.append(PokerHandParser(combo))
            elif hand_id[0] == PokerHandParser.SFLUSH:
                Test.sflush.append(PokerHandParser(combo))
            else:
                #We should NEVER get here
                assert False

    def testPHPCompOpHighCard(self):
        hand = []
    
        # High card
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 'c'))
        hand.append(Card('Q', 12, 'd'))
        hand.append(Card('J', 11, 's'))
        hand.append(Card('9', 9, 'h'))
        high_card_high = PokerHandParser(hand)
    
        high_card_high_0 = high_card_high
        
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('Q', 12, 's'))
        hand.append(Card('J', 11, 'h'))
        hand.append(Card('9', 9, 's'))
        high_card_high_1 = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('8', 8, 'h'))
        hand.append(Card('7', 7, 's'))
        hand.append(Card('6', 6, 'd'))
        hand.append(Card('5', 5, 'd'))
        hand.append(Card('3', 3, 'h'))
        high_card_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('2', 2, 's'))
        hand.append(Card('3', 3, 'h'))
        hand.append(Card('4', 4, 'd'))
        hand.append(Card('5', 5, 'c'))
        hand.append(Card('7', 7, 'd'))
        high_card_low = PokerHandParser(hand)
        
        print("High card high " + str(high_card_high.identity))
        print("High card 0 " + str(high_card_high_0.identity))
        print("High card high 1 " + str(high_card_high_1.identity))
        print("High card mid " + str(high_card_mid.identity))
        print("High card low " + str(high_card_low.identity))
        
        self.assertTrue(high_card_high == high_card_high_0 == high_card_high_1)
        self.assertTrue(high_card_high > high_card_mid > high_card_low)
        self.assertTrue(high_card_low < high_card_mid < high_card_high)
        self.assertTrue(high_card_high != high_card_mid != high_card_low)
        
        all_hands_gt_high_card_low = 0
        all_hands_eq_high_card_low = 0
        all_hands_lt_high_card_low = 0
        
        all_hands_gt_high_card_high = 0
        all_hands_eq_high_card_high = 0
        all_hands_lt_high_card_high = 0
        
        for i in Test.high:
            if(high_card_low > i):
                all_hands_lt_high_card_low += 1
            elif(high_card_low == i):
                all_hands_eq_high_card_low += 1
            elif(high_card_low < i):
                all_hands_gt_high_card_low += 1
            
            if(high_card_high > i):
                all_hands_lt_high_card_high += 1
            elif(high_card_high == i):
                all_hands_eq_high_card_high += 1
            elif(high_card_high < i):
                all_hands_gt_high_card_high += 1
        
        '''
        Frequecy: 1302540
        Distinct hands: 1277
        
        i.e. there are 1277 different types of High card hands,
        and there are 1302540 different High card hands.
        Therefore, there are 1302540//1277 = 1020 of each type of High card hand.        
        '''

        #There should be no hands less than the lowest high card hand
        self.assertTrue(all_hands_lt_high_card_low == 0)
        #There are 1302540//1277 = 1020 hands that are equal to the lowest high card hand
        self.assertTrue(all_hands_eq_high_card_low == 1302540//1277)
        #There should be 1302540 - 1020 hands that are greater than the lowest high card hand
        self.assertTrue(all_hands_gt_high_card_low == 1302540-(1302540//1277))
        
        self.assertTrue(all_hands_lt_high_card_high == 1302540-(1302540//1277))
        self.assertTrue(all_hands_eq_high_card_high == 1302540//1277)
        self.assertTrue(all_hands_gt_high_card_high == 0)
                
    def testPHPCompOpSFlush(self):
        
        # Straight Flush
        hand = []
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 'h'))
        hand.append(Card('Q', 12, 'h'))
        hand.append(Card('J', 11, 'h'))
        hand.append(Card('T', 10, 'h'))
        straight_flush_high = PokerHandParser(hand)
        
        straight_flush_high_0 = straight_flush_high
        
        hand.clear()
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('K', 13, 'c'))
        hand.append(Card('Q', 12, 'c'))
        hand.append(Card('J', 11, 'c'))
        hand.append(Card('T', 10, 'c'))
        straight_flush_high_1 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('9', 9, 's'))
        hand.append(Card('8', 8, 's'))
        hand.append(Card('7', 7, 's'))
        hand.append(Card('6', 6, 's'))
        hand.append(Card('5', 5, 's'))
        straight_flush_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('2', 2, 'h'))
        hand.append(Card('3', 3, 'h'))
        hand.append(Card('4', 4, 'h'))
        hand.append(Card('5', 5, 'h'))
        straight_flush_low = PokerHandParser(hand)
    
        print("Straight flush high " + str(straight_flush_high.identity))
        print("Straight flush high 0 " + str(straight_flush_high_0.identity))
        print("Straight flush high 1 " + str(straight_flush_high_1.identity))
        print("Straight flush mid " + str(straight_flush_mid.identity))
        print("Straight flush low " + str(straight_flush_low.identity))

        self.assertTrue(straight_flush_high == straight_flush_high_0 == straight_flush_high_1)
        self.assertTrue(straight_flush_high > straight_flush_mid > straight_flush_low)
        self.assertTrue(straight_flush_low < straight_flush_mid < straight_flush_high)
        self.assertTrue(straight_flush_low != straight_flush_mid != straight_flush_high)
        
        all_hands_gt_straight_flush_low = 0
        all_hands_eq_straight_flush_low = 0
        all_hands_lt_straight_flush_low = 0
        
        all_hands_gt_straight_flush_high = 0
        all_hands_eq_straight_flush_high = 0
        all_hands_lt_straight_flush_high = 0
        
        for i in Test.sflush:
            if(straight_flush_low > i):
                all_hands_lt_straight_flush_low += 1
            elif(straight_flush_low == i):
                all_hands_eq_straight_flush_low += 1
            elif(straight_flush_low < i):
                all_hands_gt_straight_flush_low += 1
            
            if(straight_flush_high > i):
                all_hands_lt_straight_flush_high += 1
            elif(straight_flush_high == i):
                all_hands_eq_straight_flush_high += 1
            elif(straight_flush_high < i):
                all_hands_gt_straight_flush_high += 1
        #10     40
        self.assertTrue(all_hands_lt_straight_flush_low == 0)
        self.assertTrue(all_hands_eq_straight_flush_low == 40//10)
        self.assertTrue(all_hands_gt_straight_flush_low == 40-(40//10))
        
        self.assertTrue(all_hands_lt_straight_flush_high == 40-(40//10))
        self.assertTrue(all_hands_eq_straight_flush_high == 40//10)
        self.assertTrue(all_hands_gt_straight_flush_high == 0)
                
    def testPHPCompOpFour(self):
        hand = []
        
        #Four of a kind
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 's'))
        four_high = PokerHandParser(hand)
    
        four_high_0 = four_high
        
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 'c'))
        four_high_1 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('8', 8, 's'))
        hand.append(Card('8', 8, 'c'))
        hand.append(Card('8', 8, 'd'))
        hand.append(Card('8', 8, 'c'))
        hand.append(Card('9', 9, 's'))
        four_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('8', 8, 's'))
        hand.append(Card('8', 8, 'c'))
        hand.append(Card('8', 8, 'd'))
        hand.append(Card('8', 8, 'c'))
        hand.append(Card('7', 7, 's'))
        four_mid_0 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('2', 2, 's'))
        hand.append(Card('2', 2, 'h'))
        hand.append(Card('2', 2, 'c'))
        hand.append(Card('2', 2, 'd'))
        hand.append(Card('3', 3, 'h'))
        four_low = PokerHandParser(hand)
    
        print("Four of a kind high " + str(four_high.identity))
        print("Four of a kind high 0 " + str(four_high_0.identity))
        print("Four of a kind high 1 " + str(four_high_1.identity))
        print("Four of a kind mid " + str(four_mid.identity))
        print("Four of a kind mid " + str(four_mid_0.identity))
        print("Four of a kind low " + str(four_low.identity))

        self.assertTrue(four_high == four_high_0 == four_high_1)
        self.assertTrue(four_high > four_mid > four_low)
        self.assertTrue(four_low < four_mid < four_high)
        self.assertTrue(four_high != four_mid != four_low)
        
        all_hands_gt_four_low = 0
        all_hands_eq_four_low = 0
        all_hands_lt_four_low = 0
        
        all_hands_gt_four_high = 0
        all_hands_eq_four_high = 0
        all_hands_lt_four_high = 0
        
        for i in Test.four:
            if(four_low > i):
                all_hands_lt_four_low += 1
            elif(four_low == i):
                all_hands_eq_four_low += 1
            elif(four_low < i):
                all_hands_gt_four_low += 1
            
            if(four_high > i):
                all_hands_lt_four_high += 1
            elif(four_high == i):
                all_hands_eq_four_high += 1
            elif(four_high < i):
                all_hands_gt_four_high += 1
        #156     624
        self.assertTrue(all_hands_lt_four_low == 0)
        self.assertTrue(all_hands_eq_four_low == 624//156)
        self.assertTrue(all_hands_gt_four_low == 624-(624//156))
        
        self.assertTrue(all_hands_lt_four_high == 624-(624//156))
        self.assertTrue(all_hands_eq_four_high == 624//156)
        self.assertTrue(all_hands_gt_four_high == 0)

    def testPHPCompOpFull(self):
        hand = []
        
        #Full house
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('K', 13, 'h'))
        hand.append(Card('K', 13, 's'))
        full_high = PokerHandParser(hand)
    
        full_high_0 = full_high
        
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 's'))
        hand.append(Card('K', 13, 'c'))
        full_high_1 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('8', 8, 's'))
        hand.append(Card('8', 8, 'c'))
        hand.append(Card('8', 8, 'd'))
        hand.append(Card('9', 9, 'c'))
        hand.append(Card('9', 9, 's'))
        full_mid = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('2', 2, 's'))
        hand.append(Card('2', 2, 'h'))
        hand.append(Card('2', 2, 'c'))
        hand.append(Card('3', 3, 'd'))
        hand.append(Card('3', 3, 'h'))
        full_low = PokerHandParser(hand)
    
        print("Full house high " + str(full_high.identity))
        print("Full house high 0 " + str(full_high_0.identity))
        print("Full house high 1 " + str(full_high_1.identity))
        print("Full house mid " + str(full_mid.identity))
        print("Full house low " + str(full_low.identity))
        
        self.assertTrue(full_high == full_high_0 == full_high_1)
        self.assertTrue(full_high > full_mid > full_low)
        self.assertTrue(full_low < full_mid < full_high)
        self.assertTrue(full_high != full_mid != full_low)
        
        all_hands_gt_full_low = 0
        all_hands_eq_full_low = 0
        all_hands_lt_full_low = 0
        
        all_hands_gt_full_high = 0
        all_hands_eq_full_high = 0
        all_hands_lt_full_high = 0
        
        for i in Test.full:
            if(full_low > i):
                all_hands_lt_full_low += 1
            elif(full_low == i):
                all_hands_eq_full_low += 1
            elif(full_low < i):
                all_hands_gt_full_low += 1
            
            if(full_high > i):
                all_hands_lt_full_high += 1
            elif(full_high == i):
                all_hands_eq_full_high += 1
            elif(full_high < i):
                all_hands_gt_full_high += 1
        #156     3744
        self.assertTrue(all_hands_lt_full_low == 0)
        self.assertTrue(all_hands_eq_full_low == 3744//156)
        self.assertTrue(all_hands_gt_full_low == 3744-(3744//156))
        
        self.assertTrue(all_hands_lt_full_high == 3744-(3744//156))
        self.assertTrue(all_hands_eq_full_high == 3744//156)
        self.assertTrue(all_hands_gt_full_high == 0)        
                
    def testPHPCompOpFlush(self):
        hand = []
        
        #Flush
        hand.clear()
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('Q', 12, 'd'))
        hand.append(Card('J', 11, 'd'))
        hand.append(Card('9',  9, 'd'))
        flush_high = PokerHandParser(hand)
        
        flush_high_0 = flush_high
        
        hand.clear()
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('K', 13, 'c'))
        hand.append(Card('Q', 12, 'c'))
        hand.append(Card('J', 11, 'c'))
        hand.append(Card('9',  9, 'c'))
        flush_high_1 = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('10', 10, 'd'))
        hand.append(Card('9', 9, 'd'))
        hand.append(Card('8', 8, 'd'))
        hand.append(Card('7', 7, 'd'))
        hand.append(Card('5', 5, 'd'))
        flush_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('2', 2, 's'))
        hand.append(Card('3', 3, 's'))
        hand.append(Card('4', 4, 's'))
        hand.append(Card('5', 5, 's'))
        hand.append(Card('7', 7, 's'))
        flush_low = PokerHandParser(hand)
    
        print("Flush high " + str(flush_high.identity))
        print("Flush high 0 " + str(flush_high_0.identity))
        print("Flush high 1 " + str(flush_high_1.identity))
        print("Flush mid " + str(flush_mid.identity))
        print("Flush low " + str(flush_low.identity))
        
        self.assertTrue(flush_high == flush_high_0 == flush_high_1)
        self.assertTrue(flush_high > flush_mid > flush_low)
        self.assertTrue(flush_low < flush_mid < flush_high)
        self.assertTrue(flush_high != flush_mid != flush_low)
        
        all_hands_gt_flush_low = 0
        all_hands_eq_flush_low = 0
        all_hands_lt_flush_low = 0
        
        all_hands_gt_flush_high = 0
        all_hands_eq_flush_high = 0
        all_hands_lt_flush_high = 0
        
        for i in Test.flush:
            if(flush_low > i):
                all_hands_lt_flush_low += 1
            elif(flush_low == i):
                all_hands_eq_flush_low += 1
            elif(flush_low < i):
                all_hands_gt_flush_low += 1
            
            if(flush_high > i):
                all_hands_lt_flush_high += 1
            elif(flush_high == i):
                all_hands_eq_flush_high += 1
            elif(flush_high < i):
                all_hands_gt_flush_high += 1
        #1277     5108
        self.assertTrue(all_hands_lt_flush_low == 0)
        self.assertTrue(all_hands_eq_flush_low == 5108//1277)
        self.assertTrue(all_hands_gt_flush_low == 5108-(5108//1277))
        
        self.assertTrue(all_hands_lt_flush_high == 5108-(5108//1277))
        self.assertTrue(all_hands_eq_flush_high == 5108//1277)
        self.assertTrue(all_hands_gt_flush_high == 0)        

                
    def testPHPCompOpStraight(self):
        hand = []
        
        # Straight
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 'c'))
        hand.append(Card('Q', 12, 'd'))
        hand.append(Card('J', 11, 's'))
        hand.append(Card('T', 10, 'h'))
        straight_high = PokerHandParser(hand)
        
        straight_high_0 = straight_high
        
        hand.clear()
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('Q', 12, 'd'))
        hand.append(Card('J', 11, 's'))
        hand.append(Card('T', 10, 'h'))
        straight_high_1 = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('J', 11, 's'))
        hand.append(Card('T', 10, 'c'))
        hand.append(Card('9',  9, 's'))
        hand.append(Card('8',  8, 's'))
        hand.append(Card('7',  7, 'h'))
        straight_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('2',  2, 'c'))
        hand.append(Card('3',  3, 'c'))
        hand.append(Card('4',  4, 's'))
        hand.append(Card('5',  5, 'c'))
        straight_low = PokerHandParser(hand)
        
        print("Straight high " + str(straight_high.identity))
        print("Straight high 0 " + str(straight_high_0.identity))
        print("Straight high 1 " + str(straight_high_1.identity))
        print("Straight mid " + str(straight_mid.identity))
        print("Straight low " + str(straight_low.identity))
        
        self.assertTrue(straight_high == straight_high_0 == straight_high_1)
        self.assertTrue(straight_high > straight_mid > straight_low)
        self.assertTrue(straight_low < straight_mid < straight_high)
        self.assertTrue(straight_high != straight_mid != straight_low)
        
        all_hands_gt_straight_low = 0
        all_hands_eq_straight_low = 0
        all_hands_lt_straight_low = 0
        
        all_hands_gt_straight_high = 0
        all_hands_eq_straight_high = 0
        all_hands_lt_straight_high = 0
        
        for i in Test.strt:
            if(straight_low > i):
                all_hands_lt_straight_low += 1
            elif(straight_low == i):
                all_hands_eq_straight_low += 1
            elif(straight_low < i):
                all_hands_gt_straight_low += 1
            
            if(straight_high > i):
                all_hands_lt_straight_high += 1
            elif(straight_high == i):
                all_hands_eq_straight_high += 1
            elif(straight_high < i):
                all_hands_gt_straight_high += 1
        #10     10,200
        self.assertTrue(all_hands_lt_straight_low == 0)
        self.assertTrue(all_hands_eq_straight_low == 10200//10)
        self.assertTrue(all_hands_gt_straight_low == 10200-(10200//10))
        
        self.assertTrue(all_hands_lt_straight_high == 10200-(10200//10))
        self.assertTrue(all_hands_eq_straight_high == 10200//10)
        self.assertTrue(all_hands_gt_straight_high == 0)        


    def testPHPCompOpThree(self):
        # Three of a kind
        hand = []
        
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('K', 13, 's'))
        hand.append(Card('Q', 12, 'h'))
        three_high = PokerHandParser(hand)
    
        three_high_0 = three_high
    
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('A', 14, 'd'))
        hand.append(Card('Q', 12, 's'))
        hand.append(Card('K', 13, 'h'))
        three_high_1 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('9', 9, 'h'))
        hand.append(Card('9', 9, 'c'))
        hand.append(Card('9', 9, 'd'))
        hand.append(Card('5', 5, 's'))
        hand.append(Card('11', 11, 'h'))
        three_mid = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('2', 2, 'h'))
        hand.append(Card('2', 2, 'c'))
        hand.append(Card('2', 2, 'd'))
        hand.append(Card('3', 3, 's'))
        hand.append(Card('4', 4, 'h'))
        three_low = PokerHandParser(hand)
        
        print("Three of a kind high " + str(three_high.identity))
        print("Three of a kind high 0 " + str(three_high_0.identity))
        print("Three of a kind high 1 " + str(three_high_1.identity))
        print("Three of a kind mid " + str(three_mid.identity))
        print("Three of a kind low " + str(three_low.identity))
    
        self.assertTrue(three_high == three_high_0 == three_high_1)
        self.assertTrue(three_high > three_mid > three_low)
        self.assertTrue(three_low < three_mid < three_high)
        self.assertTrue(three_high != three_mid != three_low)
        
        all_hands_gt_three_low = 0
        all_hands_eq_three_low = 0
        all_hands_lt_three_low = 0
        
        all_hands_gt_three_high = 0
        all_hands_eq_three_high = 0
        all_hands_lt_three_high = 0
        
        for i in Test.three:
            if(three_low > i):
                all_hands_lt_three_low += 1
            elif(three_low == i):
                all_hands_eq_three_low += 1
            elif(three_low < i):
                all_hands_gt_three_low += 1
            
            if(three_high > i):
                all_hands_lt_three_high += 1
            elif(three_high == i):
                all_hands_eq_three_high += 1
            elif(three_high < i):
                all_hands_gt_three_high += 1
        #858     54912
        self.assertTrue(all_hands_lt_three_low == 0)
        self.assertTrue(all_hands_eq_three_low == 54912//858)
        self.assertTrue(all_hands_gt_three_low == 54912-(54912//858))
        
        self.assertTrue(all_hands_lt_three_high == 54912-(54912//858))
        self.assertTrue(all_hands_eq_three_high == 54912//858)
        self.assertTrue(all_hands_gt_three_high == 0)        

                
    def testPHPCompOpTPair(self):
        # Two pair
        hand = []
        
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('K', 13, 's'))
        hand.append(Card('Q', 12, 'h'))
        tpair_high = PokerHandParser(hand)
        
        tpair_high_0 = tpair_high
        
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('K', 13, 'h'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('Q', 12, 'h'))
        tpair_high_1 = PokerHandParser(hand)
    
        hand.clear()
        hand.append(Card('8', 8, 's'))
        hand.append(Card('8', 8, 'h'))
        hand.append(Card('5', 5, 's'))
        hand.append(Card('5', 5, 'd'))
        hand.append(Card('7', 7, 'c'))
        tpair_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('3', 3, 'c'))
        hand.append(Card('3', 3, 'h'))
        hand.append(Card('2', 2, 's'))
        hand.append(Card('2', 2, 'c'))
        hand.append(Card('4', 4, 'h'))
        tpair_low = PokerHandParser(hand)
        
        print("Two pair high " + str(tpair_high.identity))
        print("Two pair 0 " + str(tpair_high_0.identity))
        print("Two pair high 1 " + str(tpair_high_1.identity))
        print("Two pair mid " + str(tpair_mid.identity))
        print("Two pair low " + str(tpair_low.identity))
        
        self.assertTrue(tpair_high == tpair_high_0 == tpair_high_1)
        self.assertTrue(tpair_high > tpair_mid > tpair_low)
        self.assertTrue(tpair_low < tpair_mid < tpair_high)
        self.assertTrue(tpair_low != tpair_mid != tpair_high)
        
        all_hands_gt_tpair_low = 0
        all_hands_eq_tpair_low = 0
        all_hands_lt_tpair_low = 0
        
        all_hands_gt_tpair_high = 0
        all_hands_eq_tpair_high = 0
        all_hands_lt_tpair_high = 0
        
        for i in Test.tpair:
            if(tpair_low > i):
                all_hands_lt_tpair_low += 1
            elif(tpair_low == i):
                all_hands_eq_tpair_low += 1
            elif(tpair_low < i):
                all_hands_gt_tpair_low += 1
            
            if(tpair_high > i):
                all_hands_lt_tpair_high += 1
            elif(tpair_high == i):
                all_hands_eq_tpair_high += 1
            elif(tpair_high < i):
                all_hands_gt_tpair_high += 1

        #858     123552
        self.assertTrue(all_hands_lt_tpair_low == 0)
        self.assertTrue(all_hands_eq_tpair_low == 123552//858)
        self.assertTrue(all_hands_gt_tpair_low == 123552-(123552//858))
        
        self.assertTrue(all_hands_lt_tpair_high == 123552-(123552//858))
        self.assertTrue(all_hands_eq_tpair_high == 123552//858)
        self.assertTrue(all_hands_gt_tpair_high == 0)        
                
    def testPHPCompOpPair(self):
        hand = []
        
        # Pair
        hand.clear()
        hand.append(Card('A', 14, 'h'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('K', 13, 'd'))
        hand.append(Card('Q', 12, 's'))
        hand.append(Card('J', 11, 'h'))
        pair_high = PokerHandParser(hand)
        
        pair_high_0 = pair_high
        
        hand.clear()
        hand.append(Card('A', 14, 's'))
        hand.append(Card('A', 14, 'c'))
        hand.append(Card('K', 13, 'c'))
        hand.append(Card('Q', 12, 'd'))
        hand.append(Card('J', 11, 'h'))
        pair_high_1 = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('9', 9, 'c'))
        hand.append(Card('9', 9, 'd'))
        hand.append(Card('J', 11, 'd'))
        hand.append(Card('T', 10, 'd'))
        hand.append(Card('6', 6, 'c'))
        pair_mid = PokerHandParser(hand)
        
        hand.clear()
        hand.append(Card('2', 2, 'h'))
        hand.append(Card('2', 2, 's'))
        hand.append(Card('3', 3, 'd'))
        hand.append(Card('4', 4, ''))
        hand.append(Card('5', 5, 'h'))
        pair_low = PokerHandParser(hand)
        
        print("Pair high " + str(pair_high.identity))
        print("Pair 0 " + str(pair_high_0.identity))
        print("Pair high 1 " + str(pair_high_1.identity))
        print("Pair mid " + str(pair_mid.identity))
        print("Pair low " + str(pair_low.identity))
        
        self.assertTrue(pair_high == pair_high_0 == pair_high_1)
        self.assertTrue(pair_high > pair_mid > pair_low)
        self.assertTrue(pair_low < pair_mid < pair_high)
        self.assertTrue(pair_high != pair_mid != pair_low)
        
        all_hands_gt_pair_low = 0
        all_hands_eq_pair_low = 0
        all_hands_lt_pair_low = 0
        
        all_hands_gt_pair_high = 0
        all_hands_eq_pair_high = 0
        all_hands_lt_pair_high = 0
        
        for i in Test.pair:
            if(pair_low > i):
                all_hands_lt_pair_low += 1
            elif(pair_low == i):
                all_hands_eq_pair_low += 1
            elif(pair_low < i):
                all_hands_gt_pair_low += 1
            
            if(pair_high > i):
                all_hands_lt_pair_high += 1
            elif(pair_high == i):
                all_hands_eq_pair_high += 1
            elif(pair_high < i):
                all_hands_gt_pair_high += 1
        # Distinct: 2,860    Frequency: 1,098,240
        self.assertTrue(all_hands_lt_pair_low == 0)
        self.assertTrue(all_hands_eq_pair_low == 1098240//2860)
        self.assertTrue(all_hands_gt_pair_low == 1098240-(1098240//2860))
        
        self.assertTrue(all_hands_lt_pair_high == 1098240-(1098240//2860))
        self.assertTrue(all_hands_eq_pair_high == 1098240//2860)
        self.assertTrue(all_hands_gt_pair_high == 0)        
    
    def testPokerHandParserIdentity(self):
        self.assertEqual(Test.count, 2598960, "More hands than expected.")
        self.assertEqual(len(Test.high), 1302540, "High card.")
        self.assertEqual(len(Test.pair), 1098240, "Pair.")
        self.assertEqual(len(Test.tpair), 123552, "Two pair.")
        self.assertEqual(len(Test.three), 54912, "Three of a kind.")
        self.assertEqual(len(Test.strt), 10200, "Straight.")
        self.assertEqual(len(Test.flush), 5108, "Flush.")
        self.assertEqual(len(Test.full), 3744, "Full house.")
        self.assertEqual(len(Test.four), 624, "Four of a kind.")
        self.assertEqual(len(Test.sflush), 40, "Straight flush.")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()