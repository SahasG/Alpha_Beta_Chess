import copy

class Game():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteTurn = True
        self.Log = []

    def move(self, move):
        self.board[move.dest_row][move.dest_col] = self.board[move.source_row][move.source_col]
        self.board[move.source_row][move.source_col] = "--"
        self.Log.append(move)
        self.whiteTurn = not self.whiteTurn

    def undo(self):
        if(len(self.Log) != 0):
            move = self.Log.pop()
            self.board[move.source_row][move.source_col] = move.source
            self.board[move.dest_row][move.dest_col] = move.dest
            self.whiteTurn = not self.whiteTurn

    def getValidSuccessors(self):
        return self.getSuccessors()

    def getSuccessors(self):
        successors = [Move((6,4), (4,4), self.board)]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (((self.whiteTurn == True) and (self.board[row][col][0] == 'w')) or ((not self.whiteTurn == True) and (self.board[row][col][0] == 'b'))):
                    chessPiece = self.board[row][col][1]
                    if chessPiece == 'p':
                        self.getPawnSuccessors(row, col, successors)
                    elif chessPiece == 'R':
                        self.getRookSuccessors(row, col, successors)
                    #TODO: A function for each type of piece
                    elif chessPiece == 'B':
                        self.getBishopSuccessors(row, col, successors)
                    elif chessPiece == 'N':
                        self.getKnightSuccessors(row, col, successors)
                    elif chessPiece == 'K':
                        self.getKingSuccessors(row, col, successors)
                    elif chessPiece == 'Q':
                        self.getQueenSuccessors(row, col, successors)
        return successors

    def getPawnSuccessors(self, row, col, successors):
        if((self.whiteTurn == True) and (self.board[row][col][0] == 'w')):
            if(self.board[row-1][col] == "--"):
                successors.append(Move((row, col), (row-1, col), self.board))
                if(row == 6):
                    if(self.board[row-2][col] == "--" ):
                        successors.append(Move((row, col), (row-2, col), self.board))
            if(col == 0 and self.board[row-1][col+1][0] == 'b'):
                successors.append(Move((row,col), (row-1, col+1), self.board))
            if(col == 7 and self.board[row-1][col-1][0] == 'b'):
                successors.append(Move((row, col), (row-1, col-1), self.board))
            if(col != 0 and col != 7 and self.board[row-1][col-1][0] == 'b'):
                successors.append(Move((row, col), (row-1, col-1), self.board))
            if(col != 0 and col != 7 and self.board[row-1][col+1][0] == 'b'):
                successors.append(Move((row,col), (row-1, col+1), self.board))
        else:
            if (self.board[row + 1][col] == "--"):
                successors.append(Move((row, col), (row + 1, col), self.board))
                if (row == 1):
                    if(self.board[row + 2][col] == "--"):
                        successors.append(Move((row, col), (row + 2, col), self.board))
            if (col == 0 and self.board[row + 1][col + 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col + 1), self.board))
            if (col == 7 and self.board[row + 1][col - 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row + 1][col - 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row + 1][col + 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col + 1), self.board))


    def getRookSuccessors(self, row, col, successors):
        for c in range(8):
            if(col+c == col):
                pass
            elif(col+c >= 8):
                break
            elif(self.board[row][col+c] == "--"):
                successors.append(Move((row, col), (row, col+c), self.board))
            elif(self.board[row][col+c][0] == 'b'):
                if(self.whiteTurn == True):
                    successors.append(Move((row, col), (row, col+c), self.board))
                    break
                else:
                    break
            elif(self.board[row][col+c][0] == 'w'):
                if(self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row, col+c), self.board))
                    break
        for c in range(8):
            if(col-c == col):
                pass
            elif((col - c) < 0):
                break
            elif(self.board[row][col - c] == "--"):
                successors.append(Move((row, col), (row, col - c), self.board))
            elif (self.board[row][col - c][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row, col - c), self.board))
                    break
                else:
                    break
            elif (self.board[row][col - c][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row, col - c), self.board))
                    break
        for r in range(8):
            if(row+r == row):
                pass
            elif((row+r) >= 8):
                break
            elif(self.board[row+r][col] == "--"):
                successors.append(Move((row,col), (row+r, col), self.board))
            elif (self.board[row+r][col][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row+r, col), self.board))
                    break
                else:
                    break
            elif (self.board[row+r][col][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row+r, col), self.board))
                    break
        for r in range(8):
            if (row - r == row):
                continue
            elif ((row - r) < 0):
                break
            elif (self.board[row - r][col] == "--"):
                successors.append(Move((row, col), (row - r, col), self.board))
            elif (self.board[row - r][col][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row - r, col), self.board))
                    break
                else:
                    break
            elif (self.board[row - r][col][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row - r, col), self.board))
                    break

    def getKnightSuccessors(self, row, col, successors):
        pass

    def getBishopSuccessors(self, row, col, successors):
        for i in range(8):
            if(row+i == row and col+i == col):
                continue
            elif(row+i >= 8):
                break
            elif(col+i >= 8):
                break
            elif(self.board[row+i][col+i] == "--"):
                successors.append(Move((row, col), (row+i, col+i), self.board))
            elif (self.board[row+i][col+i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row+i, col+i), self.board))
                    break
                else:
                    break
            elif (self.board[row+i][col+i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row+i, col+i), self.board))
                    break
        for i in range(8):
            if(row-i == row and col+i == col):
                continue
            elif(row-i < 0):
                break
            elif(col+i >= 8):
                break
            elif(self.board[row-i][col+i] == "--"):
                successors.append(Move((row, col), (row-i, col+i), self.board))
            elif (self.board[row-i][col+i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row-i, col+i), self.board))
                    break
                else:
                    break
            elif (self.board[row-i][col+i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row-i, col+i), self.board))
                    break
        for i in range(8):
            if(row+i == row and col-i == col):
                continue
            elif(row+i >= 8):
                break
            elif(col-i < 0):
                break
            elif(self.board[row+i][col-i] == "--"):
                successors.append(Move((row, col), (row+i, col-i), self.board))
            elif (self.board[row+i][col-i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row+i, col-i), self.board))
                    break
                else:
                    break
            elif (self.board[row+i][col-i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row+i, col-i), self.board))
                    break
        for i in range(8):
            if(row-i == row and col-i == col):
                continue
            elif(row-i < 0):
                break
            elif(col-i < 0):
                break
            elif(self.board[row-i][col-i] == "--"):
                successors.append(Move((row, col), (row-i, col-i), self.board))
            elif (self.board[row-i][col-i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row-i, col-i), self.board))
                    break
                else:
                    break
            elif (self.board[row-i][col-i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row-i, col-i), self.board))
                    break
    def getKingSuccessors(self, row, col, successors):
        pass

    def getQueenSuccessors(self, row, col, successors):
        pass



class Move():

    letterToRowNotation = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}

    rowToLetterNotation = {v: k for k, v in letterToRowNotation.items()}

    letterToColNotation = {"h" : 7, "g" : 6, "f" : 5, "e" : 4, "d" : 3, "c" : 2, "b" : 1, "a" : 0}

    colToLetterNotation = {v: k for k, v in letterToColNotation.items()}

    def __init__(self, source, dest, board):
        self.source_row = source[0]
        self.source_col = source[1]
        self.dest_row = dest[0]
        self.dest_col = dest[1]
        self.source = board[self.source_row][self.source_col]
        self.dest = board[self.dest_row][self.dest_col]
        self.ID = self.source_row*1000 + self.dest_row*100 + self.source_col*10 + self.dest_col

    '''
    Equals method that has been overrode
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.ID == other.ID
        return False