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

pygame.mixer.music.load('audio/main.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 60

BG = pygame.image.load("assets/bg.png")


def get_font(size):
    return pygame.font.Font("assets/burbank.otf", size)

smallFont = pygame.font.Font("assets/burbank.otf", 25)
medFont = pygame.font.Font("assets/burb.ttf", 40)
largeFont = pygame.font.Font("assets/burbank.otf", 100)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(SCREEN_WIDTH/2.3), (int(SCREEN_HEIGHT / 2.1) + y_displace))
    SCREEN.blit(textSurf, textRect)

def play():
    pause = False
    while True:

        player = mixer.Sound('audio/play.mp3')
        player.play()
        player.set_volume(0.2)
        mixer.music.stop()
	
		BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)
        gray = (206, 212, 218)
        ORANGE = (202, 103, 2)
	
		ROW_COUNT = 6
        COLUMN_COUNT = 7

        PLAYER = 0
        AI = 1

        EMPTY = 0
        PLAYER_PIECE = 1
        AI_PIECE = 2

        WINDOW_LENGTH = 4
	
		def create_board():
         	board = np.zeros((ROW_COUNT, COLUMN_COUNT))
         	return board

        def drop_piece(board, row, col, piece):
            board[row][col] = piece

        def is_valid_location(board, col):
            return board[ROW_COUNT - 1][col] == 0

        def get_next_open_row(board, col):
            for r in range(ROW_COUNT):
                if board[r][col] == 0:
                    return r
		def print_board(board):
            print(np.flip(board, 0))

        def winning_move(board, piece):
			for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT):
                    if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                        c + 3] == piece:
                        return True
		
			for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT - 3):
                    if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                        c] == piece:
                        return True
		
			for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT - 3):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                            board[r + 3][c + 3] == piece:
                        return True
		
			for c in range(COLUMN_COUNT - 3):
                for r in range(3, ROW_COUNT):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                            board[r - 3][c + 3] == piece:
                        return True
		
		def evaluate_window(window, piece):
            score = 0
            opp_piece = PLAYER_PIECE
            if piece == PLAYER_PIECE:
                opp_piece = AI_PIECE

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(EMPTY) == 2:
                score += 2

            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score -= 4

            return score

		def score_position(board, piece):
            score = 0

		center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3
		
		for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)
			
		for c in range(COLUMN_COUNT):
                col_array = [int(i) for i in list(board[:, c])]
                for r in range(ROW_COUNT - 3):
                    window = col_array[r:r + WINDOW_LENGTH]
                    score += evaluate_window(window, piece)
			
		for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)
			
		for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score


	def is_terminal_node(board):
            return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(
                get_valid_locations(board)) == 0

        def minimax(board, depth, alpha, beta, maximizingPlayer):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if winning_move(board, AI_PIECE):
                        return (None, 100000000000000)
                    elif winning_move(board, PLAYER_PIECE):
                        return (None, -10000000000000)
                    else:  # Game is over, no more valid moves
                        return (None, 0)
                else:  # Depth is zero
                    return (None, score_position(board, AI_PIECE))
            if maximizingPlayer:
                value = -math.inf
                column = random.choice(valid_locations)
                for col in valid_locations:
                    row = get_next_open_row(board, col)
                    b_copy = board.copy()
                    drop_piece(b_copy, row, col, AI_PIECE)
                    new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return column, value
	else:
	    value = math.inf
                column = random.choice(valid_locations)
                for col in valid_locations:
                    row = get_next_open_row(board, col)
                    b_copy = board.copy()
                    drop_piece(b_copy, row, col, PLAYER_PIECE)
                    new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return column, value

        def get_valid_locations(board):
            valid_locations = []
            for col in range(COLUMN_COUNT):
                if is_valid_location(board, col):
                    valid_locations.append(col)
            return valid_locations

        def pick_best_move(board, piece):

            valid_locations = get_valid_locations(board)
            best_score = -10000
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                temp_board = board.copy()
                drop_piece(temp_board, row, col, piece)
                score = score_position(temp_board, piece)
                if score > best_score:
                    best_score = score
                    best_col = col

            return best_col	

	def draw_board(board):
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):
                    pygame.draw.rect(screen, gray,
                                     (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.circle(screen, BLACK, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       RADIUS)

	


    
			

	
	
	

	
	
	def draw_board (board):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):		
				if board[r][c] == PLAYER_PIECE:
					pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				elif board[r][c] == AI_PIECE: 
					pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
		pygame.display.update()
				
board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
				
	if event.type == pygame.MOUSEMOTION:
		pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
		posx = event.pos[0]
		if turn == PLAYER:
			pygame.draw.circle (screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
				
	pygame.display.update()
				
	if event.type == pygame.MOUSEBUTTONDOWN:
		pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				
	if turn == PLAYER:
		posx = event.pos[0]
		col = int(math.floor(posx/SQUARESIZE))
				
		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, PLAYER_PIECE)
				
			if winning_move(board, PLAYER_PIECE):
				label = myfont.render("Player 1 wins!!", 1, RED)
				screen.blit(label, (40, 10))
				game_over = True
				
			turn += 1
			turn = turn % 2
				
			print_board(board)
				
			draw_board(board)	
				if turn == AI and not game_over:
				col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, AI_PIECE)
				
				
				if winning_move(board, Ai_PIECE):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label. (40, 10))
					game_over = True
				
				print_board(board)
				draw _board(board)
				
				turn += 1
				turn = turn % 2
		if game_over:
			pygame.time.wait(3000)
				
				

				
				


	



