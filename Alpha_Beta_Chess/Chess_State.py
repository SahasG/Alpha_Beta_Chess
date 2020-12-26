
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
        self.wKCord = (7, 4)
        self.bKCord = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def move(self, move):
        self.board[move.dest_row][move.dest_col] = self.board[move.source_row][move.source_col]
        self.board[move.source_row][move.source_col] = "--"
        self.Log.append(move)
        self.whiteTurn = not self.whiteTurn
        if(move.source == "wK"):
            self.wKCord = (move.dest_row, move.dest_col)
        elif(move.source == "bK"):
            self.bKCord = (move.dest_row, move.dest_col)


    def undo(self):
        if(len(self.Log) != 0):
            move = self.Log.pop()
            self.board[move.source_row][move.source_col] = move.source
            self.board[move.dest_row][move.dest_col] = move.dest
            self.whiteTurn = not self.whiteTurn
            if (move.source == "wK"):
                self.wKCord = (move.source_row, move.source_col)
            elif (move.source == "bK"):
                self.bKCord = (move.source_row, move.source_col)

    def getValidSuccessors(self):
        """
        Algorithm:
        1) Find all successors
        2) For each succ make the move
        3) Find all successors of that move
        4) For each of the opponents move check if they can attack the king
        5) Undo the moves and remove moves that can leave the king vulnerable
        """
        successors = self.getSuccessors()
        for i in range(len(successors)-1, -1, -1):
            self.move(successors[i])
            self.whiteTurn = not self.whiteTurn
            if(self.check() == True):
                successors.remove(successors[i])
            self.whiteTurn = not self.whiteTurn
            self.undo()
        if(len(successors) == 0):
            if self.check():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return successors

    def getSuccessors(self):
        successors = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (((self.whiteTurn == True) and (self.board[row][col][0] == 'w')) or ((not self.whiteTurn == True) and (self.board[row][col][0] == 'b'))):
                    chessPiece = self.board[row][col][1]
                    if chessPiece == 'p':
                        self.getPawnSuccessors(row, col, successors)
                    elif chessPiece == 'R':
                        self.getRookSuccessors(row, col, successors)
                    elif chessPiece == 'B':
                        self.getBishopSuccessors(row, col, successors)
                    elif chessPiece == 'N':
                        self.getKnightSuccessors(row, col, successors)
                    elif chessPiece == 'K':
                        self.getKingSuccessors(row, col, successors)
                    elif chessPiece == 'Q':
                        self.getQueenSuccessors(row, col, successors)
        return successors

    def check(self):
        if(self.whiteTurn == True):
            return self.pieceAttacked(self.wKCord[0], self.wKCord[1])
        else:
            return self.pieceAttacked(self.bKCord[0], self.bKCord[1])

    def pieceAttacked(self, row, col):
        self.whiteTurn = not self.whiteTurn
        oppSuccessors = self.getSuccessors()
        for succ in oppSuccessors:
            if(succ.dest_row == row and succ.dest_col == col):
                self.whiteTurn = not self.whiteTurn
                return True
        self.whiteTurn = not self.whiteTurn
        return False

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
        if(row-2 < 0 or col-1 < 0):
            pass
        elif(self.board[row-2][col-1] == "--"):
            successors.append(Move((row, col), (row-2, col-1), self.board))
        elif(self.board[row-2][col-1][0] == 'b'):
            if(self.whiteTurn == True):
                successors.append(Move((row, col), (row - 2, col - 1), self.board))
        elif (self.board[row - 2][col - 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 2, col - 1), self.board))
        if (row - 1 < 0 or col - 2 < 0):
            pass
        elif (self.board[row - 1][col - 2] == "--"):
            successors.append(Move((row, col), (row - 1, col - 2), self.board))
        elif (self.board[row - 1][col - 2][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 1, col - 2), self.board))
        elif (self.board[row - 1][col - 2][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 1, col - 2), self.board))
        if (row + 1 > 7 or col - 2 < 0):
            pass
        elif (self.board[row + 1][col - 2] == "--"):
            successors.append(Move((row, col), (row + 1, col - 2), self.board))
        elif (self.board[row + 1][col - 2][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 1, col - 2), self.board))
        elif (self.board[row + 1][col - 2][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 1, col - 2), self.board))
        if (row + 2 > 7 or col - 1 < 0):
            pass
        elif (self.board[row + 2][col - 1] == "--"):
            successors.append(Move((row, col), (row + 2, col - 1), self.board))
        elif (self.board[row + 2][col - 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 2, col - 1), self.board))
        elif (self.board[row + 2][col - 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 2, col - 1), self.board))
        if (row + 2 > 7 or col + 1 > 7):
            pass
        elif (self.board[row + 2][col + 1] == "--"):
            successors.append(Move((row, col), (row + 2, col + 1), self.board))
        elif (self.board[row + 2][col + 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 2, col + 1), self.board))
        elif (self.board[row + 2][col + 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 2, col + 1), self.board))
        if (row + 1 > 7 or col + 2 > 7):
            pass
        elif (self.board[row + 1][col + 2] == "--"):
            successors.append(Move((row, col), (row + 1, col + 2), self.board))
        elif (self.board[row + 1][col + 2][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 1, col + 2), self.board))
        elif (self.board[row + 1][col + 2][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 1, col + 2), self.board))
        if (row - 1 < 0 or col + 2 > 7):
            pass
        elif (self.board[row - 1][col + 2] == "--"):
            successors.append(Move((row, col), (row - 1, col + 2), self.board))
        elif (self.board[row - 1][col + 2][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 1, col + 2), self.board))
        elif (self.board[row - 1][col + 2][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 1, col + 2), self.board))
        if (row - 2 < 0 or col + 1 > 7):
            pass
        elif (self.board[row - 2][col + 1] == "--"):
            successors.append(Move((row, col), (row - 2, col + 1), self.board))
        elif (self.board[row - 2][col + 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 2, col + 1), self.board))
        elif (self.board[row - 2][col + 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 2, col + 1), self.board))

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
        if(row+1 > 7 or col+1 > 7):
            pass
        elif(self.board[row+1][col+1] == "--"):
            successors.append(Move((row,col), (row+1, col+1), self.board))
        elif(self.board[row+1][col+1][0] == 'b'):
            if(self.whiteTurn == True):
                successors.append(Move((row,col), (row+1, col+1), self.board))
        elif(self.board[row+1][col+1][0] == 'w'):
            if(self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 1, col + 1), self.board))
        if (col + 1 > 7):
            pass
        elif (self.board[row][col + 1] == "--"):
            successors.append(Move((row, col), (row, col + 1), self.board))
        elif (self.board[row][col + 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row, col + 1), self.board))
        elif (self.board[row][col + 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row, col + 1), self.board))
        if (row - 1 < 0 or col + 1 > 7):
            pass
        elif (self.board[row - 1][col + 1] == "--"):
            successors.append(Move((row, col), (row - 1, col + 1), self.board))
        elif (self.board[row - 1][col + 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 1, col + 1), self.board))
        elif (self.board[row - 1][col + 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 1, col + 1), self.board))
        if (row - 1 < 0):
            pass
        elif (self.board[row - 1][col] == "--"):
            successors.append(Move((row, col), (row - 1, col), self.board))
        elif (self.board[row - 1][col][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 1, col), self.board))
        elif (self.board[row - 1][col][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 1, col), self.board))
        if (row - 1 < 0 or col - 1 < 0):
            pass
        elif (self.board[row - 1][col - 1] == "--"):
            successors.append(Move((row, col), (row - 1, col - 1), self.board))
        elif (self.board[row - 1][col - 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row - 1, col - 1), self.board))
        elif (self.board[row - 1][col - 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row - 1, col - 1), self.board))
        if (col - 1 < 0):
            pass
        elif (self.board[row][col - 1] == "--"):
            successors.append(Move((row, col), (row, col - 1), self.board))
        elif (self.board[row][col - 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row, col - 1), self.board))
        elif (self.board[row][col - 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row, col - 1), self.board))
        if (row + 1 > 7 or col - 1 < 0):
            pass
        elif (self.board[row + 1][col - 1] == "--"):
            successors.append(Move((row, col), (row + 1, col - 1), self.board))
        elif (self.board[row + 1][col - 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
        elif (self.board[row + 1][col - 1][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
        if (row + 1 > 7):
            pass
        elif (self.board[row + 1][col] == "--"):
            successors.append(Move((row, col), (row + 1, col), self.board))
        elif (self.board[row + 1][col][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 1, col), self.board))
        elif (self.board[row + 1][col][0] == 'w'):
            if (self.whiteTurn == True):
                pass
            else:
                successors.append(Move((row, col), (row + 1, col), self.board))

    def getQueenSuccessors(self, row, col, successors):
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


class Move():

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