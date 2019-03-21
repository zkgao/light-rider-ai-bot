import random
import sys

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game
    def get_herustic(self,l):
            reachable,hlist=self.game.field.h2(l,self.game.my_botid, self.game.players)
            enemy_reachable,hlist2=self.game.field.h2(l,self.game.my_botid ^ 1, self.game.players)
            territory=0
            for i in range(400):
                if hlist[i] < hlist2[i]:
                    territory+=1
            return reachable,enemy_reachable,territory
    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            best=-100000
            possible=[]
            for l in legal:
                herustic,herustic2,herustic3=self.get_herustic(l)
                if -1*herustic2 > best:
                    possible=[]
                    possible.append(l)
                    best=herustic
                elif herustic == best:
                    possible.append(l)
            (_,chosen)=(_, chosen) = random.choice(possible)
            self.game.issue_order(chosen)
    
