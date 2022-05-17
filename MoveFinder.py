from copy import deepcopy
import random

from constraint import *

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findRandomPromote(promoteTo = None):
    return ['q', 'n', 'r', 'b'][random.randint(0, 3)] if promoteTo is None else promoteTo


def scoreBoard(gs):
    # print(gs.whiteToMove)
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piecePositionScore = 0
            square = gs.board[row][col]
            # if square != '--':
            #     if square[1] == 'p':
            #         piecePositionScore = PIECE_POSITIONS_SCORE['wp' if square[0] == 'w' else 'bp'][row][col] * WEIGHT_SCORE['p']
            #     elif square[1] != 'k':
            #         piecePositionScore = PIECE_POSITIONS_SCORE[square[1]][row][col] * WEIGHT_SCORE[square[1]]
            #     if square[0] == 'w':
            #         score += PIECESCORE[square[1]] + piecePositionScore
            #     elif square[0] == 'b':
            #         score -= PIECESCORE[square[1]] + piecePositionScore
            if square == '--':
                continue
            if not gs.whiteToMove and square[0]=='w':
                if square[1] == 'p':
                    piecePositionScore = PIECE_POSITIONS_SCORE['wp'][row][col] * WEIGHT_SCORE['p']
                elif square[1] != 'k':
                    piecePositionScore = PIECE_POSITIONS_SCORE[square[1]][row][col] * WEIGHT_SCORE[square[1]]
                score += PIECESCORE[square[1]] + piecePositionScore
            elif gs.whiteToMove and square[0]=='b':
                if square[1] == 'p':
                    piecePositionScore = PIECE_POSITIONS_SCORE['bp'][row][col] * WEIGHT_SCORE['p']
                elif square[1] != 'k':
                    piecePositionScore = PIECE_POSITIONS_SCORE[square[1]][row][col] * WEIGHT_SCORE[square[1]]
                score -= PIECESCORE[square[1]] + piecePositionScore
    return score


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinimax(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove


def findMoveMinimax(gs, validMoves, depth, alpha, beta, turn):
    # print(alpha,beta)
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        if move.isPromote:
            move.promoteTo = findRandomPromote('q')
        local_gs = deepcopy(gs)
        local_gs.makeMove(move)
        nextMoves = local_gs.getValidMoves()
        score = - findMoveMinimax(local_gs, nextMoves, depth-1, -beta, -alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        # gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore