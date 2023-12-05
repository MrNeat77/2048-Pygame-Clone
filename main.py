from game import Game
from board import Board

'''create necessary objects'''
size = 4
board = Board(size)
screenSize = (size * 128, size * 128)
game = Game(board, screenSize)

game.run()