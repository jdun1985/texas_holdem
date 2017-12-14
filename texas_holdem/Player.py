from texas_holdem.PlayerAction import PlayerAction

class Player():

    def __init__(self, name):
        self.name = name
        self.stack = None
        self.bets = [] # Contains a list of PlayerAction(), one for each new hand.
        self.hole_cards = []
        self.is_all_in = False
        self.hand_index = None # Contains the current hand index for a given game. 
        self.hand_status = None # 'allin', 
        
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
    
    def postBlind(self, amount, blind_type):
        '''Post the blind.
        
        It is POSSIBLE for the player to post LESS than requested, it is up to the Table to account
        for this scenario.
        
        Args:
            amount: an integer representing the amount of the blind the player is required to post.
            blind_type: a string representing the type of blind, it is either 'small' or 'big'
        Returns:
            integer representing the amount that the player posted.
        Assumes:
            self.hand_index is setup properly.
        Raises:
            None
        '''
        assert self.stack > 0
        assert (blind_type == 'small') or (blind_type == 'big')
        
        if self.stack < amount:
            #There is not enough in the stack to cover the blind.  Payer is all-in.
            self.bets[self.hand_index].blind = self.stack
            self.stack = 0
            self.is_all_in = True
            self.hand_status = 'allin'
            self.bets[self.hand_index].act_blind.append(\
                'blind posted. {} blind. blind required: {}. blind posted: {}. all-in.'\
                .format(blind_type, amount, self.bets[self.hand_index].blind, self.name))
            return self.bets[self.hand_index].blind
        else:
            self.bets[self.hand_index].blind = amount
            self.stack = self.stack - amount
            self.is_all_in = False
            self.bets[self.hand_index].act_blind.append(\
                'blind posted. {} blind. blind required: {}. blind posted: {}.'\
                .format(blind_type, amount, self.bets[self.hand_index].blind))
            return amount
    
    def action(self, players, bet_round_type, hand_action, amount):
        '''
        Args: 
            players: The dictionary of players.
            bet_round_type: 'preflop', 'flop', 'turn', 'river'
            hand_action: 'check', 'bet'
        Returns: ?

        Check: 
        Check is the poker term for "pass." If it is your turn and there has been no bet or there is
        no blind to call, you may check and let the action pass to the next person. If everyone checks
        the round is over.
        
        Bet:
        If you don't feel like checking you may bet by putting chips/money into the pot
        The amount you can bet differs depending on what the betting structure is. Once there's a bet,
        the rest of the players have three actions to choose from.

        FACING A BET ACTIONS
            Call:
            To call is to match the amount one of your opponents has a bet. Your turn is over unless
            someone reopens the betting by raising. The round ends if everyone has either called or folded.
        
            Raise:
            If there is a bet, anyone left to act can raise by putting in more money than the original bet.
            
            Fold:
            Folding is simply throwing your hand away and waiting for the next one.

        '''

        assert hand_action in ['check', 'bet']
        assert self.stack > 0
        
        if self.hand_status == 'allin':
            print('Player prompted for action and is already all-in.')
            return
        
        if hand_action == 'bet':
            finished = False 
            while(not finished):
                # Player can call, raise, or fold.
                print('The current bet is: {}.'.format(amount))
                print('Your stack is: {}.'.format(self.stack))
                print('You can "call", "raise", or "fold".')
                choice = input('Please enter your choice:  ')
                
                if choice not in ['call', 'raise', 'fold']:
                    print('Your entry was not valid.')
                    finished = False
                    continue

                if choice == 'call':
                    if self.stack > amount:
                        pass
                    else: # Player is all-in.
                        self.is_all_in = True
                        self.hand_status = 'allin'
                        self.addBet(bet_round_type, amount)
                elif choice == 'raise':
                    pass
                else:# choice == 'fold':
                    pass
        else:
            pass
        
    
    def addBet(self, bet_round_type, action_type, amount):
        '''
        
        Args:
            bet_round_type:
            action_type:
            amount:
        Returns:
            integer representing the amount that the player bet.
        Assumes:
        Raises:
            None
        '''
        if bet_round_type == 'preflop':
            bet = self.stack if self.is_all_in else amount
            self.stack = 0 if self.is_all_in else (self.stack - bet)
            self.bets[self.hand_index].pre_flop = self.bets[self.hand_index].pre_flop + bet
            log = 'Action: {}. Bet required: {}. Bet made: {}.'\
                .format(action_type, amount, bet)
            if self.is_all_in:
                log.append(' all-in.')
            return bet
        
        elif bet_round_type == 'flop':
            pass
        elif bet_round_type == 'turn':
            pass
        elif bet_round_type == 'river':
            pass
        
        