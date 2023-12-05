import pygame, os, sys

os.chdir('C:\\MyPrograms\\Python\\PyGames\\2048')

'''The game object runs the main game loop and coordinates player interaction with the other objects.
It also handles loading and displaying images'''
class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.gameOver = False
        self.loadTiles('tile sheet1.png', 128)

    '''run() method initializes pygame, creates/updates the screen, and runs the game loop (very important).
    Also contains win condition, and handles key events like quitting, WASD, and arrow keys.'''

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption('2048')
        
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    self.handleKey(keys)

            self.gameOver = self.checkGameOver()

            if self.gameOver == 'WIN':
                pygame.display.set_caption('You won!!!')
            elif self.gameOver == 'LOSE':
                pygame.display.set_caption('GAME OVER')

            self.draw()
            pygame.display.flip()
             
    # Creates a grid of images by assigning a tile to a value at a given position, and displaying it at the position * the pixel size 
    # which offsets after each tile
    def draw(self):
        pos = (0, 0)
        for row in range(self.board.getSize()):
            for col in range(self.board.getSize()):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, (row*self.size, col*self.size))
                pos = pos[0] + self.size,  pos[1]
            pos = pos[0], pos[1] + self.size
            
    '''Saves a list of tiles from tile sheet file
    The number displayed by the tile directly corresponds as 2^(index of tile list)
    for example self.images[3] is the image for 8'''
    
    def loadTiles(self, file, size):
        self.size = size
        self.images = []
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        w, h = self.rect.size
        for i in range(0, w, self.size):
            for j in range(0, h, self.size):
                tile = pygame.Surface((self.size, self.size))
                tile.blit(self.image, (0,0), (i, j, self.size, self.size))
                self.images.append(tile)

    # Not yet used
    def loadBg(self, file):
        self.images = []

    def getImage(self, piece):
        return self.images[piece.getVal()]

    # Passes key press and return single character. Only 8 keys are supported (2 per direction)
    def handleKey(self, keys):
        try: 
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction = 'L'
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction = 'R'
            elif keys[pygame.K_w] or keys[pygame.K_UP]:
                direction = 'U'
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction = 'D'
                
            self.board.move(direction)
        except:
            pass
        
    # Evaluate win/loss condition 
    def checkGameOver(self):
        for row in range(self.board.getSize()):
            for col in range(self.board.getSize()):
                piece = self.board.getPiece((row, col))
                # Check for 2048
                if piece.getVal() == 11:
                    return 'WIN'
                # Game continues if there is any 0 value
                elif piece.getVal()== 0:
                    return False
        # Game over when there is no 0 values
        # Check if there are no possible moves somehow
        if not self.board.checkAvailableMoves():
            return 'LOSE'
            