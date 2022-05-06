# handle rules, valid move, log move

from constrant import *


class GameState:
    def __init__(self):
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        self.moveFuctions = {'p': self.getPawnMoves, 'r': self.getRookMoves, 'n': self.getKnightMoves,
                             'b': self.getBishopMoves, 'q': self.getQueenMoves, 'k': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog += [move]
        self.whiteToMove = not self.whiteToMove

    # check checkmate, draw move, error move
    def getValidMoves(self):
        return self.getAllPossibleMove()  # don't check

    def getAllPossibleMove(self):
        moves = [] # list of move object, example: Move((6,4), (4,4), self.board)
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFuctions[piece](r, c, moves)
        return moves

    # append to list moves for each piece
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if r >= 1:
                if self.board[r-1][c] == '--':  # pawn move one square
                    moves += [Move((r, c), (r-1, c), self.board)]
                    if r == 6 and self.board[r-2][c] == '--':
                        moves += [Move((r, c), (r-2, c), self.board)]

                # capture an enemy piece
                if c >= 1 and self.board[r-1][c-1][0] == 'b':
                    moves += [Move((r, c), (r-1, c-1), self.board)]
                # capture an enemy piece
                if c <= 6 and self.board[r-1][c+1][0] == 'b':
                    moves += [Move((r, c), (r-1, c+1), self.board)]
            elif r == 0:  # promote white pawn
                pass
        else:
            if r <= 6:
                if self.board[r+1][c] == '--':  # pawn move one square
                    moves += [Move((r, c), (r+1, c), self.board)]
                    if r == 1 and self.board[r+2][c] == '--':
                        moves += [Move((r, c), (r+2, c), self.board)]

                # capture an enemy piece
                if c >= 1 and self.board[r+1][c-1][0] == 'w':
                    moves += [Move((r, c), (r+1, c-1), self.board)]
                # capture an enemy piece
                if c <= 6 and self.board[r+1][c+1][0] == 'w':
                    moves += [Move((r, c), (r+1, c+1), self.board)]
            elif r == 7:  # promote black pawn
                pass

    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range (8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0<= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))
                    


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def __eq__(self, other):
        return self.startRow == other.startRow and self.startCol == other.startCol and self.endRow == other.endRow and self.endCol == other.endCol

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + ' - ' + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
