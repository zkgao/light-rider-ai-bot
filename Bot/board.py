import copy
import sys
import random

PLAYER1, PLAYER2, EMPTY, BLOCKED = [0, 1, 2, 3]
S_PLAYER1, S_PLAYER2, S_EMPTY, S_BLOCKED, = ['0', '1', '.', 'x']

CHARTABLE = [(PLAYER1, S_PLAYER1), (PLAYER2, S_PLAYER2), (EMPTY, S_EMPTY), (BLOCKED, S_BLOCKED)]

DIRS = [
    ((-1, 0), "up"),
    ((0, 1), "right"),
    ((1, 0), "down"),
    ((0, -1), "left")
]

class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell = [[[EMPTY] for col in range (0, width)] for row in range(0, height)]

    def parse_cell_char(self, players, row, col, char):
        result = -1
        if char == S_PLAYER1:
            players[0].row = row;
            players[0].col = col;
        elif char == S_PLAYER2:
            players[1].row = row;
            players[1].col = col;
        for (i, symbol) in CHARTABLE:
            if symbol == char:
                result = i
                break
        return result

    def parse_cell(self, players, row, col, data):
        cell = []
        for char in data:
            item = self.parse_cell_char(players, row, col, char)
            cell.append(item)
        return cell

    def parse(self, players, data):
        cells = data.split(',')
        col = 0
        row = 0
        for cell in cells:
            if (col >= self.width):
                col = 0
                row +=1
            self.cell[row][col] = self.parse_cell(players, row, col, cell)
            col += 1

    def in_bounds (self, row, col):
        return row >= 0 and col >= 0 and col < self.width and row < self.height

    def is_legal(self, row, col, my_id):
        enemy_id = my_id ^ 1
        return (self.in_bounds(row, col)) and (not BLOCKED in self.cell[row][col]) and (not enemy_id in self.cell[row][col])

    def is_legal_tuple(self, loc):
        row, col = loc
        return self.is_legal(row, col)

    def get_adjacent(self, row, col,my_id):
        result = []
        for (o_row, o_col), _ in DIRS:
            t_row, t_col = o_row + row, o_col + col
            if self.is_legal(t_row, t_col,my_id):
                result.append((t_row, t_col))
        return result

    def legal_moves(self, my_id, players):
        my_player = players[my_id]
        result = []
        for ((o_row, o_col), order) in DIRS:
            t_row = my_player.row + o_row
            t_col = my_player.col + o_col
            if self.is_legal(t_row, t_col, my_id):
                result.append(((o_row, o_col), order))
            else:
                pass
        random.shuffle(result)
        return result

    def output_cell(self, cell):
        done = False
        for (i, symbol) in CHARTABLE:
            if i in cell:
                if not done:
                    sys.stderr.write(symbol)
                done = True
                break
        if not done:
            sys.stderr.write("!")
            done = True
                

    def output(self):
        for row in self.cell:
            sys.stderr.write("\n")
            for cell in row:
                self.output_cell(cell)
        sys.stderr.write("\n")
        sys.stderr.flush()
        
    def h1(self,my_id, players):
        my_player = players[my_id]
        t_row = my_player.row 
        t_col = my_player.col
        count=0
        while self.is_legal(t_row,t_col,my_id):
            t_row +=1
            count +=1
        t_row = my_player.row 
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_col +=1
            count +=1
        t_row = my_player.row 
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_row -=1
            count +=1
        t_row = my_player.row 
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_col -=1
            count +=1
        return count

    def h2(self,my_id, players):
        my_player = players[my_id]
        t_row = my_player.row 
        t_col = my_player.col
        openlist=[]
        tlist=self.get_adjacent(t_row,t_col,my_id)
        openlist.extend(tlist)
        #closedlist=[]
        #closedlist.append((t_row,t_col))
        depth=[400]*400
        for tl in tlist:
            (tl_row,tl_col)=tl
            depth[self.width*tl_row+tl_col]=1
        depth[self.width*t_row+t_col]=0
        count=0
        while(len(openlist)!= 0):
            current=openlist.pop(0)
            #closedlist.append(current)
            (c_row,c_col)=current
            for (o_row, o_col), _ in DIRS:
                t_row, t_col = o_row + c_row, o_col + c_col
                if self.is_legal(t_row, t_col,my_id):
                    if not depth[t_row*self.width+t_col] == 400:
                        
                        depth[t_row*self.width+t_col]=depth[c_row*self.width+c_col]+1
                        if depth[t_row*self.width+t_col]>7:
                            return count,depth
                        openlist.append((t_row, t_col))
                        count+=1
        return count,depth   
    def ki(self,my_id, players):
        my_player = players[my_id]
        t_row = my_player.row 
        t_col = my_player.col
        tlist=self.get_adjacent(t_row,t_col,my_id)
        return len(tlist)
        
    def h3(self,my_id, players):
        my_player = players[my_id]
        t_row = my_player.row 
        t_col = my_player.col
        count=0
        while self.is_legal(t_row,t_col,my_id):
            t_row +=1
            count +=1
        tmp=count
        count=0
        t_row = my_player.row 
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_col +=1
            count +=1
        if count < tmp and count > 0:
            tmp=count
        count=0
        t_row = my_player.row
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_row -=1
            count +=1
        if count < tmp and count > 0:
            tmp=count
        count=0
        t_row = my_player.row 
        t_col = my_player.col 
        while self.is_legal(t_row,t_col,my_id):
            t_col -=1
            count +=1
        if count < tmp and count > 0:
            tmp=count
        count=0
        return tmp

    def h21(self, my_id, players):
        my_player = players[my_id]
        t_row = my_player.row 
        t_col = my_player.col
        openlist = []
        tlist = self.get_adjacent(t_row, t_col, my_id)
        openlist.extend(tlist)
        #closedlist=[]
        #closedlist.append((t_row,t_col))
        visited = [False] * self.width * self.height
        depth = [0] * self.width * self.height
        depth[self.width * t_row + t_col] = 0
        visited[self.width * t_row + t_col] = True
        for tl in tlist:
            (tl_row, tl_col) = tl
            depth[self.width * tl_row + tl_col] = 1
        count = 0
        while len(openlist) != 0:
            current = openlist.pop(0)
            #closedlist.append(current)
            (c_row, c_col) = current
            tlist = self.get_adjacent(c_row, c_col, my_id)
            for tl in tlist:
                (tl_row, tl_col) = tl
                if not visited[self.width * tl_row + tl_col]:
                    depth[self.width * tl_row + tl_col] = depth[c_row * self.width + c_col] + 1
                    count += 1
                    openlist.append(tl)
                    visited[self.width * tl_row + tl_col] = True
                    if depth[self.width * tl_row + tl_col] > 4:
                            return count, depth
        return count, depth

    def h8(self, my_id, players):
        my_player = players[my_id]
        frontier = [self.get_adjacent(my_player.row, my_player.col, my_id)]
        count = 0
        depth = 0
        while(len(frontier) != 0):
            level = frontier.pop(0)
            depth += 1
            if(depth == 10):
                break
            tmp = set()
            for curr in level:
                tmp = tmp.union(set(self.get_adjacent(*curr, my_id)))
            frontier.append(list(tmp))
        return depth

    def field_forward(self, move, p_id, players):
        curr_player = players[p_id]
        old_row, old_col = curr_player.row, curr_player.col
        ((o_row, o_col),_) = move
        new_row, new_col = curr_player.row + o_row, curr_player.col + o_col
        self.cell[old_row][old_col] = [BLOCKED];
        self.cell[new_row][new_col] = [CHARTABLE[p_id][1]]
        curr_player.row, curr_player.col = new_row, new_col

    def field_reverse(self, move, p_id, players):
        curr_player = players[p_id]
        old_row, old_col = curr_player.row, curr_player.col
        ((o_row, o_col),_) = move
        new_row, new_col = curr_player.row - o_row, curr_player.col - o_col
        self.cell[old_row][old_col] = [EMPTY];
        self.cell[new_row][new_col] = [CHARTABLE[p_id][1]]
        curr_player.row, curr_player.col = new_row, new_col
