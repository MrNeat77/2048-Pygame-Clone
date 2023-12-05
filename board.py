from piece import Piece
import random as r

class Board():
    def __init__(self, size):
        self.size = size
        # Set of instructions to take a direction and construct a for loop sequence
        self.sequenceDict = {
                    'L' : (0, self.size, 1, 1, 0, True),
                    'U' : (0, self.size, 1, 0, 1, False),
                    'R' : (self.size - 1 , -1, -1, -1, 0, True),
                    'D' : (self.size - 1, -1, -1, 0, -1, False)}
        self.setBoard()

    def setBoard(self):        
        self.board = [[Piece() for i in range(self.size)] for j in range(self.size)]
        self.addPiece()

    # Generates a 2 or 4 piece at a random position
    def addPiece(self):
        while True:
            row, col = r.randint(0, self.size-1), r.randint(0, self.size-1)
            newPiece = self.board[row][col].getVal()
            if newPiece != 0:
                continue
            self.board[row][col].setVal(r.randint(1, 2)) 
            break    

    def getSize(self):
        return self.size
    
    def getPiece(self, index):
        return self.board[index[0]][index[1]]
    
    def comparePiece(self, staticPiece, movePiece):
        # Ignore when the moveable piece is 0 (no need to move empty space)
        if movePiece == 0:
            return 0
        # Swap static empty space with any non 0 value
        elif staticPiece == 0:
            return 1
        # Combine any equal and non 0 pieces 
        elif movePiece == staticPiece and (movePiece + staticPiece) != 0:
            return 2
        # Ignore any unequal pieces
        elif movePiece != staticPiece:
            return 0
        
        '''Summary of Logical flow:
        if movePiece is 0, then skip because we dont move empty space,
        if staticPiece is 0 then we swap it with the move piece since it must have a value,
        if the pieces are equal value then combine them,
        and finally if they are unequal non zero values (not swapable or combinable) then ignore them (needed for game over)'''
        
    def move(self, directionKey):

        IGNORE = 0
        SWAP = 1
        COMBINE = 2

        '''The following dictionary acts as a set of instructions to construct a sequence
        when given a directional key.
        The key is a direction, given as a one letter string representing "Left", "Right", "Up", and "Down".
        Value index 0 is for the beginning of the loop, 1 is for the end, and 2 is the step/ direction,
        3 and 4 are for the modifier that is for comparing the original and modified coordinates, and
        finally 5 is a bool that swaps the inner and outer iterators to effectually invert the iteration order,
        e.g. Rows first -> then Columns or Columns -> then Rows'''

        
        # This is a technically unecessary intermediate step, however it is more readable as it unpacks the dict into variables
        seq = self.sequenceDict[directionKey]
        sMin, sMax, sStep = seq[0], seq[1], seq[2]
        iMod, jMod, isInverse = seq[3], seq[4], seq[5]
        

        isFinished = False
        isFirst = True

        # Repeats sequence until all available moves are exhausted 
        while not isFinished:
            isFinished = True

            # Loop iterates through 2D list, but direction depends on sequence instruction variables
            for outer in range(sMin, sMax, sStep):
                for inner in range(sMin, sMax, sStep):
                    if isInverse:
                        i, j = inner, outer
                    else:
                        i, j = outer, inner

                    # Does not compare values that are out of range (non existent)
                    if ((i + iMod < 0) or (j + jMod < 0) or (i + iMod > self.size-1) or (j + jMod > self.size-1)):
                        continue

                    # Comparison logic mainly from comparePiece() method
                    if self.comparePiece(self.board[i][j].getVal(), self.board[i + iMod][j + jMod].getVal()) == IGNORE:
                        continue
                    elif self.comparePiece(self.board[i][j].getVal(), self.board[i + iMod][j + jMod].getVal()) == SWAP:
                        self.board[i][j], self.board[i + iMod][j + jMod] = self.board[i + iMod][j + jMod], self.board[i][j]
                        isFinished = False
                    elif self.comparePiece(self.board[i][j].getVal(), self.board[i + iMod][j + jMod].getVal()) == COMBINE:
                        self.board[i][j].setVal(self.board[i][j].getVal()+1)
                        self.board[i + iMod][j + jMod].setVal(0)
                        isFinished = False

            # Won't add piece if no actual move was made (if all pieces ignored on first pass by sequencer then no random piece)
            if isFirst:
                isFirst = False
                if isFinished:
                    return                
        self.addPiece()
    
    def checkAvailableMoves(self):

        '''This is like the move() method, but it takes no argument and instead runs through every move.
        It also only makes comparisons, and does not modify the board.'''        
        for directionKey in self.sequenceDict:
            seq = self.sequenceDict[directionKey]
            sMin, sMax, sStep = seq[0], seq[1], seq[2]
            iMod, jMod, isInverse = seq[3], seq[4], seq[5]

            for outer in range(sMin, sMax, sStep):
                for inner in range(sMin, sMax, sStep):
                    if isInverse:
                        i, j = inner, outer
                    else:
                        i, j = outer, inner

                    # Does not compare values that are out of range (non existent)
                    if ((i + iMod < 0) or (j + jMod < 0) or (i + iMod > self.size-1) or (j + jMod > self.size-1)):
                        continue

                    # Comparison logic mainly from comparePiece() method
                    if self.comparePiece(self.board[i][j].getVal(), self.board[i + iMod][j + jMod].getVal()) != 0:
                        return True
        return False
