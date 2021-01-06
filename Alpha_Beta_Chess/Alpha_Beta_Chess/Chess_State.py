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
        self.lastMoveMade = None
        self.castlingRights = Castling()

    def move(self, move, pieceToPromote='None'):
        self.board[move.dest_row][move.dest_col] = self.board[move.source_row][move.source_col]
        self.board[move.source_row][move.source_col] = "--"
        if (move.source == "wK"):
            self.castlingRights.whiteKingMoved = True
            self.castlingRights.whiteKingMovedAt.append(move)
        elif (move.source == "bK"):
            self.castlingRights.blackKingMoved = True
            self.castlingRights.blackKingMovedAt.append(move)
        elif ((move.source == "bR") and (move.source_col == 7)):
            self.castlingRights.blackRightRookMoved = True
            self.castlingRights.blackRightRookMovedAt.append(move)
        elif ((move.source == "bR") and (move.source_col == 0)):
            self.castlingRights.blackLeftRookMoved = True
            self.castlingRights.blackLeftRookMovedAt.append(move)
        elif ((move.source == "wR") and (move.source_col == 7)):
            self.castlingRights.whiteRightRookMoved = True
            self.castlingRights.whiteRightRookMovedAt.append(move)
        elif ((move.source == "wR") and (move.source_col == 0)):
            self.castlingRights.whiteLeftRookMoved = True
            self.castlingRights.whiteLeftRookMovedAt.append(move)

        self.Log.append(move)
        self.lastMoveMade = move
        self.whiteTurn = not self.whiteTurn
        if (move.source == "wK"):
            self.wKCord = (move.dest_row, move.dest_col)
        elif (move.source == "bK"):
            self.bKCord = (move.dest_row, move.dest_col)

        if ((pieceToPromote == 'Q') and (move.pawnPromotion == True)):
            self.board[move.dest_row][move.dest_col] = move.source[0] + pieceToPromote
        elif ((pieceToPromote == 'B') and (move.pawnPromotion == True)):
            self.board[move.dest_row][move.dest_col] = move.source[0] + pieceToPromote
        elif ((pieceToPromote == 'N') and (move.pawnPromotion == True)):
            self.board[move.dest_row][move.dest_col] = move.source[0] + pieceToPromote
        elif ((pieceToPromote == 'R') and (move.pawnPromotion == True)):
            self.board[move.dest_row][move.dest_col] = move.source[0] + pieceToPromote

        if (move.enpassant == 'True'):
            if (move.source[0] == "w"):
                self.board[3][move.dest_col] = "--"
            elif (move.source[0] == "b"):
                self.board[4][move.dest_col] = "--"

        if (move.castling == 'wqs'):
            self.board[7][3] = "wR"
            self.board[7][0] = "--"
        elif (move.castling == 'bqs'):
            self.board[0][3] = "bR"
            self.board[0][0] = "--"
        elif (move.castling == 'wks'):
            self.board[7][5] = "wR"
            self.board[7][7] = "--"
        elif (move.castling == 'bks'):
            self.board[0][5] = "wR"
            self.board[0][7] = "--"

    def undo(self):
        if (len(self.Log) != 0):
            move = self.Log.pop()
            self.board[move.source_row][move.source_col] = move.source
            self.board[move.dest_row][move.dest_col] = move.dest
            self.whiteTurn = not self.whiteTurn
            if(len(self.Log) != 0):
                self.lastMoveMade = self.Log[len(self.Log) - 1]
            else:
                self.lastMoveMade = None
            if ((move.source == "wK") and (self.castlingRights.whiteKingMoved == True)):
                self.castlingRights.whiteKingMovedAt.pop()
                if (len(self.castlingRights.whiteKingMovedAt) == 0):
                    self.castlingRights.whiteKingMoved = False
            elif ((move.source == "bK") and (self.castlingRights.blackKingMoved == True)):
                self.castlingRights.blackKingMovedAt.pop()
                if (len(self.castlingRights.blackKingMovedAt) == 0):
                    self.castlingRights.blackKingMoved = False
            elif ((move.source == "wR") and (self.castlingRights.whiteRightRookMoved == True) and (
                    move.source_col == 7)):
                self.castlingRights.whiteRightRookMovedAt.pop()
                if (len(self.castlingRights.whiteRightRookMovedAt) == 0):
                    self.castlingRights.whiteRightRookMoved = False
            elif ((move.source == "wR") and (self.castlingRights.whiteLeftRookMoved == True) and (
                    move.source_col == 0)):
                self.castlingRights.whiteLeftRookMovedAt.pop()
                if (len(self.castlingRights.whiteLeftRookMovedAt) == 0):
                    self.castlingRights.whiteLeftRookMoved = False
            elif ((move.source == "bR") and (self.castlingRights.blackRightRookMoved == True) and (
                    move.source_col == 7)):
                self.castlingRights.blackRightRookMovedAt.pop()
                if (len(self.castlingRights.blackRightRookMovedAt) == 0):
                    self.castlingRights.blackRightRookMoved = False
            elif ((move.source == "bR") and (self.castlingRights.blackLeftRookMoved == True) and (
                    move.source_col == 0)):
                self.castlingRights.blackLeftRookMovedAt.pop()
                if (len(self.castlingRights.blackLeftRookMovedAt) == 0):
                    self.castlingRights.blackLeftRookMoved = False

            if (move.source == "wK"):
                self.wKCord = (move.source_row, move.source_col)
            elif (move.source == "bK"):
                self.bKCord = (move.source_row, move.source_col)
            if (move.pawnPromotion == True):
                self.board[move.source_row][move.source_col] = move.source[0] + 'p'
            if (move.enpassant == 'True'):
                if (move.source[0] == "w"):
                    self.board[move.source_row][move.dest_col] = "bp"
                elif (move.source[0] == "b"):
                    self.board[move.source_row][move.dest_col] = "wp"

            if (move.castling == 'wqs'):
                self.board[7][0] = "wR"
                self.board[7][3] = "--"
            elif (move.castling == 'bqs'):
                self.board[0][0] = "bR"
                self.board[0][3] = "--"
            elif (move.castling == "wks"):
                self.board[7][7] = "wR"
                self.board[7][5] = "--"
            elif (move.castling == "bks"):
                self.board[0][7] = "bR"
                self.board[0][5] = "--"

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
        if (self.whiteTurn == True):
            if (self.CheckCastlingRights('wqs') == True):
                successors.append(Move((7, 4), (7, 2), self.board, castlingMove='wqs'))
            if (self.CheckCastlingRights('wks') == True):
                successors.append(Move((7, 4), (7, 6), self.board, castlingMove='wks'))
        else:
            if (self.CheckCastlingRights('bqs') == True):
                successors.append(Move((0, 4), (0, 2), self.board, castlingMove='bqs'))
            if (self.CheckCastlingRights('bks') == True):
                successors.append(Move((0, 4), (0, 6), self.board, castlingMove='bks'))
        for i in range(len(successors) - 1, -1, -1):
            self.move(successors[i])
            self.whiteTurn = not self.whiteTurn
            if (self.check() == True):
                successors.remove(successors[i])
            self.whiteTurn = not self.whiteTurn
            self.undo()
        if (len(successors) == 0):
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
                if (((self.whiteTurn == True) and (self.board[row][col][0] == 'w')) or (
                        (not self.whiteTurn == True) and (self.board[row][col][0] == 'b'))):
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
        if (self.whiteTurn == True):
            return self.pieceAttacked(self.wKCord[0], self.wKCord[1])
        else:
            return self.pieceAttacked(self.bKCord[0], self.bKCord[1])

    def pieceAttacked(self, row, col):
        self.whiteTurn = not self.whiteTurn
        oppSuccessors = self.getSuccessors()
        for succ in oppSuccessors:
            if (succ.dest_row == row and succ.dest_col == col):
                self.whiteTurn = not self.whiteTurn
                return True
        self.whiteTurn = not self.whiteTurn
        return False

    def getPawnSuccessors(self, row, col, successors):
        if ((self.whiteTurn == True) and (self.board[row][col][0] == 'w')):
            if (self.board[row - 1][col] == "--"):
                successors.append(Move((row, col), (row - 1, col), self.board))
                if (row == 6):
                    if (self.board[row - 2][col] == "--"):
                        successors.append(Move((row, col), (row - 2, col), self.board, 'False', True))
            if (col == 0 and self.board[row - 1][col + 1][0] == 'b'):
                successors.append(Move((row, col), (row - 1, col + 1), self.board))
            if (col == 7 and self.board[row - 1][col - 1][0] == 'b'):
                successors.append(Move((row, col), (row - 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row - 1][col - 1][0] == 'b'):
                successors.append(Move((row, col), (row - 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row - 1][col + 1][0] == 'b'):
                successors.append(Move((row, col), (row - 1, col + 1), self.board))
            if (self.lastMoveMade != None and self.lastMoveMade.doublePawnMove == True):
                if (row == 3 and col == 7 and self.lastMoveMade.source[0] == 'b'):
                    successors.append(Move((row, col), (row - 1, self.lastMoveMade.dest_col), self.board, 'True'))
                if (row == 3 and col == 0 and self.lastMoveMade.source[0] == 'b'):
                    successors.append(Move((row, col), (row - 1, self.lastMoveMade.dest_col), self.board, 'True'))
                if (row == 3 and self.lastMoveMade.source[0] == 'b'):
                    successors.append(Move((row, col), (row - 1, self.lastMoveMade.dest_col), self.board, 'True'))
        else:
            if (self.board[row + 1][col] == "--"):
                successors.append(Move((row, col), (row + 1, col), self.board))
                if (row == 1):
                    if (self.board[row + 2][col] == "--"):
                        successors.append(Move((row, col), (row + 2, col), self.board, 'False', True))
            if (col == 0 and self.board[row + 1][col + 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col + 1), self.board))
            if (col == 7 and self.board[row + 1][col - 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row + 1][col - 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col - 1), self.board))
            if (col != 0 and col != 7 and self.board[row + 1][col + 1][0] == 'w'):
                successors.append(Move((row, col), (row + 1, col + 1), self.board))
            if (self.lastMoveMade != None and self.lastMoveMade.doublePawnMove == True):
                if (row == 4 and col == 7 and self.lastMoveMade.source[0] == 'w'):
                    successors.append(Move((row, col), (row + 1, self.lastMoveMade.dest_col), self.board, 'True'))
                if (row == 4 and col == 0 and self.lastMoveMade.source[0] == 'w'):
                    successors.append(Move((row, col), (row + 1, self.lastMoveMade.dest_col), self.board, 'True'))
                if (row == 4 and self.lastMoveMade.source[0] == 'w'):
                    successors.append(Move((row, col), (row + 1, self.lastMoveMade.dest_col), self.board, 'True'))

    def getRookSuccessors(self, row, col, successors):
        for c in range(8):
            if (col + c == col):
                pass
            elif (col + c >= 8):
                break
            elif (self.board[row][col + c] == "--"):
                successors.append(Move((row, col), (row, col + c), self.board))
            elif (self.board[row][col + c][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row, col + c), self.board))
                    break
                else:
                    break
            elif (self.board[row][col + c][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row, col + c), self.board))
                    break
        for c in range(8):
            if (col - c == col):
                pass
            elif ((col - c) < 0):
                break
            elif (self.board[row][col - c] == "--"):
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
            if (row + r == row):
                pass
            elif ((row + r) >= 8):
                break
            elif (self.board[row + r][col] == "--"):
                successors.append(Move((row, col), (row + r, col), self.board))
            elif (self.board[row + r][col][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + r, col), self.board))
                    break
                else:
                    break
            elif (self.board[row + r][col][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + r, col), self.board))
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
        if (row - 2 < 0 or col - 1 < 0):
            pass
        elif (self.board[row - 2][col - 1] == "--"):
            successors.append(Move((row, col), (row - 2, col - 1), self.board))
        elif (self.board[row - 2][col - 1][0] == 'b'):
            if (self.whiteTurn == True):
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
            if (row + i == row and col + i == col):
                continue
            elif (row + i >= 8):
                break
            elif (col + i >= 8):
                break
            elif (self.board[row + i][col + i] == "--"):
                successors.append(Move((row, col), (row + i, col + i), self.board))
            elif (self.board[row + i][col + i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + i, col + i), self.board))
                    break
                else:
                    break
            elif (self.board[row + i][col + i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + i, col + i), self.board))
                    break
        for i in range(8):
            if (row - i == row and col + i == col):
                continue
            elif (row - i < 0):
                break
            elif (col + i >= 8):
                break
            elif (self.board[row - i][col + i] == "--"):
                successors.append(Move((row, col), (row - i, col + i), self.board))
            elif (self.board[row - i][col + i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row - i, col + i), self.board))
                    break
                else:
                    break
            elif (self.board[row - i][col + i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row - i, col + i), self.board))
                    break
        for i in range(8):
            if (row + i == row and col - i == col):
                continue
            elif (row + i >= 8):
                break
            elif (col - i < 0):
                break
            elif (self.board[row + i][col - i] == "--"):
                successors.append(Move((row, col), (row + i, col - i), self.board))
            elif (self.board[row + i][col - i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + i, col - i), self.board))
                    break
                else:
                    break
            elif (self.board[row + i][col - i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + i, col - i), self.board))
                    break
        for i in range(8):
            if (row - i == row and col - i == col):
                continue
            elif (row - i < 0):
                break
            elif (col - i < 0):
                break
            elif (self.board[row - i][col - i] == "--"):
                successors.append(Move((row, col), (row - i, col - i), self.board))
            elif (self.board[row - i][col - i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row - i, col - i), self.board))
                    break
                else:
                    break
            elif (self.board[row - i][col - i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row - i, col - i), self.board))
                    break

    def getKingSuccessors(self, row, col, successors):
        if (row + 1 > 7 or col + 1 > 7):
            pass
        elif (self.board[row + 1][col + 1] == "--"):
            successors.append(Move((row, col), (row + 1, col + 1), self.board))
        elif (self.board[row + 1][col + 1][0] == 'b'):
            if (self.whiteTurn == True):
                successors.append(Move((row, col), (row + 1, col + 1), self.board))
        elif (self.board[row + 1][col + 1][0] == 'w'):
            if (self.whiteTurn == True):
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
            if (row + i == row and col + i == col):
                continue
            elif (row + i >= 8):
                break
            elif (col + i >= 8):
                break
            elif (self.board[row + i][col + i] == "--"):
                successors.append(Move((row, col), (row + i, col + i), self.board))
            elif (self.board[row + i][col + i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + i, col + i), self.board))
                    break
                else:
                    break
            elif (self.board[row + i][col + i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + i, col + i), self.board))
                    break
        for i in range(8):
            if (row - i == row and col + i == col):
                continue
            elif (row - i < 0):
                break
            elif (col + i >= 8):
                break
            elif (self.board[row - i][col + i] == "--"):
                successors.append(Move((row, col), (row - i, col + i), self.board))
            elif (self.board[row - i][col + i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row - i, col + i), self.board))
                    break
                else:
                    break
            elif (self.board[row - i][col + i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row - i, col + i), self.board))
                    break
        for i in range(8):
            if (row + i == row and col - i == col):
                continue
            elif (row + i >= 8):
                break
            elif (col - i < 0):
                break
            elif (self.board[row + i][col - i] == "--"):
                successors.append(Move((row, col), (row + i, col - i), self.board))
            elif (self.board[row + i][col - i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + i, col - i), self.board))
                    break
                else:
                    break
            elif (self.board[row + i][col - i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + i, col - i), self.board))
                    break
        for i in range(8):
            if (row - i == row and col - i == col):
                continue
            elif (row - i < 0):
                break
            elif (col - i < 0):
                break
            elif (self.board[row - i][col - i] == "--"):
                successors.append(Move((row, col), (row - i, col - i), self.board))
            elif (self.board[row - i][col - i][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row - i, col - i), self.board))
                    break
                else:
                    break
            elif (self.board[row - i][col - i][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row - i, col - i), self.board))
                    break
        for c in range(8):
            if (col + c == col):
                pass
            elif (col + c >= 8):
                break
            elif (self.board[row][col + c] == "--"):
                successors.append(Move((row, col), (row, col + c), self.board))
            elif (self.board[row][col + c][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row, col + c), self.board))
                    break
                else:
                    break
            elif (self.board[row][col + c][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row, col + c), self.board))
                    break
        for c in range(8):
            if (col - c == col):
                pass
            elif ((col - c) < 0):
                break
            elif (self.board[row][col - c] == "--"):
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
            if (row + r == row):
                pass
            elif ((row + r) >= 8):
                break
            elif (self.board[row + r][col] == "--"):
                successors.append(Move((row, col), (row + r, col), self.board))
            elif (self.board[row + r][col][0] == 'b'):
                if (self.whiteTurn == True):
                    successors.append(Move((row, col), (row + r, col), self.board))
                    break
                else:
                    break
            elif (self.board[row + r][col][0] == 'w'):
                if (self.whiteTurn == True):
                    break
                else:
                    successors.append(Move((row, col), (row + r, col), self.board))
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

    def CastlingCheck(self, orientation):
        if (orientation == 'wqs'):
            if ((self.pieceAttacked(7, 4) == False) and (self.pieceAttacked(7, 3) == False) and (
                    self.pieceAttacked(7, 2) == False)):
                return True
        elif (orientation == 'bqs'):
            if ((self.pieceAttacked(0, 4) == False) and (self.pieceAttacked(0, 3) == False) and (
                    self.pieceAttacked(0, 2) == False)):
                return True
        elif (orientation == 'bks'):
            if ((self.pieceAttacked(0, 4) == False) and (self.pieceAttacked(0, 6) == False) and (
                    self.pieceAttacked(0, 5) == False)):
                return True
        elif (orientation == 'wks'):
            if ((self.pieceAttacked(7, 4) == False) and (self.pieceAttacked(7, 6) == False) and (
                    self.pieceAttacked(7, 5) == False)):
                return True
        else:
            return False

    def SpaceBetweenEmpty(self, orientation):
        if (orientation == 'wqs'):
            if ((self.board[7][3] == "--") and (self.board[7][2] == "--") and (self.board[7][1] == "--")):
                return True
        elif (orientation == 'bqs'):
            if ((self.board[0][3] == "--") and (self.board[0][2] == "--") and (self.board[0][1] == "--")):
                return True
        elif (orientation == 'wks'):
            if ((self.board[7][5] == "--") and (self.board[7][6] == "--")):
                return True
        elif (orientation == 'bks'):
            if ((self.board[0][5] == "--") and (self.board[0][6] == "--")):
                return True
        else:
            return False

    def CheckCastlingRights(self, orientation):
        if (orientation == 'wqs'):
            if ((self.castlingRights.whiteLeftRookMoved == False) and (
                    self.castlingRights.whiteKingMoved == False) and (self.SpaceBetweenEmpty(orientation) == True) and (
                    self.CastlingCheck(orientation) == True)):
                return True
        elif (orientation == 'bqs'):
            if ((self.castlingRights.blackLeftRookMoved == False) and (
                    self.castlingRights.blackKingMoved == False) and (self.SpaceBetweenEmpty(orientation) == True) and (
                    self.CastlingCheck(orientation) == True)):
                return True
        elif (orientation == 'wks'):
            if ((self.castlingRights.whiteRightRookMoved == False) and (
                    self.castlingRights.whiteKingMoved == False) and (self.SpaceBetweenEmpty(orientation) == True) and (
                    self.CastlingCheck(orientation) == True)):
                return True
        elif (orientation == 'bks'):
            if ((self.castlingRights.blackRightRookMoved == False) and (
                    self.castlingRights.blackKingMoved == False) and (self.SpaceBetweenEmpty(orientation) == True) and (
                    self.CastlingCheck(orientation) == True)):
                return True
        else:
            return False


