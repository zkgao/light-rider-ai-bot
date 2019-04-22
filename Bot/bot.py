import random
import sys

TREE_DEPTH = 4
LOST_VALUE = -10000
WIN_VALUE = 10000
INF = 100000

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game
    def get_herustic(self, curr_botid):
            #total_hit_dis = self.game.field.h1(self.game.my_botid, self.game.players)
            min_hit_dis=0
            total_hit_dis=0
            #min_hit_dis = self.game.field.h3(self.game.my_botid, self.game.players)
            ki=self.game.field.ki(curr_botid, self.game.players)
            enemy_ki = self.game.field.ki(self.game.my_botid ^ 1, self.game.players)
            reachable,hlist = self.game.field.h21(curr_botid, self.game.players)
            enemy_reachable,hlist2 = self.game.field.h21(curr_botid ^ 1, self.game.players)
            territory=0
            for i in range(256):
                if hlist[i] < hlist2[i]:
                    territory += 1
            # return reachable,400-enemy_reachable,territory,total_hit_dis,min_hit_dis,ki,4-enemy_ki
            weight=[3,1,1,1,1,2,2]
            #weight=[1,0,0,0,0,0,0,0]
            return territory*weight[0] + ki*weight[1]+total_hit_dis*weight[2]+min_hit_dis*weight[3]+reachable*weight[4]-enemy_ki*weight[5]-enemy_reachable*weight[6]
            # h1,h2,h3,h4,h5,h6,h7=self.get_herustic()
            # weight=[1,0,0,0,0,0,0]
            # herustic=h1*weight[0]+h2*weight[1]+h3*weight[2]+h4*weight[3]+h5*weight[4]+h6*weight[5]+h7*weight[6]
            # return herustic
    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            best_value = -INF
            best_move = None
            possible=[]
            if(len(legal) > 1):
                for move in legal:
                    self.game.field.field_forward(move, self.game.my_botid, self.game.players)
                    value = self.minimax(self.game.my_botid ^ 1, 0, False, -INF, INF)
                    self.game.field.field_reverse(move, self.game.my_botid, self.game.players)
                    if value > best_value:
                        best_value = value
                        possible= [move]
                    elif value == best_value:
                        possible.append(move)
            else:
                possible.append(legal[0])
            # assert best_move != legal[0], "best move didn't get updated"
            (_, chosen) = random.choice(possible)
            self.game.issue_order(chosen)
            
    def minimax(self, curr_botid, depth, maximizing_player, alpha, beta):
        legal = self.game.field.legal_moves(curr_botid, self.game.players)
        if len(legal) == 0:
            if self.game.my_botid == curr_botid:
            #state is terminal
                return LOST_VALUE
            else:
                return WIN_VALUE
        if depth == TREE_DEPTH:
            # return 0.01 * self.game.field.h8(curr_botid, self.game.players) + 1 * self.game.field.h1(curr_botid, self.game.players) + 100 * self.game.field.ki(curr_botid, self.game.players)
            return self.get_herustic(curr_botid)
        next_botid = curr_botid ^ 1
        if maximizing_player:
            best_value = -INF
            for move in legal:
                self.game.field.field_forward(move, curr_botid, self.game.players)
                value = self.minimax(next_botid, depth + 1, False, alpha, beta)
                self.game.field.field_reverse(move, curr_botid, self.game.players)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        if not maximizing_player:
            best_value = INF
            for move in legal:
                self.game.field.field_forward(move, curr_botid, self.game.players)
                value = self.minimax(next_botid, depth + 1, True, alpha, beta)
                self.game.field.field_reverse(move, curr_botid, self.game.players)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value          
