import random
import sys

TREE_DEPTH = 6
LOST_VALUE = -10

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
            best_value = -100000
            best_move = None
            for move in legal:
                self.game.field.field_forward(move, self.game.my_botid, self.game.players)
                value = self.minimax((self.game.my_botid + 1)%2, 0, False)
                self.game.field.field_reverse(move, self.game.my_botid, self.game.players)
                if value > best_value:
                    best_value = value
                    best_move = move
            # assert best_move != legal[0], "best move didn't get updated"
            (_, chosen) = best_move
            self.game.issue_order(chosen)
            
    def minimax(self, curr_botid, depth, maximizing_player):
        legal = self.game.field.legal_moves(curr_botid, self.game.players)
        if len(legal) == 0:
            #state is terminal
            return LOST_VALUE
        if depth == TREE_DEPTH:
            # return self.game.field.h1(curr_botid, self.game.players)
            h1,h2,h3,h4,h5,h6,h7=self.get_herustic()
            weight=[1,0,0,0,0,0,0]
            herustic=h1*weight[0]+h2*weight[1]+h3*weight[2]+h4*weight[3]+h5*weight[4]+h6*weight[5]+h7*weight[6]
            return herustic
        next_botid = (curr_botid + 1) % 2
        if maximizing_player:
            best_value = -10000
            for move in legal:
                self.game.field.field_forward(move, curr_botid, self.game.players)
                value = self.minimax(next_botid, depth + 1, False)
                self.game.field.field_reverse(move, curr_botid, self.game.players)
                if value > best_value:
                    best_value = value
                    # best_move = move
            return best_value
        if not maximizing_player:
            best_value = 10000
            for move in legal:
                self.game.field.field_forward(move, curr_botid, self.game.players)
                value = self.minimax(next_botid, depth + 1, True)
                self.game.field.field_reverse(move, curr_botid, self.game.players)
                if value < best_value:
                    best_value = value
                    # best_move = move
            return best_value          
    
