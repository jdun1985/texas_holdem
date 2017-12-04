class PlayerAction():
    def __init__(self):
        self.blind = 0
        self.pre_flop = 0
        self.flop = 0
        self.turn = 0
        self.river = 0
        
        self.act_blind = []
        self.act_pre_flop = []
        self.act_flop = []
        self.act_turn = []
        self.act_river = []
        
    def total(self):
        return self.blind + self.pre_flop + self.flop + self.turn + self.river
    
    def reset(self):
        self.blind = self.pre_flop = self.flop = self.turn = self.river = 0