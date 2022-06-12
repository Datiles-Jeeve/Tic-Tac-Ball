import numpy as np
import random
import sys
import math
import pygame
from button import Button
from pygame import mixer

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TicTac Ball")

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)


pygame.mixer.music.load('audio/main.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


clock = pygame.time.Clock()
FPS = 60

BG = pygame.image.load("assets/bg.png")
GB = pygame.image.load("assets/Background.png")


def get_font(size):  
    return pygame.font.Font("assets/burbank.otf", size)   
def frostbite(size):
    return pygame.font.Font("assets/frosbite_b.ttf", size)




frostbite_n = pygame.font.Font("assets/frostbite_n.ttf", 20) 
frostbite_w = pygame.font.Font("assets/frostbite_w.ttf", 20)   
frostbite_wb = pygame.font.Font("assets/frostbite_wb.ttf", 55)
smallFont = pygame.font.Font("assets/burbank.otf", 25)
medFont = pygame.font.Font("assets/burb.ttf", 40)
largeFont = pygame.font.Font("assets/burbank.otf", 100)
font = pygame.font.SysFont("none", 30)
myfont = pygame.font.SysFont("none", 25)
my_font = pygame.font.SysFont("monospace", 14)
f_ont = pygame.font.SysFont("none", 45)


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    elif size == "frostbite_":
        textSurface = frostbite_wb.render(text, True, color)    
    elif size == "frost_":
        textSurface = f_ont.render(text, True, color)      
    return textSurface, textSurface.get_rect()



def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(SCREEN_WIDTH/2.3), (int(SCREEN_HEIGHT / 2.1) + y_displace))
    SCREEN.blit(textSurf, textRect)



