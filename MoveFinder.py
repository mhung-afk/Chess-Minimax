from copy import deepcopy
import random

pieceScore = {'k': 500, 'q': 9, 'r': 5, 'n': 3, 'b': 3, 'p': 1}
CHECKMATE = 1000
DRAW = 0


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findRandomPromote():
    return ['q', 'n', 'r', 'b'][random.randint(0, 3)]


def findBestMove(gs, validMoves):
    turn = 1 if gs.whiteToMove else -1
    opponentMinimaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        local_gs = deepcopy(gs)
        local_gs.makeMove(playerMove)
        opponentMoves = local_gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentMove in opponentMoves:
            slocal_gs = deepcopy(local_gs)
            slocal_gs.makeMove(opponentMove)
            if slocal_gs.checkmate:
                score = -turn * CHECKMATE
            elif slocal_gs.draw:
                score = DRAW
            else:
                score = -turn * scoreMaterial(slocal_gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
        if opponentMinimaxScore > opponentMaxScore:
            opponentMinimaxScore = opponentMaxScore
            bestPlayerMove = playerMove
    return bestPlayerMove


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[1] == 'b':
                score -= pieceScore[square[1]]
    return score
