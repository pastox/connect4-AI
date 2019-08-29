from player import Player
import copy
import numpy as np
import utils

class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """
	
    def __init__(self):
        self.name = "Pastox"
        self.depth = 3
    
    def getColumn(self, board):
        if self.is_empty(board): # if the AI has to start, it starts in the middle
            return 3
        else:
            maxi = -np.inf 
            selected_col = 0
            for col in board.getPossibleColumns(): # get the column that has the maximum min_value
                new_board = copy.deepcopy(board)
                row = new_board.getHeight(col)
                new_board.board[col][row] = self.color 
                if self.is_ended((col,row),new_board): # if playing col ends the game, the AI should play col
                    return col 
                value = self.min_value(new_board, -np.inf, np.inf, self.depth)
                if value > maxi:
                    maxi = value
                    selected_col = col
            return selected_col
        
    def max_value(self, board, alpha, beta, depth): # when this function is called, the current node in the tree is a situation where it is the AI's turn to play
        if depth == 0: # if the depth is 0, just return the value of the board's heuristic
            heuristic = self.heuristic(board)
            return heuristic
        else: 
            for col in board.getPossibleColumns():
                new_board = copy.deepcopy(board)
                row = new_board.getHeight(col)
                new_board.board[col][row] = self.color
                if self.is_ended((col,row),new_board): # in this case, the AI can win from this state by playing col, so depth is decreased to 0 because there's no need to visit the tree deeper
                    alpha = max(alpha, self.min_value(new_board, alpha, beta, 0)) 
                else:
                    alpha = max(alpha, self.min_value(new_board, alpha, beta, depth-1)) # the alpha for this board is the max of the betas among the children
                if alpha >= beta: # in this case, one can cut the tree and stop exploring from board
                    return beta 
            return alpha
        
    def min_value(self, board, alpha, beta, depth):
        if depth == 0:
            heuristic = self.heuristic( board)
            return heuristic
        else: 
            for col in board.getPossibleColumns():
                new_board = copy.deepcopy(board)
                row = new_board.getHeight(col)
                new_board.board[col][row] = -self.color
                if self.is_ended((col,row),new_board):
                    beta = min(beta, self.max_value(new_board, alpha, beta, 0))   
                else:
                    beta = min(beta, self.max_value(new_board, alpha, beta, depth-1))
                if alpha >= beta:
                    return beta
            return beta

    def heuristic(self, board): # look at all the rows, columns and diagonals and compute points according to compute_points_in_line for both self.color and -self.color
        points = 0
        for row in range(board.num_rows):
            line = board.getRow(row)
            points += self.compute_points_in_line(line, self.color)
            points += self.compute_points_in_line(line, -self.color)
        for col in range(board.num_cols):
            line = board.getCol(col)
            points += self.compute_points_in_line(line, self.color)
            points += self.compute_points_in_line(line, -self.color)
        for shift1 in range(-board.num_cols + 5, board.num_cols - 3):
            line = board.getDiagonal(True, shift1)
            points += self.compute_points_in_line(line, self.color)
            points += self.compute_points_in_line(line, -self.color)
        for shift2 in range(3, board.num_cols + 2):
            line = board.getDiagonal(False, shift2)
            points += self.compute_points_in_line(line, self.color)
            points += self.compute_points_in_line(line, -self.color)
        return points
    
    def compute_points_in_line(self, line, color): # computes the number of points in a line to add to the heuristic of board
        res = 0
        k = 0
        while k < len(line): #go through the line
            if line[k] == color: #everytime one sees a coin with the color color
                j = 1 # number of spots until next opponent coin
                c = 1 # number of spots with the color color until next opponent coin
                anti_c = 0 # number of white spots separating color colored coins in case c>=4
                while k+j < len(line) and line[k+j] != -color: # while one doesn't encounter any opponent coin
                    if line[k+j] == color:
                        c+=1 # increase c everytime one sees a color colored coin
                    else:
                        if c < 4: # anti_c is only used when c >= 4 : if anti_c is 0 and c>=4, then there are 4 color colored coins in a row
                            anti_c += 1
                    j+=1
                k += j
                i = 1
                while k-i >= 0 and line[k-i] == 0: # we also need to know how many spots are free before spot k in the line
                    i+=1
                if color == self.color: #add point for the AI's coins
                    if c == 2 and i+j-1  >= 4: # 2 coins aligned and space for at least 4 coins
                        res += 20
                    elif c == 3 and i+j-1 >= 4: # 3 coins aligned and space for at least 4 coins
                        res += 50
                    elif c == 4 and i+j-1 >= 4: # 4 coins aligned
                        if anti_c == 0: # the 4 coins are consecutive
                            res += 10000
                        else:
                            res += 50
                else: # decrease points for the opponent's coins
                    if c == 2 and i+j-1  >= 4: # 2 coins aligned and space for at least 4 coins
                        res -= 10
                    elif c == 3 and i+j-1 >= 4: # 3 coins aligned and space for at least 4 coins
                        res -= 25
                    elif c == 4 and i+j-1 >= 4: # 4 coins aligned
                        if anti_c == 0: # the 4 coins are consecutive
                            res -= 10000
                        else:
                            res -= 50
            else:
                k += 1
        return res
    
    def is_empty(self, board): # check wether the board is empty or not
        for col in board:
            for row in col:
                if row != 0:
                    return False
        return True
    
    def is_ended(self, pos, board): # checks wether the game is ended or not
        """Returns whether the game is over or not"""
        tests = []
        tests.append(board.getCol(pos[0]))
        tests.append(board.getRow(pos[1]))
        tests.append(board.getDiagonal(True, pos[0] - pos[1]))
        tests.append(board.getDiagonal(False, pos[0] + pos[1]))
        for test in tests:
            color, size = utils.longest(test)
            if size >= 4:
                return True
        return False