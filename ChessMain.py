# handle user interaction

import sys
from time import sleep
import pygame as p
import ChessEngine
import MoveFinder
from constraint import *


def loadImages():
    pieces = ['wp','bp','wr','br','wn','bn','wb','bb','wq','bq','wk','bk']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))

def loadLargeImage():
    pieces = ['wr','bn','wb','bq']
    for piece in pieces:
        LARGE_IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (2*SQ_SIZE,2*SQ_SIZE))


def main(mode = 0, firstTurn = True):
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    gameOver = False
    firstTurnForPlayer = firstTurn # Player will have the first turn

    loadImages()
    loadLargeImage()

    running = True
    sqSelected = () # tuple (row, col)
    playerClicks = [] # list of 2 tuples: [(start_row, start_col), (end_row, end_col)]
    while running:
        if mode == 1 and not gameOver:
            playerTurn = firstTurnForPlayer == gs.whiteToMove
            # Player move
            if playerTurn:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        col = int(location[0]/SQ_SIZE)
                        row = int(location[1]/SQ_SIZE)
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks += [sqSelected]
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            lstMoves = [v for v in validMoves if v == move]
                            if len(lstMoves) == 1:
                                move = lstMoves[0]
                            if move in validMoves:
                                if move.isPromote: # pawn promote
                                    piece = ''
                                    srunning = True
                                    drawPromoteSelection(p, screen)
                                    drawGameState(screen, gs, validMoves, ())
                                    drawText(screen, 'Promote!')
                                    p.display.flip()
                                    while srunning:
                                        for se in p.event.get():
                                            if se.type == p.QUIT:
                                                srunning = False
                                                running = False
                                            elif se.type == p.MOUSEBUTTONDOWN:
                                                location = p.mouse.get_pos()
                                                pieceSelected = int(location[0]/(2*SQ_SIZE))
                                                if location[1] < DIMENSION*SQ_SIZE:
                                                    break
                                                else:
                                                    srunning = False
                                                    if pieceSelected == 0:
                                                        piece = 'q'
                                                    elif pieceSelected == 1:
                                                        piece = 'r'
                                                    elif pieceSelected == 2:
                                                        piece = 'n'
                                                    elif pieceSelected == 3:
                                                        piece = 'b'
                                    screen = p.display.set_mode((WIDTH,HEIGHT))
                                    move.promoteTo = piece
                                gs.makeMove(move)
                                print(move.getChessNotation())
                                moveMade =True
                                sqSelected = ()
                                playerClicks = []
                            else:
                                playerClicks = [sqSelected]
            else:
                AImove = MoveFinder.findBestMove(gs, validMoves)
                if AImove is None:
                    AImove = MoveFinder.findRandomMove(validMoves)
                if AImove.isPromote:
                    AImove.promoteTo = MoveFinder.findRandomPromote()
                gs.makeMove(AImove)
                print(AImove.getChessNotation())
                moveMade =True
        elif mode == 0 and not gameOver:
            minimaxTurn = firstTurnForPlayer == gs.whiteToMove
            # Minimax Agent move
            if minimaxTurn:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                minimaxMove = MoveFinder.findBestMove(gs, validMoves)
                if minimaxMove is None:
                    minimaxMove = MoveFinder.findRandomMove(validMoves)
                if minimaxMove.isPromote:
                    minimaxMove.promoteTo = MoveFinder.findRandomPromote()
                gs.makeMove(minimaxMove)
                print(minimaxMove.getChessNotation())
                moveMade =True
            
            # Random Agent move
            else:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                AImove = MoveFinder.findRandomMove(validMoves)
                if AImove.isPromote:
                    AImove.promoteTo = MoveFinder.findRandomPromote()
                gs.makeMove(AImove)
                print(AImove.getChessNotation())
                moveMade =True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, validMoves, sqSelected)
        if len(validMoves) == 0:
            gameOver = True
            running = False
            if gs.checkMate:
                drawText(screen, ('Black' if gs.whiteToMove else 'White') + ' wins!!!')
            else:
                drawText(screen, 'Draw!!!')
            
        clock.tick(MAX_FPS)
        p.display.flip()
        while gameOver:
            for e in p.event.get():
                if e.type == p.QUIT:
                    exit()

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSqSelected(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPromoteSelection(p, screen):
    screen = p.display.set_mode((WIDTH,HEIGHT+2*SQ_SIZE))
    colors = [p.Color('white'), p.Color('black')]
    for c in range(int(DIMENSION/2)):
        color = colors[c%2]
        p.draw.rect(screen, color, p.Rect(c*2*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['bq'], p.Rect(0, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['wr'], p.Rect(2*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['bn'], p.Rect(4*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['wb'], p.Rect(6*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))

def highlightSqSelected(screen, gs, validMoves, sqSelected):
    if sqSelected!=():
        r,c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(80)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE,r*SQ_SIZE))

            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObj = font.render(text, 0, p.Color('black'))
    textLoc = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    screen.blit(textObj, textLoc)
    print(text)

if __name__ == "__main__":
    main(int(sys.argv[1]), not bool(int(sys.argv[2])))