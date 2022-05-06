# handle user interaction

import pygame as p
import ChessEngine
from constrant import *


def loadImages():
    pieces = ['wp','bp','wr','br','wn','bn','wb','bb','wq','bq','wk','bk']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()

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
                if sqSelected == (row, col) or (gs.board[row][col] == '--' and sqSelected == ()):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks += [sqSelected]
                if len(playerClicks) == 2:
                    if gs.board[row][col][0] == gs.board[playerClicks[0][0]][playerClicks[0][1]][0]:
                        playerClicks = playerClicks[1:]
                        continue
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        print(move.getChessNotation())
                        moveMade =True
                    sqSelected = ()
                    playerClicks = []

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

if __name__ == "__main__":
    main()