class Move():

    def __init__(self, source, dest, board, enpassantPossible='False', doublePawn=False, castlingMove=None):
        self.source_row = source[0]
        self.source_col = source[1]
        self.dest_row = dest[0]
        self.dest_col = dest[1]
        self.source = board[self.source_row][self.source_col]
        self.dest = board[self.dest_row][self.dest_col]
        self.pawnPromotion = False
        self.doublePawnMove = doublePawn
        if ((self.source == 'wp' and self.dest_row == 0) or (self.source == 'bp' and self.dest_row == 7)):
            self.pawnPromotion = True
        self.enpassant = enpassantPossible
        self.castling = castlingMove
        self.ID = self.source_row * 1000 + self.dest_row * 100 + self.source_col * 10 + self.dest_col

    '''
    Equals method that has been overrode
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.ID == other.ID
        return False

    def getPawnPromotion(self):
        return self.pawnPromotion


class Castling():

    def __init__(self):
        self.whiteKingMoved = False
        self.blackKingMoved = False
        self.whiteLeftRookMoved = False
        self.whiteRightRookMoved = False
        self.blackLeftRookMoved = False
        self.blackRightRookMoved = False
        self.whiteKingMovedAt = []
        self.blackKingMovedAt = []
        self.whiteLeftRookMovedAt = []
        self.whiteRightRookMovedAt = []
        self.blackLeftRookMovedAt = []
        self.blackRightRookMovedAt = []
