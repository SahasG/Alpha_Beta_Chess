from Alpha_Beta_Chess import Chess_State
import pygame as game

game.init()
WIDTH = HEIGHT = 512
DIM = 8
SQ = HEIGHT // DIM
IMAGES = {}
FPS = 30

def loadImages():
    image_pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in image_pieces:
        IMAGES[piece] = game.image.load("Alpha_Beta_Chess/images/" + piece + ".png")

def draw(screen, state):
    drawBoard(screen)
    drawChessPieces(screen, state.board)

def drawBoard(screen):
    colors = [game.Color(200, 190, 140), game.Color(100, 40, 0)]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[((r+c)%2)]
            game.draw.rect(screen, color, game.Rect(c*SQ, r*SQ, SQ, SQ))

def drawChessPieces(screen, board):
    for r in range(DIM):
        for c in range(DIM):
            chessPiece = board[r][c]
            if(chessPiece != "--"):
                screen.blit(IMAGES[chessPiece], game.Rect(c*SQ, r*SQ, SQ, SQ))

def main():
    screen = game.display.set_mode((WIDTH, HEIGHT))
    clock = game.time.Clock()
    screen.fill(game.Color("white"))
    state = Chess_State.Game()
    loadImages()
    print(state.board)
    running = True
    while running == True:
        for event in game.event.get():
            if event.type == game.QUIT:
                running = False
        draw(screen, state)
        clock.tick(FPS)
        game.display.flip()

if __name__ == "__main__":
    main()