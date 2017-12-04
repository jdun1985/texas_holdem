class Card():
    def __init__(self, face, rank, suit):
        self.face = face
        self.rank = rank
        self.suit = suit        

    def printCard(self):
        print('(' + str(self.face) + ',' + str(self.rank) + ',' + str(self.suit), end = ')')
        
    def testFuncToBeRemoved(self):
        if (True):
            print("This function is to be removed")