# handle user interaction

import pygame as p
import ChessEngine
from constrant import *


def loadImages():
    pieces = ['wp','bp','wr','br','wn','bn','wb','bb','wq','bq','wk','bk']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))

def loadLargeImage():
    pieces = ['wr','bn','wb','bq']
    for piece in pieces:
        LARGE_IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (2*SQ_SIZE,2*SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    loadLargeImage()

    running = True
    sqSelected = () # tuple (row, col)
    playerClicks = [] # list of 2 tuples: [(start_row, start_col), (end_row, end_col)]
    while running:
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
                    if move in validMoves:
                        if move.isPromote: # pawn promote
                            piece = ''
                            srunning = True
                            drawPromoteSelection(p, screen)
                            drawGameState(screen, gs)
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

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
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

if __name__ == "__main__":
    main()