def play():
    pause = False
    while True:

        BLUE = (0, 0, 255)
        WHITE = (255, 255, 25)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)
        gray = (206, 212, 218)
        ORANGE = (202, 103, 2)

        ROW_COUNT = 6
        COLUMN_COUNT = 7

        def create_board():
            board = np.zeros((ROW_COUNT,COLUMN_COUNT))
            return board

        def drop_piece(board, row, col, piece):
            board[row][col] = piece

        def is_valid_location(board, col):
            return board[ROW_COUNT-1][col] == 0

        def get_next_open_row(board, col):
            for r in range(ROW_COUNT):
                if board[r][col] == 0:
                    return r

        def print_board(board):
            print(np.flip(board, 0))

        def winning_move(board, piece):
            # Check horizontal locations for win
            for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        return True

            # Check vertical locations for win
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True

            # Check negatively sloped diaganols
            for c in range(COLUMN_COUNT-3):
                for r in range(3, ROW_COUNT):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True

        def draw_board(board):
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):
                    pygame.draw.rect(screen, white, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.circle(screen, "#000814", (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):		
                    if board[r][c] == 1:
                        pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                    elif board[r][c] == 2: 
                        pygame.draw.circle(screen, green, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            player = mixer.Sound('audio/sound.mp3')
            player.play()
            player.set_volume(0.2)
            pygame.display.update()


        board = create_board()
        print_board(board)
        game_over = False
        turn = 0

        pygame.init()

        SQUARESIZE = 100

        width = COLUMN_COUNT * SQUARESIZE
        height = (ROW_COUNT+1) * SQUARESIZE

        size = (width, height)

        RADIUS = int(SQUARESIZE/2 - 5)

        screen = pygame.display.set_mode(size)
        draw_board(board)
        pygame.display.update()

        

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, "#000814", (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(screen, green, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = True
                        while paused:  
                            SCREEN.fill("#000814")
                            message_to_screen("Paused", white, -100, size = "frostbite_")
                            message_to_screen("Press C to continue or Q to Quit", white, size = "frost_")
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_c:
                                        paused = False
                                        pygame.display.update()
                                        clock.tick
                                        draw_board(board)
                                        pygame.draw.rect(screen, "#000814", (0, 0, width, SQUARESIZE))  
                                    elif event.key == pygame.K_q:
                                        pygame.quit()
                                        quit()

                                pygame.display.update()
                                clock.tick

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, "#000814", (0,0, width, SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if winning_move(board, 1):
                                label = frostbite(35).render("Player 1 wins!!", True, white)
                                screen.blit(label, (220, 30))
                                game_over = True


                    # # Ask for Player 2 Input
                    else:				
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            if winning_move(board, 2):
                                label = frostbite(35).render("Player 2 wins!!", True, white)
                                screen.blit(label, (220, 30))
                                game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        pygame.time.wait(3000)


def instructions():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = medFont.render("How to Play Tic Tac Ball | Rules of Tic Tac Ball.", True, "#ca6702")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTION_TEXT = smallFont.render("OBJECTIVES:", True, "Black")
        OPTION_RECT = OPTION_TEXT.get_rect(center=(110, 130))
        SCREEN.blit(OPTION_TEXT, OPTION_RECT)

        OPT_TEXT = my_font.render ("To be the first player to connect 4 of the same colored discs in a row (either", True, "Black")
        OPT_RECT = OPT_TEXT.get_rect(center=(375, 165))
        SCREEN.blit(OPT_TEXT, OPT_RECT)

        OPT1_TEXT = my_font.render ("vertically, horizontally, or diagonally).", True, "Black")
        OPT1_RECT = OPT1_TEXT.get_rect(center=(227, 185))
        SCREEN.blit(OPT1_TEXT, OPT1_RECT)

        OPT2_TEXT = smallFont.render("HOW TO PLAY:", True, "Black")
        OPT2_RECT = OPT2_TEXT.get_rect(center=(115, 245))
        SCREEN.blit(OPT2_TEXT, OPT2_RECT)

        OPT3_TEXT = my_font.render ("- First, decide who goes first and what color each player will have.", True, "Black")
        OPT3_RECT = OPT3_TEXT.get_rect(center=(335, 280))
        SCREEN.blit(OPT3_TEXT, OPT3_RECT)

        OPT4_TEXT = my_font.render ("- Players must alternate turns, and only one ball can be dropped in each turn. ", True, "Black")
        OPT4_RECT = OPT4_TEXT.get_rect(center=(377, 305))
        SCREEN.blit(OPT4_TEXT, OPT4_RECT)

        OPT5_TEXT = my_font.render ("- On your turn, drop one of your colored balls from the top into any of the seven slots. ", True, "Black")
        OPT5_RECT = OPT5_TEXT.get_rect(center=(418, 330))
        SCREEN.blit(OPT5_TEXT, OPT5_RECT)

        OPT6_TEXT = my_font.render ("- The game ends when there is a 4-in-a-row or a stalemate. ", True, "Black")
        OPT6_RECT = OPT6_TEXT.get_rect(center=(299, 355))
        SCREEN.blit(OPT6_TEXT, OPT6_RECT)

        OPT7_TEXT = my_font.render ("- The starter of the previous game goes second on the next game. ", True, "Black")
        OPT7_RECT = OPT7_TEXT.get_rect(center=(322, 375))
        SCREEN.blit(OPT7_TEXT, OPT7_RECT)


        OPTIONS_BACK = Button(image=None, pos=(400, 560), 
                            text_input="BACK", font=medFont, base_color="Black", hovering_color="#ca6702")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.fill("#000814")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = frostbite(70).render("TicTac Ball", True, "#ca6702")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 140))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/option_s.png"), pos=(400, 310),
                             text_input="Play", font=frostbite(35), base_color="#d7fcd4", hovering_color="#6c757d")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/option_s.png"), pos=(400, 435),
                             text_input="Instruction", font=frostbite(35), base_color="#d7fcd4", hovering_color="#6c757d")                    
        QUIT_BUTTON = Button(image=pygame.image.load("assets/option_s.png"), pos=(400, 560),
                             text_input="Quit", font=frostbite(35), base_color="#d7fcd4", hovering_color="#6c757d")

        SCREEN.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
