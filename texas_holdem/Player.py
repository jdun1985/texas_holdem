from texas_holdem.PlayerAction import PlayerAction

class Player():

    def __init__(self, name):
        self.name = name
        self.stack = None
        self.bets = [] # Contains a list of PlayerAction(), one for each new hand
        self.hole_cards = []
        self.is_all_in = False
        self.hand_index = None # Contains the current hand index for a given game, 
        
    def printPlayer(self):
        assert not (self.stack is None)
        print('Player: ' + str(self.name) + 'Chip value: ' + str(self.stack))
      
    def printHoleCards(self):
        for c in self.hole_cards:
            c.printCard()
        print()
    
    def printBets(self):
        for h in self.bets:
            print(' ' + str(h.blind))
            print(' ' + str(h.pre_flop))
            print(' ' + str(h.flop))
            print(' ' + str(h.turn))
            print(' ' + str(h.river))
        
    def setupHand(self, hand_index):
        
        self.hand_index = hand_index
        self.bets.append(PlayerAction())
    
    def postBlind(self, amount, blind_type, hand_index):
        '''Post the blind.
        
        It is possible for the player to post less than required, it is up to the Table to account
        for this scenario.
        
        Args:
            amount: an integer representing the amount of the blind the player is required to post.
            blind_type: a string representing the type of blind, it is either 'small' or 'big'
        Returns:
            integer representing the amount that the player posted.
        Raises:
            None
        '''
        assert self.stack > 0
        assert (blind_type == 'small') or (blind_type == 'big')
        
        if self.stack < amount:
            self.bets[hand_index].blind = self.stack
            self.stack = 0
            self.is_all_in = True
            self.bets[hand_index].act_blind.append('all-in on {} blind. blind required: {}, blind posted: {}'.format(blind_type, amount, self.bets[hand_index].blind))
            return self.bets[hand_index].blind
        else:
            self.bets[hand_index].blind = amount
            self.stack = self.stack - amount
            self.is_all_in = False
            self.bets[hand_index].act_blind.append('{} blind required: {}, blind posted: {}'.format(blind_type, amount, self.bets[hand_index].blind))
            return amount
        