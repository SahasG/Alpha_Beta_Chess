import random
import copy
from Alpha_Beta_Chess import Chess_State

class Chess_Player():

    colors = ['w', 'b']
    values = {
        'p': 10,
        'N': 30,
        'B': 30,
        'R': 50,
        'Q': 100,
        'K': 900
    }

    def __init__(self):
        self.my_color = 'b'

    def findSucc(self, state):
        successors = []
        succ = state.getValidSuccessors()
        for s in succ:
            temp_state = copy.deepcopy(state)
            temp_state.move(s)
            successors.append(temp_state)
        return successors

    def game_value(self, state):
        #If white won
        if(state.checkMate == True and state.whiteTurn == True):
            return 1 if self.my_color == 'w' else -1
        #If black won
        if(state.checkMate == True and state.whiteTurn == False):
            return 1 if self.my_color == 'b' else -1

        return 0 # no winner yet

    def heuristic_value(self, state):
        total = 0
        for r in range(8):
            for c in range(8):
                if(state.board[r][c] != "--"):
                    if(state.board[r][c][0] == self.my_color):
                        total = total + self.values[state.board[r][c][1]]
                    else:
                        total = total - self.values[state.board[r][c][1]]
        return total

    def Max_Value(self, state, depth, alpha, beta):
        if(self.game_value(state) == 1):
            return 1
        elif(self.game_value(state) == -1):
            return -1
        else:
            if(depth == 4):
                return self.heuristic_value(state)
            else:
                for s in self.findSucc(state):
                    alpha = max(alpha, self.Min_Value(state, depth+1, alpha, beta))
                    if(alpha >= beta):
                        return beta
            return alpha

    def Min_Value(self, state, depth, alpha, beta):
        if (self.game_value(state) == 1):
            return 1
        elif (self.game_value(state) == -1):
            return -1
        else:
            if (depth == 4):
                return self.heuristic_value(state)
            else:
                for s in self.findSucc(state):
                    beta = min(beta, self.Min_Value(state, depth + 1, alpha, beta))
                    if (alpha >= beta):
                        return alpha
            return beta

    def make_move(self, state):


        max_alpha = float('-inf')
        best_move = []
        successors = self.findSucc(state)
        for s in successors:
            curr_alpha = self.Max_Value(state, 0, float('-inf'), float('inf'))
            if(curr_alpha > max_alpha):
                max_alpha = curr_alpha
                best_move = s

        succ = state.getValidSuccessors()
        for s in succ:
            state.move(s)
            if(state.board == best_move.board):
                state.undo()
                print(s)
                return s
            state.undo()





