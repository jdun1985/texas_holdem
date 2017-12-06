'''
Straight Flush  40     one in 64,974
Four of a Kind         624     one in 4165
Full House         3,744     one in 694
Flush         5,108     one in 509
Straight         10,200     one in 255
Three of a Kind         54,912     one in 47
Two Pairs         123,552     one in 21
One Pair         1,098,240     one in 2.36
Only Singles         1,302,540     one in 2
trivial file change to be removed TODO: remove this line
'''

class PokerHandParser():
    
    '''The below class globals are not a bad decision, I tried enum and various different methods
    to define these 'types', but enums DOUBLED the computation time for comparisons, and other
    methods did not allow the range of comparison operators needed.
    '''
    HIGH    = 0
    PAIR    = 1
    TPAIR   = 2
    THREE   = 3
    STRT    = 4
    FLUSH   = 5
    FULL    = 6
    FOUR    = 7
    SFLUSH  = 8

    def __init__(self, hand):
        assert len(hand) == 5
        
        self.community = True   #TODO exclude any comparisons between hands with identical cards if it is not a community game
        
        self.hand = hand
        
        self.identity = None
        
        self.is_sflush = None
        self.is_four = None
        self.is_full = None
        self.is_flush = None
        self.is_straight = None
        self.is_three = None
        self.is_two_pair = None
        self.is_pair = None
        self.is_high = None        
        
        self.rank_l = [hand[0].rank, hand[1].rank, hand[2].rank, hand[3].rank, hand[4].rank]
        self.rank_l.sort(key=None, reverse=False)

        self.rank_s = {hand[0].rank, hand[1].rank, hand[2].rank, hand[3].rank, hand[4].rank}
        self.suit_s = {hand[0].suit, hand[1].suit, hand[2].suit, hand[3].suit, hand[4].suit}

        self.identity = self.identify()
    '''
        Ranking    Rank-card(s)    Kicker-card(s)    Tie Breakers
    ROYAL FLUSH     Royal Flush Cards     NA     A Royal Flush is the highest hand in poker. Between two Royal flushes,
     there can be no tie breaker. If two players have Royal Flushes, they split the pot. The odds of this happening
      though are very less unless the Royal card lands on the table (community cards) in a game of Texas Holdem.
    STRAIGHT FLUSH     Top Card     NA     Straight flushes come in varying strengths from five high to a king high.
     A King High Straight Flush loses only to a Royal. If more than one player has a Straight Flush, the winner is
      the player with the highest card used in the Straight. A queen high Straight Flush beats a jack high and a 
      jack high beats a ten high and so on. The suit never comes into play i.e. a seven High Straight Flush of
       Diamonds will split the pot with a seven high Straight Flush of hearts.
    FOUR OF A KIND     Four of a Kind Card     Remaining 1     This one is simple. Four Aces beats any other four 
    of a kind, four Kings beats four queens or less and so on. The only tricky part of a tie breaker with four of
     a kind is when the four falls on the table in a game of Texas Holdem and is therefore shared between two (or more) players. A kicker can be used, however if the fifth community card is higher than any card held by any player still in the hand, then the hand is considered a tie and the pot is split.
    FULL HOUSE     Trips & Pair Card     NA     When two or more players have full houses, we look first at the
     strength of the three of a kind to determine the winner. For example, Aces full of deuces (AAA22) beats Kings
      full of Jacks (KKKJJ). If there are three of a kind on the table (community cards) in a Texas Holdem game 
      that are used by two or more players to make a full house, then we would look at the strength of the pair to determine a winner.
    FLUSH     Flush Cards     NA     A flush is any hand with five cards of the same suit. If two or more players
     hold a flush, the flush with the highest card wins. If more than one player has the same strength high card,
      then the strength of the second highest card held wins. This continues through the five highest cards in the
       player's hands.
    STRAIGHT     Top Card     NA     A straight is any five cards in sequence, but not necessarily of the same suit.
     If more than one player has a straight, the straight ending in the card wins. If both straights end in a card
     of the same strength, the hand is tied.
    THREE OF A KIND     Trips Card     Remaining 2     If more than one player holds three of a kind, then the higher
     value of the cards used to make the three of kind determines the winner. If two or more players have the same
      three of a kind, then a fourth card (and a fifth if necessary) can be used as kickers to determine the winner.
    TWO PAIR     1st & 2nd Pair Card     Remaining 1     The highest pair is used to determine the winner. If two or
     more players have the same highest pair, then the highest of the second pair determines the winner. If both players
      hold identical two pairs, fifth card is used to break the tie.
    ONE PAIR     Pair Card     Remaining 3     If two or more players hold a single pair, then highest pair wins. If
     the pairs are of the same value, the highest kicker card determines the winner. A second and even third kicker
      can be used if necessary.
    HIGH CARD     Top Card     Remaining 4     The highest card wins. When both
     players have identical high cards, the next highest card wins, and so on until five cards have been used. In
      the unusual circumstance that two players hold the identical five cards, the pot would be split.
    '''
    def __eq__(self, other):
        if isinstance(other, PokerHandParser):
            return self.identity == other.identity
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, PokerHandParser):
            return self.identity != other.identity
        return NotImplemented
  
    def __lt__(self, other):
        if isinstance(other, PokerHandParser):
            if self.identity[0] != other.identity[0]:
                return self.identity[0] < other.identity[0]
            else:
                if self.identity[0] == PokerHandParser.HIGH: ####
                    '''List of the 5 card hand sorted from lowest to highest
                    '''
                    #[0, [2, 3, 4, 5, 8]], [0, [3, 4, 5, 6, 8]]
                    for i in range(4, -1, -1):
                        if self.identity[1][i] < other.identity[1][i]:
                            return True
                        elif self.identity[1][i] == other.identity[1][i]:
                            continue
                        else:
                            return False
                    #if we got here, all of the elements were ==
                    return False
                    
                if self.identity[0] == PokerHandParser.PAIR: ####
                    '''The first element indicates the rank of the pair.
                    The 2nd, 3rd, and 4th element are the remaining cards from lowest to highest.
                    '''
                    #[1, [3, 4, 5, 6]] [1, [3, 2, 5, 6]]
                    if self.identity[1][0] < other.identity[1][0]:
                        return True
                    elif self.identity[1][0] == other.identity[1][0]:
                        for i in range(3, 0, -1):
                            if self.identity[1][i] < other.identity[1][i]:
                                return True
                            elif self.identity[1][i] == other.identity[1][i]:
                                continue
                            else:
                                return False
                        return False
                
                if self.identity[0] == PokerHandParser.TPAIR: ####
                    '''The first element indicates the rank of the lowest pair,
                    The second element indicates the rank of the highest pair.
                    The third element indicates the rank of the remaining card.
                    '''
                    #lowest highest remaining [2, [3, 4, 2]] [2, [3, 4, 5]]
                    for i in range(1, -1, -1):
                        if self.identity[1][i] < other.identity[1][i]:
                            return True
                        elif self.identity[1][i] == other.identity[1][i]:
                            continue
                        else:
                            return False
                    return self.identity[1][2] < other.identity[1][2]

                if self.identity[0] == PokerHandParser.THREE: ####
                    '''The first element indicates the rank of the triplet,
                    The second element indicates the rank of the lower of the non-triplet cards.
                    The third element indicates the rank of the higher of the other two cards.
                    '''
                    
                    # triplet lower higher [3, [3, 4, 8]] [3, [3, 2, 8]]
                    if self.identity[1][0] < other.identity[1][0]:
                        return True
                    
                    #if we got here self.identity[1][0] is >= other
                    elif self.identity[1][0] == other.identity[1][0]:#self.identity[1][0] == other
                        for i in range(2, 0, -1):
                            
                            if self.identity[1][i] < other.identity[1][i]:
                                # it is < the other
                                return True
                            # it is >= to the other
                            elif self.identity[1][i] == other.identity[1][i]:
                                # it is == other 
                                continue
                            # it is > the other
                            else:
                                return False
                        return False
                    else:#self.identity[1][0] > other
                        return False

                if self.identity[0] == PokerHandParser.STRT: ####
                    # [4, 6]
                    return self.identity[1] < other.identity[1]
                
                if self.identity[0] == PokerHandParser.FLUSH: ####
                    '''An ascending list containing the card ranks.
                    [5, 7, 8, 9, 10] [4, 7, 8, 9, 10]
                    '''
                    for i in range(4, -1, -1):
                        if self.identity[1][i] < other.identity[1][i]:
                            return True
                        elif self.identity[1][i] == other.identity[1][i]:
                            continue
                        else:
                            return False
                    return False

                if self.identity[0] == PokerHandParser.FULL: ####
                    '''The first element indicates the rank of the triplet,
                    The second element indicates the rank of the pair.
                    [6, [14, 8]] [6, [14, 7]]
                    '''
                    #triplet pair
                    if self.identity[1][0] < other.identity[1][0]:
                        return True
                    elif self.identity[1][0] == other.identity[1][0]:
                        return self.identity[1][1] < other.identity[1][1]
                    else:
                        return False
                    
                if self.identity[0] == PokerHandParser.FOUR: ####
                    '''The first element indicates the rank of the Four of a kind,
                    The second element indicates the rank of the kicker.
                    [7, [14, 13]]
                    '''
                    #four kicker
                    if self.identity[1][0] < other.identity[1][0]:
                        return True
                    elif self.identity[1][0] == other.identity[1][0]:
                        return self.identity[1][1] < other.identity[1][1]
                    else:
                        return False
                    
                if self.identity[0] == PokerHandParser.SFLUSH: ####
                    '''The first element is an integer indicating the rank of the high card.
                    '''
                    return self.identity[1] < other.identity[1]    
        else:
            return NotImplemented

    def identify(self): 
        
        if not (self.identity is None):
            return self.identity
                           
        if self.isHigh()[0] == True:
            return [PokerHandParser.HIGH, self.isHigh()[1]]
        
        if self.isPair()[0] == True:
            return [PokerHandParser.PAIR, self.isPair()[1]]
        
        if self.isTwoPair()[0] == True:
            return [PokerHandParser.TPAIR, self.isTwoPair()[1]]

        if self.isThree()[0] == True:
            return [PokerHandParser.THREE, self.isThree()[1]]

        if self.isStraight()[0] == True:
            return [PokerHandParser.STRT, self.isStraight()[1]]

        if self.isFlush()[0] == True:
            return [PokerHandParser.FLUSH, self.isFlush()[1]]

        if self.isFull()[0] == True:
            return [PokerHandParser.FULL, self.isFull()[1]]

        if self.isFour()[0] == True:
            return [PokerHandParser.FOUR, self.isFour()[1]]
        
        if self.isSFlush()[0] == True:
            return [PokerHandParser.SFLUSH, self.isSFlush()[1]]

        assert False
    
    def isSFlush(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Straight Flush.
            If the first element is True, the second element is an integer indicating the rank of the high card.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.suit_s is initialized with all 5 cards in the hand.
            self.rank_s is initialized with all 5 cards in the hand.
        '''        
        ret = None
        
        if not (self.is_sflush is None):
            ret = self.is_sflush
        
        elif len(self.suit_s) != 1:
            ret = (False, None)
        #There is only one suit
        elif 14 in self.rank_s:
            #There is an Ace in the hand, need to check high/low
            if (self.rank_l[0] == 10 and self.rank_l[1] == 11 and self.rank_l[2] == 12 and self.rank_l[3] == 13):
                ret = (True, 14)
            elif (self.rank_l[0] == 2 and self.rank_l[1] == 3 and self.rank_l[2] == 4 and self.rank_l[3] == 5):
                ret = (True, 5)
            else:
                ret = (False, None)
        else:
            #There is NOT an Ace in the hand, check for a clean straight.
            sr = self.rank_l[0]
            strait = self.rank_l[1] == sr+1 and self.rank_l[2] == sr+2 and self.rank_l[3] == sr+3 and self.rank_l[4] == sr+4
            if strait:
                ret = (True, self.rank_l[4])
            else:
                ret = (False, None)
        assert not (ret is None)
        self.is_sflush = ret
        return ret
            
    def isFour(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Four of a kind.
            If the first element is True, the second element is a two element list: 
                The first element indicates the rank of the Four of a kind,
                The second element indicates the rank of the kicker.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        ret = None
        
        if not (self.is_four is None):
            return self.is_four
        
        elif len(self.rank_s) != 2:
            ret = (False, None)
        else:
            rc1 = self.rank_l.count(self.rank_l[0])
            if(rc1 == 4 or rc1 == 1):
                ret = (True, [self.rank_l[0] if rc1 == 4 else self.rank_l[4], self.rank_l[0] if rc1 != 4 else self.rank_l[4]])
            else:
                ret = (False, None)
        assert not (ret is None)
        self.is_four = ret
        return ret
            
    def isFull(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Full House.
            If the first element is True, the second element is a two element list: 
                The first element indicates the rank of the triplet,
                The second element indicates the rank of the pair.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        ret = None
        
        if not (self.is_full is None):
            ret = self.is_full
            
        elif len(self.rank_s) != 2:
            ret = (False, None)
        else:
            rc1 = self.rank_l.count(self.rank_l[0])
            if(rc1 == 3):
                ret = (True, [self.rank_l[0], self.rank_l[4]])
            elif(rc1 == 2):
                ret = (True, [self.rank_l[4], self.rank_l[0]])
            else:
                ret = (False, None)
        assert not (ret is None)
        self.is_full = ret
        return ret
                           
    def isFlush(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Flush.
            If the first element is True, the second element is an ascending list containing the card ranks.
            If the first element is False, the second element contains None.
            
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.suit_s is initialized with all 5 cards in the hand.
       '''
        ret = None
        
        if not (self.is_flush is None):
            ret = self.is_flush
        
        elif len(self.suit_s) != 1:
            #There is more than one suit, or it is a Straight Flush
            ret = (False, None)
        elif self.isSFlush()[0]:
            ret = (False, None)
        else:
            ret = (len(self.suit_s) == 1, self.rank_l if len(self.suit_s) == 1 else None)
        assert not (ret is None)
        self.is_flush = ret
        return ret

    def isStraight(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Straight.
            If the first element is True, the second element is an integer indicating the rank of the high card.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        '''TODO optimize with sum of differences
        10 11 12 13 14 = 4
        '''
        ret = None
        
        if not (self.is_straight is None):
            ret = self.is_straight
        
        elif len(self.rank_s) < 5 or self.isSFlush()[0]:
            #There are less than 5 ranks, or it is a Straight Flush
            ret = (False, None)

        elif 14 in self.rank_s:
            #There is an Ace in the hand, need to check high/low
            if (self.rank_l[0] == 10 and self.rank_l[1] == 11 and self.rank_l[2] == 12 and self.rank_l[3] == 13):
                ret = (True, 14)
            elif (self.rank_l[0] == 2 and self.rank_l[1] == 3 and self.rank_l[2] == 4 and self.rank_l[3] == 5):
                ret = (True, 5)
            else:
                ret = (False, None)
        else:
            #There is NOT an Ace in the hand, check for a clean straight.
            sr = self.rank_l[0]
            strait = self.rank_l[1] == sr+1 and self.rank_l[2] == sr+2 and self.rank_l[3] == sr+3 and self.rank_l[4] == sr+4
            
            if strait:
                ret = (True, self.rank_l[4])
            else:
                ret = (False, None)
        assert not (ret is None)
        self.is_straight = ret
        return ret
                
    def isThree(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Three of a kind.
            If the first element is True, the second element is a three element list: 
                The first element indicates the rank of the triplet,
                The second element indicates the rank of the lower of the non-triplet cards.
                The third element indicates the rank of the higher of the other two cards.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        ret = None
        
        if not (self.is_three is None):
            ret = self.is_three
            
        elif len(self.rank_s) != 3:
            ret = (False, None)
        else:
            # possible rank_l permutations: 22234 23334 23444 22334 22344 23344
            triplet = False
            #triplet_rank = None
            #triplet_removed = []
            for r in self.rank_s:
                if self.rank_l.count(r) == 3:
                    ret = (True, [r] + [y for y in self.rank_l if y != r])
                    triplet = True
                    break
            if not triplet:
                ret = (False, None)
        assert not (ret is None)
        self.is_three = ret
        return ret

    def isTwoPair(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Two pair.
            If the first element is True, the second element is a three element list: 
                The first element indicates the rank of the lowest pair,
                The second element indicates the rank of the highest pair.
                The third element indicates the rank of the remaining card.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.        
        '''
        ret = None
        
        if not (self.is_two_pair is None):
            ret = self.is_two_pair
            
        elif len(self.rank_s) != 3:
            ret = (False, None)
        else:
            '''possible rank_l permutations: 22234 23334 23444 22334 22344 23344 '''
            triplet = False
            for r in self.rank_s:
                if self.rank_l.count(r) == 3:
                    triplet = True
                    break
            if not triplet: 
                ''' 22334 22344 23344 '''
                if self.rank_l.count(self.rank_l[0]) == 1: 
                    ''' 23344 '''
                    ret = (True, [self.rank_l[1], self.rank_l[3], self.rank_l[0]])
                elif self.rank_l.count(self.rank_l[2]) == 1: 
                    ''' 22344 '''
                    ret = (True, [self.rank_l[0], self.rank_l[3], self.rank_l[2]])
                else: 
                    ''' 22334 '''
                    ret = (True, [self.rank_l[0], self.rank_l[2], self.rank_l[4]])
            else:
                ''' There is a triplet '''
                ret = (False, None)
        assert not (ret is None)
        self.is_two_pair = ret
        return ret
    
    def isPair(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a Pair.
            If the first element is True, the second element is a four element list: 
                The first element indicates the rank of the pair.
                The 2nd, 3rd, and 4th element are the remaining cards from lowest to highest.
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        ret = None
        
        if not (self.is_pair is None):
            ret = self.is_pair
            
        elif len(self.rank_s) != 4:
            ret = (False, None)
        else:
            '''possible rank_l permutations: 12344 12334 12234 11234 '''
            double = False
            #double_rank = None
            for r in self.rank_s:
                if self.rank_l.count(r) == 2:
                    ret = (True, [r] + [y for y in self.rank_l if y != r])
                    double = True
                    break
            if not double:
                ret = (False, None)
        assert not (ret is None)
        self.is_pair = ret
        return ret
    
    def isHigh(self):
        '''Returns a two tuple:
        The first element is boolean, indicating whether or not the hand is a High Card hand.
            If the first element is True, the second element is a list of the 5 card hand
                sorted from lowest to highest
            If the first element is False, the second element contains None.
        Assumes:
            self.rank_l is initialized with all 5 cards in the hand, and is sorted in ascending order.
            self.rank_s is initialized with all 5 cards in the hand.
        '''
        ret = None
        
        if not (self.is_high is None):
            ret = self.is_high
            
        elif len(self.rank_s) != 5:
            ret = (False, None)
        elif len(self.suit_s) == 1:
            ret = (False, None)
        #TODO remove below isFlush()
        elif self.isFlush()[0]:
            ret = (False, None)
        elif self.isStraight()[0]:
            ret = (False, None)
        elif self.isSFlush()[0]:
            ret = (False, None)
        else:
            ret = (True, self.rank_l)
        assert not (ret is None)
        self.is_high = ret
        return ret

    
                    
                

        










