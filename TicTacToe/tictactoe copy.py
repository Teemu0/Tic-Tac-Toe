# Tic tac toe AI using a mini-maxing recursive function. Tutorial used: https://www.youtube.com/watch?v=Bk9hlNZc6sE&ab_channel=CodingSpot . 21.4.2023.

# Default opponent: ai-hard.
# Default starting player: player 1.
# Controls:
#   "0" : change the opponent to ai-random
#   "1" : change the opponent to ai-hard
#   "g" : change the opponent to player 2
#   "r" : start a new game

import sys
import pygame
import numpy as np
import random
import copy
import time

from constants import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

class Menu:
    def __init__(self):
        pygame.font.init()  # you have to call this at the start, 
                            # if you want to use this module.
        self.difficulty = None
        self.starter = None
        self.starter_show =  None
        self.ready_to_play = False

        self.menu_screen = False
        self.results_screen = False
        self.big_font = pygame.font.SysFont('Comic Sans MS', 40)
        self.small_font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw_menu_screen(self, difficulty, starter_show):

        # ---------- Choose difficulty ---------- 
        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(OFFSET, MENU_TOP_1A, WIDTH - OFFSET_2, MENU_OPTION_HEIGHT))
        text_surface = self.big_font.render('Choose difficulty', True, (0, 0, 0), MENUBOX_COLOR)
        screen.blit(text_surface, (OFFSET, MENU_TOP_1A))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(OFFSET, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('Easy', True, (0, 0, 0), MENUBOX_COLOR)
        screen.blit(text_surface, (OFFSET, MENU_TOP_1B))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('Hard', True, (0, 0, 0), MENUBOX_COLOR)
        screen.blit(text_surface, (MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_1B))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('Impossible', True, (0, 0, 0), MENUBOX_COLOR)
        screen.blit(text_surface, (2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_1B))

        if difficulty == 1:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(OFFSET, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('Easy', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (OFFSET, MENU_TOP_1B))

        if difficulty == 2:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('Hard', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_1B))
        
        if difficulty == 3:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_1B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('Impossible', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_1B))

        # ---------- Do you wish to go first? ---------- 
        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(OFFSET, MENU_TOP_2A, WIDTH - OFFSET_2, MENU_OPTION_HEIGHT))
        text_surface = self.big_font.render('Would you like to go first?', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (OFFSET, MENU_TOP_2A))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(OFFSET, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('Yes', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (OFFSET, MENU_TOP_2B))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('No', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_2B))

        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        text_surface = self.small_font.render('Randomize', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_2B))

        if starter_show == 1:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(OFFSET, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('Yes', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (OFFSET, MENU_TOP_2B))
        
        if starter_show  == 2:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('No', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (MENU_OPTION_WIDTH + OFFSET_1_5, MENU_TOP_2B))
        
        if starter_show == 3:
            pygame.draw.rect(screen, MENU_SELECTED_COLOR, pygame.Rect(2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_2B, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
            text_surface = self.small_font.render('Randomize', True, (0, 0, 0), MENU_SELECTED_COLOR)
            screen.blit(text_surface, (2 * MENU_OPTION_WIDTH + OFFSET_2, MENU_TOP_2B))

        

        # ---------- Play ---------- 
        pygame.draw.rect(screen, MENUBOX_COLOR, pygame.Rect(OFFSET, MENU_TOP_3A, WIDTH - OFFSET_2, MENU_OPTION_HEIGHT))
        text_surface = self.big_font.render('Play', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (OFFSET, MENU_TOP_3A))


    def choose_difficulty(self, row, col):
        # choose difficulty
        if (MENU_TOP_1B - 1) < row < (MENU_TOP_1B + MENU_OPTION_HEIGHT + 1):
            #easy
            if OFFSET - 1 < col < OFFSET + MENU_OPTION_WIDTH + 1:
                self.difficulty = 1
            #hard
            elif OFFSET_1_5 + MENU_OPTION_WIDTH < col < OFFSET_1_5 + 2 * MENU_OPTION_WIDTH:
                self.difficulty = 2
            #impossible
            elif OFFSET_2 + 2 * MENU_OPTION_WIDTH < col < OFFSET_2 + 3 * MENU_OPTION_WIDTH:
                self.difficulty = 3

        print(self.difficulty)
        return self.difficulty
    
    def choose_starter(self, row, col):
        # choose starter
        if (MENU_TOP_2B - 1) < row < (MENU_TOP_2B + MENU_OPTION_HEIGHT + 1):
            #yes
            if OFFSET - 1 < col < OFFSET + MENU_OPTION_WIDTH + 1:
                self.starter = 1
                self.starter_show = 1
            #no
            elif OFFSET_1_5 + MENU_OPTION_WIDTH < col < OFFSET_1_5 + 2 * MENU_OPTION_WIDTH:
                self.starter = 2
                self.starter_show = 2
            #randomize
            elif OFFSET_2 + 2 * MENU_OPTION_WIDTH < col < OFFSET_2 + 3 * MENU_OPTION_WIDTH:
                self.starter = random.randint(1,2)
                self.starter_show = 3

        print(self.starter)
        return self.starter

    def start_game(self, row, col):
        if (MENU_TOP_3A - 1) < row < (MENU_TOP_3A + MENU_OPTION_HEIGHT + 1):
            if OFFSET - 1 < col < WIDTH - OFFSET + 1:
                print("play")
                self.ready_to_play = True
                return self.ready_to_play
        
    def draw_results_screen(self, result):
        # Declare results
        if result == 1: #player wins
            text_surface = self.big_font.render('You win!', True, (0, 0, 0), (200,200,200))
            screen.blit(text_surface, (OFFSET, MENU_TOP_1B))

        elif result == 2: # opponent wins
            text_surface = self.big_font.render('The opponent wins!', True, (0, 0, 0), (200,200,200))
            screen.blit(text_surface, (OFFSET, MENU_TOP_1B))

        elif result == 3 :# draw
            text_surface = self.big_font.render('It is a draw!', True, (0, 0, 0), (200,200,200))
            screen.blit(text_surface, (OFFSET, MENU_TOP_1B))

        # Rematch button
        text_surface = self.big_font.render('Rematch', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (OFFSET, MENU_TOP_2A))
        # Back to menu button
        text_surface = self.big_font.render('Back to menu', True, (0, 0, 0), (200,200,200))
        screen.blit(text_surface, (OFFSET, MENU_TOP_2B))

    def choose_rematch(self, row, col):
        if (MENU_TOP_2A - 1) < row < (MENU_TOP_2A + MENU_OPTION_HEIGHT):
            #yes
            if OFFSET - 1 < col < OFFSET + MENU_OPTION_WIDTH + 12:
                print("rematch")
                return True
        else:
            return False
    
    def back_to_menu(self, row, col):
        if (MENU_TOP_2B - 1) < row < (MENU_TOP_2B + MENU_OPTION_HEIGHT):
            #yes
            if OFFSET - 1 < col < OFFSET + MENU_OPTION_WIDTH + 99:
                print("Back to menu")
                return True
        else:
            return False

        
        




class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0
    
    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        # descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            
            return self.squares[1][1]
        
        # ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT - 20)
                    fPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def is_full(self):
        return self.marked_sqrs == 9
    
    def is_empty(self):
        return self.marked_sqrs == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs


class AI:
    def __init__(self, level=3, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move
        
        # player 2 wins
        if case == 2:
            return -1, None
        
        # draw
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        time.sleep(0.2)
        if main_board.is_empty():
            # random choice
            eval = "random"
            move = self.rnd(main_board)
        
        else:
            if self.level == 1: # easy
                # random choice
                eval = "random"
                move = self.rnd(main_board)
                
            elif self.level == 2: # hard
                if random.randint(1, 8) == 1:
                    # random choice
                    eval = "random"
                    move = self.rnd(main_board)
                else:
                    # minimax algo choice
                    eval, move = self.minimax(main_board, False)

            elif  self.level == 3: # impossible
                # minimax algo choice
                eval, move = self.minimax(main_board, False)

        print(f"AI has chosen to mark the square in pos {move} with an eval of: {eval}")
        return move # (row, col)


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.menu = Menu()
        self.player = 1 #1-cross #2-circles
        self.gamemode = "ai" # pvp or  ai
        self.running = False
        self.result = None
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # background
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross
            #descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            #ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()
    
    def winner(self):
        if self.board.final_state() == 1:
            self.result = 1
            return 1
        elif self.board.final_state() == 2:
            self.result = 2
            return 2
        elif self.board.is_full():
            self.result = 3
            return 3



    def reset(self):
        self.__init__()


def main():
    
    # object
    game = Game()
    board = game.board
    ai = game.ai
    menu = game.menu
    # state machine variables
    menu.menu_screen = True
    game.running =  False
    menu.results_screen = False
    # game settings
    menu.difficulty = None
    menu.starter = None
    game.result = None
    
    

    # mainloop
    while True:
        # menu loop
        while menu.menu_screen:
            menu.draw_menu_screen(menu.difficulty, menu.starter_show) # draw menu*

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1]
                    col = pos[0]       
                    ai.level = menu.choose_difficulty(row, col) # choose difficulty
                    game.player = menu.choose_starter(row, col) # choose who goes first
                    if menu.difficulty and menu.starter:
                        if menu.start_game(row, col):# play
                            game.show_lines()
                            menu.menu_screen = False
                            game.running = True
        
            pygame.display.update()

        # During game
        while game.running:
            while game.player != ai.player:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:

                        # g-gamemode
                        if event.key == pygame.K_g:
                            game.change_gamemode()
                        
                        # r-restart
                        if event.key == pygame.K_r:
                            game.reset()
                            board = game.board
                            ai = game.ai

                        # 0-random ai
                        if event.key == pygame.K_0:
                            ai.level = 0

                        # 1-minmax ai
                        if event.key == pygame.K_1:
                            ai.level = 1

                    if event.type == pygame.MOUSEBUTTONDOWN and game.player != ai.player:
                        pos = event.pos
                        row = pos[1] // SQSIZE
                        col = pos[0] // SQSIZE
                        
                        if board.empty_sqr(row, col) and game.running:
                            game.make_move(row, col)

                            if game.is_over():
                                game.winner()
                                game.running = False
                                menu.results_screen = True         
                    
            if game.gamemode == "ai" and game.player == ai.player and game.running:
                # update the screen
                pygame.display.update()

                # ai methods
                row, col = ai.eval(board)
                game.make_move(row, col)

                if game.is_over():
                    game.winner()
                    game.running = False
                    menu.results_screen = True
                    
            pygame.display.update()
            pygame.event.clear()
            if game.is_over():
                time.sleep(0.6)
                
            

        # Results screen loop
        while menu.results_screen:
            
            menu.draw_results_screen(game.result)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1]
                    col = pos[0]  
                    print(pos)
                    if menu.choose_rematch(row, col):
                        game.reset()
                        board = game.board
                        ai = game.ai
                        ai.level = menu.difficulty # choose difficulty
                        if menu.starter_show < 3:
                            game.player = menu.starter_show # choose who goes first
                        else:
                            game.player = random.randint(1,2)
                        menu.results_screen = False
                        game.running = True
                    elif menu.back_to_menu(row, col):
                        game.reset()
                        board = game.board
                        ai = game.ai
                        ai.level = menu.difficulty # choose difficulty
                        if menu.starter_show < 3:
                            game.player = menu.starter_show # choose who goes first
                        else:
                            game.player = random.randint(1,2)
                        menu.results_screen = False
                        menu.menu_screen = True


            pygame.display.update()

main()
