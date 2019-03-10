import random
import pygame
import math
import time
from copy import deepcopy


class BoxesandGridsGame():
    def __init__(self):
        pass
        # 1
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        # 2
        self.hColor = [[0 for x in range(6)] for y in range(7)]
        self.vColor = [[0 for x in range(7)] for y in range(6)]
        # initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")
        # 3
        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        self.boardh_temp = self.boardh
        self.boardv_temp = self.boardv
        self.initGraphics();
        self.drawBoard();
        self.hColor = [[0 for x in range(6)] for y in range(7)]
        self.vColor = [[0 for x in range(7)] for y in range(6)]

        self.goal_x = 6;
        self.goal_y = 5;
        self.initial_move = [0, 0, 0];

        self.score_player1 = 0;
        self.score_player2 = 0;

    def update(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)

        # clear the screen
        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
        print ('before making a move')
        self.player2();
        print ('move made by player 2')
        self.player1();
        print ('move made by player 1')
        # update the screen

        pygame.display.flip()

    def initGraphics(self):
        self.normallinev = pygame.image.load("normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.bar_donev = pygame.image.load("bar_done.png")
        self.bar_doneh = pygame.transform.rotate(pygame.image.load("bar_done.png"), -90)
        self.bar_donev_r = pygame.image.load("bar_done_red.png")
        self.bar_doneh_r = pygame.transform.rotate(pygame.image.load("bar_done_red.png"), -90)
        self.bar_donev_g = pygame.image.load("bar_done_green.png")
        self.bar_doneh_g = pygame.transform.rotate(pygame.image.load("bar_done_green.png"), -90)
        self.bar_donev_r_l = pygame.image.load("bar_done_light_red.png")
        self.bar_doneh_r_l = pygame.transform.rotate(pygame.image.load("bar_done_light_red.png"), -90)
        self.bar_donev_g_l = pygame.image.load("bar_done_light_green.png")
        self.bar_doneh_g_l = pygame.transform.rotate(pygame.image.load("bar_done_light_green.png"), -90)
        self.hoverlinev = pygame.image.load("hoverline.png")
        self.hoverlineh = pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
        self.separators = pygame.image.load("separators.png")
        self.redindicator = pygame.image.load("redindicator.png")
        self.greenindicator = pygame.image.load("greenindicator.png")
        self.greenplayer = pygame.image.load("greenplayer.png")
        self.blueplayer = pygame.image.load("blueplayer.png")
        self.winningscreen = pygame.image.load("youwin.png")
        self.gameover = pygame.image.load("gameover.png")
        self.score_panel = pygame.image.load("score_panel.png")

    def drawBoard(self):
        for x in range(6):
            for y in range(7):

                if (self.hColor[y][x] == -1):
                    self.screen.blit(self.bar_doneh_r, [(x) * 64 + 5, (y) * 64])
                elif self.hColor[y][x] == 1:
                    self.screen.blit(self.bar_doneh_g, [(x) * 64 + 5, (y) * 64])
                else:
                    self.screen.blit(self.bar_doneh, [(x) * 64 + 5, (y) * 64])

        for x in range(7):
            for y in range(6):

                if (self.vColor[y][x] == -1):
                    self.screen.blit(self.bar_donev_r, [(x) * 64, (y) * 64 + 5])
                elif self.vColor[y][x] == 1:
                    self.screen.blit(self.bar_donev_g, [(x) * 64, (y) * 64 + 5])
                else:
                    self.screen.blit(self.bar_donev, [(x) * 64, (y) * 64 + 5])

        for x in range(7):
            for y in range(7):
                self.screen.blit(self.separators, [x * 64, y * 64])

    def drawHUD(self):
        # draw the background for the bottom:
        self.screen.blit(self.score_panel, [0, 389])
        # create font
        myfont = pygame.font.SysFont(None, 32)

        # create text surface
        label = myfont.render("Player 1:", 1, (255, 255, 255))

        # draw surface
        self.screen.blit(label, (10, 400))
        # same thing here
        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.score_player1), 1, (255, 255, 255))
        scoreother = myfont64.render(str(self.score_player2), 1, (255, 255, 255))
        scoretextme = myfont20.render("Player1", 1, (255, 255, 255))
        scoretextother = myfont20.render("Player2", 1, (255, 255, 255))

        self.screen.blit(scoretextme, (10, 425))
        self.screen.blit(scoreme, (10, 435))
        self.screen.blit(scoretextother, (280, 425))
        self.screen.blit(scoreother, (340, 435))

    def finished(self):
        self.screen.blit(self.winningscreen, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()

    def next_possible_moves(self, move):
        # make the move true if the last move is not true to be true in the psuedo list
        if (move[2] == 1):
            self.boardh_temp[move[0]][move[1]] = True;
        elif (move[2] == 0):
            self.boardv_temp[move[0]][move[1]] = True;
        else:
            print ("Invalid move");
        next_moves = [];

        for x in range(7):
            for y in range(6):
                if (self.boardh_temp[x][y] == False):
                    next_moves.append([x, y, 1]);  # append all horizontal moves

        for x in range(6):
            for y in range(7):
                if (self.boardv_temp[x][y] == False):
                    next_moves.append([x, y, 0]);  # append all horizontal moves

        return next_moves

    def list_possible_moves(self, state_h, state_v):
        # make the move true if the last move is not true to be true in the psuedo list

        next_moves = [];
        for x in range(7):
            for y in range(6):
                if (state_h[x][y] == False):
                    next_moves.append([x, y, 1]);  # append all horizontal moves

        for x in range(6):
            for y in range(7):
                if (state_v[x][y] == False):
                    next_moves.append([x, y, 0]);  # append all horizontal moves

        return next_moves

    def current_state(self):
        return self.boardh, self.boardv

    def increment_score(self, move, h_matrix, v_matrix):
        temp_score = 0;
        xpos = move[0];
        ypos = move[1];
        if (move[2] == 0):  # vertical matrices
            if (ypos == 0):  # left most edge
                if (h_matrix[xpos][ypos] == True and h_matrix[xpos + 1][ypos] == True and v_matrix[xpos][
                    ypos + 1] == True):
                    temp_score = 1;
            elif (ypos == 6):  # left most edge
                if (h_matrix[xpos][ypos - 1] == True and h_matrix[xpos + 1][ypos - 1] == True and v_matrix[xpos][
                    ypos - 1] == True):
                    temp_score = 1;
            else:
                if (h_matrix[xpos][ypos] == True and h_matrix[xpos + 1][ypos] == True and v_matrix[xpos][
                    ypos + 1] == True):
                    temp_score = temp_score + 1;
                if (h_matrix[xpos][ypos - 1] == True and h_matrix[xpos + 1][ypos - 1] == True and v_matrix[xpos][
                    ypos - 1] == True):
                    temp_score = temp_score + 1;

        if (move[2] == 1):  # horizontal matrices
            if (xpos == 0):
                if (v_matrix[xpos][ypos] == True and v_matrix[xpos][ypos + 1] == True and h_matrix[xpos + 1][
                    ypos] == True):
                    temp_score = 1;
            elif (xpos == 6):
                if (v_matrix[xpos - 1][ypos] == True and v_matrix[xpos - 1][ypos + 1] == True and h_matrix[xpos - 1][
                    ypos] == True):
                    temp_score = 1;

            else:
                if (v_matrix[xpos][ypos] == True and v_matrix[xpos][ypos + 1] == True and h_matrix[xpos + 1][
                    ypos] == True):
                    temp_score = temp_score + 1;
                if (v_matrix[xpos - 1][ypos] == True and v_matrix[xpos - 1][ypos + 1] == True and h_matrix[xpos - 1][
                    ypos] == True):
                    temp_score = temp_score + 1;

        return temp_score;

    def make_move(self, move, player_id):
        print ('value before coming', self.boardh)
        xpos = move[0];
        ypos = move[1];
        # print xpos,ypos
        if (move[2] == 1):  # Vertical Matrices

            self.boardh[xpos][ypos] = True;

        if (move[2] == 0):
            self.boardv[xpos][ypos] = True;
        self.boardh_temp = self.boardh
        self.boardv_temp = self.boardv
        # score=self.increment_score(move,self.boardh,self.boardv);
        # print self.boardh,self.boardv
        ### Leave space here for player color change 

        if (player_id == 0):
            self.score_player1 = self.score_player1 + self.increment_score(move, self.boardh, self.boardv);
            if (move[2] == 1):
                self.hColor[xpos][ypos] = -1;
            if (move[2] == 0):
                print (xpos, ypos)
                self.vColor[xpos][ypos] = -1;

        if (player_id == 1):
            self.score_player2 = self.score_player2 + self.increment_score(move, self.boardh, self.boardv);
            if (move[2] == 1):
                self.hColor[xpos][ypos] = 1;
            if (move[2] == 0):
                self.vColor[xpos][ypos] = 1;

    def next_state(self, move, h1, v1):
        xpos = move[0];
        ypos = move[1];
        h_matrix1 = deepcopy(list(h1))
        v_matrix1 = deepcopy(list(v1))

        score = self.increment_score(move, h_matrix1, v_matrix1);
        # print move[2];
        if (move[2] == 0):  # vetical matrices

            v_matrix1[xpos][ypos] = True;

            # self.boardv[xpos][ypos]=False
        if (move[2] == 1):  # horizontal matrices

            h_matrix1[xpos][ypos] = True;

            # self.boardh[xpos][ypos]=False
        # print move ,h_matrix,v_matrix
        return h_matrix1, v_matrix1, score;

    def game_ends(self, temp_h, temp_v):
        count = True;
        for x in range(6):
            for y in range(7):
                if not temp_h[y][x]:
                    count = False;
        for x in range(7):
            for y in range(6):
                if not temp_v[y][x]:
                    count = False;
        return count;

    def player1(self):
        temp_h = self.boardh
        temp_v = self.boardv

        # next_move = self.list_possible_moves(temp_h, temp_v);
        #
        # best_move = next_move[0];
        # best_score = 0;
        #
        # for move in next_move:
        #
        #     temp_h, temp_v, score = self.next_state(move, temp_h, temp_v);
        #
        #     if (score > best_score):
        #         best_score = score;
        #         best_move = move;

        best_move = self.minimax(self.boardh, self.boardv)

        self.make_move(best_move, 0);

    '''
    You will make changes to the code from this part onwards
    '''

    def player2(self):
        '''
        Call the minimax/alpha-beta pruning  function to return the optimal move
        '''

        ## change the next line of minimax/ aplpha-beta pruning according to your input and output requirments

        # next_move = self.minimax(self.boardh, self.boardv)
        next_move = self.alphabetapruning(self.boardh, self.boardv)
        # next_move_alpha=self.alphabetapruning();

        self.make_move(next_move, 1);
        print ('move_made by player 2', next_move)

    '''
    Write down the code for minimax to a certain depth do no implement minimax all the way to the final state. 
    '''

    # You will implement the minimax algorithm in this function. You can change the
    # number of input parameters of the function and the output of the function must
    # be the optimal move made by the function.

    def minimax(self, horizontal, vertical, maxDepth=1):
        self.maxDepth = maxDepth
        self.depth = 0

        ######## APPROACH 2: calling max on myself
        bestMove = random.choice(self.list_possible_moves(horizontal, vertical))
        v = self.increment_score(bestMove, horizontal, vertical)

        print('All possible moves: {}'.format(self.list_possible_moves(horizontal, vertical)))
        print('Random init of bestMove: {}, {}'.format(bestMove, v))

        for newMove in self.list_possible_moves(horizontal, vertical):
            newH, newV, score = self.next_state(newMove, horizontal, vertical)
            v_ = self.minVal(newMove, newH, newV)

            print('exploring possible move: {}, score: {}, v_: {}'.format(newMove, score, v_))

            if v_ > v:
                v = v_
                print('updating to best move^')
                bestMove = newMove

        return bestMove

    def maxVal(self, move, h_matrix, v_matrix):

        # print('MAX, depth: {}, maxDepth: {}'.format(self.depth, self.maxDepth))
        # print('MOVE: {}'.format(move))
        # print (' Horizontal matrix', h_matrix)
        # print (' vertical matrix', v_matrix)

        self.depth += 1
        if self.depth == self.maxDepth or self.game_ends(h_matrix, v_matrix):  # TODO: check this is the right condition
            self.depth -= 1
            # return self.increment_score(move, h_matrix, v_matrix) * (self.depth+1)
            return self.evaluate(move, h_matrix, v_matrix)

        v = float('-inf')
        for newMove in self.list_possible_moves(h_matrix, v_matrix):
            newH, newV, score = self.next_state(newMove, h_matrix, v_matrix)
            v_ = self.minVal(newMove, newH, newV)
            if v_ > v: v = v_

        return v

    def minVal(self, move, h_matrix, v_matrix):

        # print('MIN, depth: {}, maxDepth: {}'.format(self.depth, self.maxDepth))
        # print('MOVE: {}'.format(move))
        # print (' Horizontal matrix', h_matrix)
        # print (' vertical matrix', v_matrix)

        self.depth += 1
        if self.depth == self.maxDepth or self.game_ends(h_matrix, v_matrix):  # TODO: check this is the right condition
            self.depth -= 1
            # return self.increment_score(move, h_matrix, v_matrix) * (self.depth+1)
            return self.evaluate(move, h_matrix, v_matrix)

        v = float('inf')
        for newMove in self.list_possible_moves(h_matrix, v_matrix):
            newH, newV, score = self.next_state(newMove, h_matrix, v_matrix)
            v_ = self.maxVal(newMove, newH, newV)
            if v_ < v: v = v_

        return v

    # ALPHA BETA PRUNING
    def alphabetapruning(self, horizontal, vertical, maxDepth=13):
        a = float('-inf')
        b = float('inf')
        self.maxDepth = maxDepth
        self.depth = 0

        bestMove = random.choice(self.list_possible_moves(horizontal, vertical))
        v = self.increment_score(bestMove, horizontal, vertical)

        print('All possible moves: {}'.format(self.list_possible_moves(horizontal, vertical)))
        print('Random init of bestMove: {}, {}'.format(bestMove, v))

        for newMove in self.list_possible_moves(horizontal, vertical):
            newH, newV, score = self.next_state(newMove, horizontal, vertical)
            v_ = self.minValAB(newMove, newH, newV, a, b)

            print('exploring possible move: {}, score: {}, v_: {}'.format(newMove, score, v_))

            if v_ > v:
                v = v_
                print('updating to best move^')
                bestMove = newMove

            if v_ >= b:
                print('BETA Pruning: b = {}'.format(b))
                break

            if v_ > a:
                print('ALPHA Update^')
                a = v_

        return bestMove

    def maxValAB(self, move, h_matrix, v_matrix, a, b):

        print('MAX: depth = {}, a = {}, b = {}'.format(self.depth, a, b))

        self.depth += 1
        if self.depth == self.maxDepth or self.game_ends(h_matrix, v_matrix):  # TODO: check this is the right condition
            self.depth -= 1
            # return self.increment_score(move, h_matrix, v_matrix) * (self.depth + 1)
            return self.evaluate(move, h_matrix, v_matrix)

        v = float('-inf')
        for newMove in self.list_possible_moves(h_matrix, v_matrix):
            newH, newV, score = self.next_state(newMove, h_matrix, v_matrix)
            v_ = self.minValAB(newMove, newH, newV, a, b)
            print('After recursive return: v = {}, v_ = {}, a = {}, b = {}'.format(v, v_, a, b))
            if v_ > v:
                v = v_

            if v_ >= b:
                print('BETA Pruning: b = {}'.format(b))
                return v

            if v_ > a:
                print('ALPHA Update^')
                a = v_

        return v

    def minValAB(self, move, h_matrix, v_matrix, a, b):

        print('MIN: depth = {}, a = {}, b = {}'.format(self.depth, a, b))

        self.depth += 1
        if self.depth == self.maxDepth or self.game_ends(h_matrix, v_matrix):  # TODO: check this is the right condition
            self.depth -= 1
            # return self.increment_score(move, h_matrix, v_matrix) * (self.depth + 1)
            return self.evaluate(move, h_matrix, v_matrix)

        v = float('inf')
        for newMove in self.list_possible_moves(h_matrix, v_matrix):
            newH, newV, score = self.next_state(newMove, h_matrix, v_matrix)
            v_ = self.maxValAB(newMove, newH, newV, a, b)
            print('After recursive return: v = {}, v_ = {}, a = {}, b = {}'.format(v, v_, a,b))
            if v_ < v:
                v = v_
            if v_ <= a:
                print('ALPHA Pruning: a = {}'.format(a))
                return v
            if v_ < b:
                print('BETA Update')
                b = v_

        return v

    '''
    Write down you own evaluation strategy in the evaluation function 
    '''

    def evaluate(self, move, h_matrix, v_matrix):
        return self.increment_score(move, h_matrix, v_matrix) * (self.depth + 1)


bg = BoxesandGridsGame();
while (bg.game_ends(bg.boardh, bg.boardv) == False):
    bg.update();
    print ('Player1 :score', bg.score_player1)
    print ('Player2 :score', bg.score_player2)
    time.sleep(2)
time.sleep(10)
pygame.quit()
