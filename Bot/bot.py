import random
import sys

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game
    def get_herustic():
            total_hit_dis=self.game.field.h1(self.game.my_botid, self.game.players)
            min_hit_dis=self.game.field.h3(self.game.my_botid, self.game.players)
            ki=self.game.field.ki(self.game.my_botid, self.game.players)
            enemy_ki=self.game.field.ki(self.game.my_botid ^ 1, self.game.players)
            reachable,hlist=self.game.field.h2(self.game.my_botid, self.game.players)
            enemy_reachable,hlist2=self.game.field.h2(self.game.my_botid ^ 1, self.game.players)
            territory=0
            for i in range(400):
                if hlist[i] < hlist2[i]:
                    territory+=1
            return reachable,400-enemy_reachable,territory,total_hit_dis,min_hit_dis,ki,4-enemy_ki
    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            best=-100000
            possible=[]
            for l in legal:
                h1,h2,h3,h4,h5,h6,h7=self.get_herustic(l)
                weight=[1,0,0,0,0,0,0]
                herustic=h1*weight[0]+h2*weight[1]+h3*weight[2]+h4*weight[3]+h5*weight[4]+h6*weight[5]+h7*weight[6]
                if herustic > best:
                    possible=[]
                    possible.append(l)
                    best=herustic
                elif herustic == best:
                    possible.append(l)
            (_,chosen)=(_, chosen) = random.choice(possible)
            self.game.issue_order(chosen)
    
