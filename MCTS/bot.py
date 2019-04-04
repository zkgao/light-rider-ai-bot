import random
import sys
import copy
from math import log, sqrt
import time

PLAYOUTS = 10
ROLLOUT_DEPTH = 5
WIN = 10000
LOSS = -WIN

# Reference: https://int8.io/monte-carlo-tree-search-beginners-guide/

class Bot:
    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        # with open('../lightriders_mcts/tmp.txt', 'a') as f:
                # print('starting turn', file=f)
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        elif len(legal) == 1 or len(legal) == 4:
            (_, chosen) = random.choice(legal)
            self.game.issue_order(chosen)
        else:
            root = Node(self.game.field, self.game.my_botid, self.game.players, (self.game.players[self.game.my_botid].row, self.game.players[self.game.my_botid].col))
            best_child = self.monte_carlo_tree_search(root)
            (_, chosen) = best_child.move
            # (_, chosen) = random.choice(legal)
            self.game.time_remaining()
            self.game.issue_order(chosen)

    def monte_carlo_tree_search(self, root):
        playouts = PLAYOUTS
        tree = Tree(root, self.game.my_botid)
        # tree.printf(str(self.game.field.width) + "x" + str(self.game.field.height))
        while(playouts > 0):
            # with open('../lightriders_mcts/tmp.txt', 'a') as f:
                # print('new playout', file=f)
            # tree.printf("playouts =" +  str(playouts))
            leaf = tree.traverse(root)
            assert leaf != None, "leaf is none"
            # tree.printf(leaf.state.cell)
            if leaf.children == None:
                leaf.children = leaf.get_children()
            simulation_result = tree.rollout(leaf)
            tree.backpropagate(leaf, simulation_result)
            # tree.printf("done backpropagate")
            tree.check_expanded(leaf.parent)
            playouts -= 1
        return root.best_child()

class Tree:
    def __init__(self, root, botid):
        self.root = root
        self.root.children = self.root.get_children()
        self.depth = ROLLOUT_DEPTH
        self.botid = botid

    def traverse(self, node):
        # self.printf("traverse")
        while node is not None and node.expanded:
            prev = node
            node = node.best_uct()
        if node == None:
            return prev
        x = node.unvisited_child()
        if x is not None:
            return x
        else:
            return node

    def rollout(self, node):
        # self.printf("rollout")
        d = 0
        while not node.is_terminal() and d < self.depth:
            node = node.rollout_policy()
            d += 1
        # self.printf(d)
        return node.result(self.botid)
    
    def backpropagate(self, node, result):
        while node is not None:
            node.update_values(result)
            node.visited = True
            node = node.parent

    def check_expanded(self, node):
        if all([c.visited for c in node.children]):
            node.expanded = True

    def printf(self, s):
        with open('../lightriders_mcts/tmp.txt', 'a') as f:
            print(s, file=f)
class Node:
    def __init__(self, field, player_id, players, pos, parent=None, move=None):
        # self.printf("init node")
        self.state = field
        self.player_id = player_id
        self.players = players
        self.pos = pos
        self.parent = parent
        self.wins = 0
        self.losses = 0
        self.visits = 0
        self.children = None
        self.move = move
        self.value = 0
        self.visited = False
        self.expanded = False

    def get_children(self):
        # self.printf("get children")
        legal = self.state.legal_moves(self.player_id, self.players, self.pos)
        children = []
        if(not self.is_terminal()):
            # self.printf("start")
            for move in legal:
                # self.printf('before')
                # self.printf(self.state.cell)
                pos = self.state.field_forward(move, self.player_id, self.pos)
                children.append(Node(copy.deepcopy(self.state), self.player_id ^ 1, self.players, self.pos, self, move))
                # self.printf('forward')
                # self.printf(self.state.cell)
                self.state.field_reverse(move, self.player_id, pos)
                # self.printf('reverse')
                # self.printf(self.state.cell)
        return children
    
    def best_child(self):
        # self.printf("best child")
        if self.is_terminal():
            return None
        mx_child = self.children[0]
        for child in self.children[1:]:
            if child.value * child.visits > mx_child.value * mx_child.visits:
                mx_child = child
        return mx_child
    
    def best_uct(self):
        # self.printf("best uct")
        if self.is_terminal():
            return None
        mx_child = self.children[0]
        for child in self.children[1:]:
            if child.uct() > mx_child.uct():
                mx_child = child
        return mx_child

    def unvisited_child(self):
        if self.is_terminal():
            return None
        for child in self.children:
            if not child.visited:
                return child
        return None

    def uct(self):
        # self.printf("uct")
        try:
            return self.q() + 5*(sqrt(log(self.parent.visits) / 5 * self.visits))
            # return (self.q() / self.visits) + 0.8*(sqrt(log(self.parent.visits) / self.visits))
        except ZeroDivisionError:
            return 0
    
    def q(self):
        # self.printf("q value")
        return self.value

    def is_terminal(self):
        # self.printf("is terminal")
        legal = self.state.legal_moves(self.player_id, self.players, self.pos)
        return len(legal) == 0

    def result(self, botid):
        # self.printf("result")
        if self.is_terminal():
            if self.player_id == botid:
                return LOSS
            else:
                return WIN
        reachable, hlist = self.state.h21(self.player_id, self.pos)
        enemy_reachable, elist = self.state.h21(self.player_id ^ 1, self.pos)
        territory=0
        for i in range(256):
            if hlist[i] < elist[i]:
                territory += 1
        # self.printf(str(self.player_id) + ',' + str(territory))
        # return territory
        # return reachable
        # return 'loss'
        return self.state.ki(self.player_id, self.pos) + territory

    def update_values(self, result):
        # self.printf("update values")
        # if result == 'win':
            # self.wins += WIN
        # if result == 'loss':
        #     self.losses += LOSS
        # else:
        #     self.value = result
        self.visits += 1
        self.value = ((self.value * self.visits - 1) + result) / self.visits

    def get_random_child(self):
        legal = self.state.legal_moves(self.player_id, self.players, self.pos)
        if len(legal) == 0:
            return None
        move = random.choice(legal)
        pos = self.state.field_forward(move, self.player_id, self.pos)
        child = Node(copy.deepcopy(self.state), self.player_id ^ 1, self.players, pos, self, move)
        self.state.field_reverse(move, self.player_id, pos)
        return child

    def rollout_policy(self):
        # self.printf("rollout policy")
        # children = self.get_children()
        # return random.choice(children)
        return self.get_random_child()

    def printf(self, s):
        with open('../lightriders_mcts/tmp.txt', 'a') as f:
            print(s, file=f)
