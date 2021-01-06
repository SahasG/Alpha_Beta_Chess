from Alpha_Beta_Chess import Chess_State
from Alpha_Beta_Chess import Chess_Player
import pygame as game

game.init()
WIDTH = HEIGHT = 512
DIM = 8
SQ = HEIGHT // DIM
IMAGES = {}
Frames = 30

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
    AIplayer = Chess_Player.Chess_Player()
    validSuccessors = state.getSuccessors()
    moveMade = False
    loadImages()
    clickLogs = []
    lastSQClick = ()
    gameType = raw_input("Play against AI: ")
    if(gameType == 'Yes' or gameType == 'YES'):
        running = True
        while running == True:
            for event in game.event.get():
                if(event.type == game.QUIT):
                    running = False
                elif(event.type == game.MOUSEBUTTONDOWN):
                    if(AIplayer.my_color == 'w' and state.whiteTurn == False) or (AIplayer.my_color == 'b' and state.whiteTurn == True):
                        cords = game.mouse.get_pos()
                        col = cords[0]//SQ
                        row = cords[1]//SQ
                        if(lastSQClick == (row, col)):
                            lastSQClick = ()
                            clickLogs = []
                        else:
                            lastSQClick = (row, col)
                            clickLogs.append(lastSQClick)
                        if(len(clickLogs) == 2):
                            move = Chess_State.Move(clickLogs[0], clickLogs[1], state.board)
                            for i in range(len(validSuccessors)):
                                if (move == validSuccessors[i]):
                                    if(validSuccessors[i].getPawnPromotion() == True):
                                        looking = True
                                        while looking == True:
                                            for event in game.event.get():
                                                if(event.type == game.KEYDOWN):
                                                    if(event.key == game.K_q):
                                                        state.move(validSuccessors[i], 'Q')
                                                        moveMade = True
                                                        clickLogs = []
                                                        lastSQClick = ()
                                                        looking = False
                                                    elif(event.key == game.K_n):
                                                        state.move(validSuccessors[i], 'N')
                                                        moveMade = True
                                                        clickLogs = []
                                                        lastSQClick = ()
                                                        looking = False
                                                    elif(event.key == game.K_r):
                                                        state.move(validSuccessors[i], 'R')
                                                        moveMade = True
                                                        clickLogs = []
                                                        lastSQClick = ()
                                                        looking = False
                                                    elif(event.key == game.K_b):
                                                        state.move(validSuccessors[i], 'B')
                                                        moveMade = True
                                                        clickLogs = []
                                                        lastSQClick = ()
                                                        looking = False
                                    else:
                                        state.move(validSuccessors[i])
                                        moveMade = True
                                        clickLogs = []
                                        lastSQClick = ()
                            if moveMade == False:
                                clickLogs = [lastSQClick]
                    else:
                        AImove = AIplayer.make_move(state)
                        state.move(AImove)
                        moveMade = True
                        clickLogs = []
                        lastSQClick = ()

                elif(event.type == game.KEYDOWN):
                    if(event.key == game.K_u):
                        state.undo()
                        moveMade = True
            if moveMade:
                validSuccessors = state.getValidSuccessors()
                moveMade = False

            draw(screen, state)
            clock.tick(Frames)
            game.display.flip()
    else:
        running = True
        while running == True:
            for event in game.event.get():
                if (event.type == game.QUIT):
                    running = False
                elif (event.type == game.MOUSEBUTTONDOWN):
                    cords = game.mouse.get_pos()
                    col = cords[0] // SQ
                    row = cords[1] // SQ
                    if (lastSQClick == (row, col)):
                        lastSQClick = ()
                        clickLogs = []
                    else:
                        lastSQClick = (row, col)
                        clickLogs.append(lastSQClick)
                    if (len(clickLogs) == 2):
                        move = Chess_State.Move(clickLogs[0], clickLogs[1], state.board)
                        for i in range(len(validSuccessors)):
                            if (move == validSuccessors[i]):
                                if (validSuccessors[i].getPawnPromotion() == True):
                                    looking = True
                                    while looking == True:
                                        for event in game.event.get():
                                            if (event.type == game.KEYDOWN):
                                                if (event.key == game.K_q):
                                                    state.move(validSuccessors[i], 'Q')
                                                    moveMade = True
                                                    clickLogs = []
                                                    lastSQClick = ()
                                                    looking = False
                                                elif (event.key == game.K_n):
                                                    state.move(validSuccessors[i], 'N')
                                                    moveMade = True
                                                    clickLogs = []
                                                    lastSQClick = ()
                                                    looking = False
                                                elif (event.key == game.K_r):
                                                    state.move(validSuccessors[i], 'R')
                                                    moveMade = True
                                                    clickLogs = []
                                                    lastSQClick = ()
                                                    looking = False
                                                elif (event.key == game.K_b):
                                                    state.move(validSuccessors[i], 'B')
                                                    moveMade = True
                                                    clickLogs = []
                                                    lastSQClick = ()
                                                    looking = False
                                else:
                                    state.move(validSuccessors[i])
                                    moveMade = True
                                    clickLogs = []
                                    lastSQClick = ()
                        if moveMade == False:
                            clickLogs = [lastSQClick]
                elif (event.type == game.KEYDOWN):
                    if (event.key == game.K_u):
                        state.undo()
                        moveMade = True
            if moveMade:
                validSuccessors = state.getValidSuccessors()
                moveMade = False
            draw(screen, state)
            clock.tick(Frames)
            game.display.flip()

if __name__ == "__main__":
    main()