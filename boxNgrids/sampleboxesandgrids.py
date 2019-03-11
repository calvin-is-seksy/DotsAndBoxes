import pygame
import math
import random
import time 
from copy import deepcopy
class BoxesGame():
    def __init__(self):
        #initialize variables for the current state
        self.hColor=[[0 for x in range(6)] for y in range(7)]
        self.vColor=[[0 for x in range(7)] for y in range(6)]
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        #initialize variables for tracking the score
        self.score_player1=0;
        self.score_player2=0;
    def update(self):
    

        print ('Player 2')
        self.player2();
        print ('Player1')
        self.player1();
        
    # A function to lost all the possible moves 
    def list_possible_moves(self,state_h,state_v):
        #make the move true if the last move is not true to be true in the psuedo list
        
        next_moves=[];
        for x in range (7):
            for y in range(6):
                if(state_h[x][y]==False):
                    next_moves.append([x,y,1]); # append all horizontal moves
                
                
                
        for x in range (6):
            for y in range(7):
                if(state_v[x][y]==False):
                    next_moves.append([x,y,0]); # append all horizontal moves
                
        
                
        return next_moves
    # gives the current state of the system
    def current_state(self):
        '''
        h_matrix =[[False for x in range(6)] for y in range(7)];
        v_matrix=[[False for x in range(7)] for y in range(6)];
        for x in range (7):
            for y in range(6):
                h_matrix[x][y]=self.boardh[x][y]
        for x in range (6):
            for y in range(7):
                v_matrix[x][y]=self.boardv[x][y]
                
        '''
        h2=deepcopy(list(self.boardh))
        v2=deepcopy(list(self.boardv))
        return h2,v2
    #checks if the score has been updated by a given move or not
    def increment_score(self,move,h_matrix,v_matrix):
        temp_score=0;
        xpos=move[0];
        ypos=move[1];
        if(move[2]==0): # vertical matrices
            if(ypos==0):# left most edge
                if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
                    temp_score=1;
            elif(ypos==6):# left most edge   
                if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
                    temp_score=1;     
            else:
                if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
                    temp_score=temp_score+1;
                if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
                    temp_score=temp_score+1;
                    
        if(move[2]==1): # horizontal matrices
            if(xpos==0):
                if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
                    temp_score=1;
            elif(xpos==6):
                if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
                    temp_score=1;
                
            else:
                if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
                    temp_score=temp_score+1;
                if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
                    temp_score=temp_score+1;
                
                
            
        return temp_score;
    # function to actulally make a move
    def make_move(self,move,player_id):
        #print 'value before coming',self.boardh
        xpos=move[0];
        ypos=move[1];
        print (xpos,ypos)
        if(move[2]==1):# Vertical Matrices
            
            self.boardh[xpos][ypos]=True;
            
        if(move[2]==0):
            self.boardv[xpos][ypos]=True;
        #self.boardh_temp = self.boardh
        #self.boardv_temp = self.boardv
        score=self.increment_score(move,self.boardh,self.boardv);
        if(player_id==0):
            self.score_player1=self.score_player1+self.increment_score(move,self.boardh,self.boardv);
            
        if(player_id==1):
            self.score_player2=self.score_player2+self.increment_score(move,self.boardh,self.boardv);
            
       
        
    # function for printing the next state of the system    
    def next_state(self,move,h1,v1):
        xpos=move[0];
        ypos=move[1];
        h_matrix1=deepcopy(list(h1))
        v_matrix1=deepcopy(list(v1))
        
        score=self.increment_score(move,h_matrix1,v_matrix1);
        #print move[2];
        if(move[2]==0):#vetical matrices
            
            v_matrix1[xpos][ypos]=True;
            
            #self.boardv[xpos][ypos]=False
        if(move[2]==1):#horizontal matrices
            
            h_matrix1[xpos][ypos]=True;
            
            #self.boardh[xpos][ypos]=False
        #print move ,h_matrix,v_matrix
        return h_matrix1,v_matrix1,score;
    # function for 
    def game_ends(self,temp_h,temp_v):
        count=True;
        for x in range(6):
            for y in range(7):
                if not temp_h[y][x]:
                    count=False;
        for x in range(7):
            for y in range(6):
                if not temp_v[y][x]:
                    count=False;
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
     
bg=BoxesGame();
while (bg.game_ends(bg.boardh,bg.boardv)==False):
    bg.update();
    print ('Player1 :score',bg.score_player1)
    print ('Player2:score',bg.score_player2)
    time.sleep(2)
time.sleep(10)
pygame.quit()