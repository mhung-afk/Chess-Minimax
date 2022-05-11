import random

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findRandomPromote():
    return ['q','n','r','b'][random.randint(0,3)]