class PlayerAction():
    '''This class contains the bets posted by each player, and the activity
    surrounding each betting session.
    
    It is exclusively a data structure and contains no logic beyond reporting.
    
    TODO: SERIALIZE/SQLIZE
    
    '''
    def __init__(self):
        self.blind = 0
        self.pre_flop = 0
        self.flop = 0
        self.turn = 0
        self.river = 0
        
        '''Logs of the players actions for a single hand, these are lists,
        to account for multiple betting round activity.
        '''
        self.act_blind = []  
        self.act_pre_flop = []
        self.act_flop = []
        self.act_turn = []
        self.act_river = []
        
    def total(self):
        return self.blind + self.pre_flop + self.flop + self.turn + self.river

        

