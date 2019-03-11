import random
import sys

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            best=-100000
            possible=[]
            for l in legal:
                herustic=self.game.field.h1(l,self.game.my_botid, self.game.players) #*-1
                if herustic > best:
                    possible=[]
                    possible.append(l)
                    best=herustic
                elif herustic == best:
                    possible.append(l)
            (_,chosen)=(_, chosen) = random.choice(possible)
            self.game.issue_order(chosen)
    
