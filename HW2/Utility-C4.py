import numpy as np
import math

class State
    #In my solution, every board state is going to be stored in a state object.
    #It has X children/successor states, where X is the width of the board and the maximum number of options for plays at a state
    #skip_board: cells in the board that do not need to be checked anymore because predescessor states
    #   marked them as cells that could no longer be start of a winning connect-n sequence
    #   this is a 3 dimentional bit map, of dimentions (4,x,y). It corresponds to 4 bit maps of the board for the skip cells in 4
    #   possible directions of play (Vertical, +45 degrees, -45 degrees, horizontal). For any cell, it will tell in which directions
    #   it could still originate a winning sequence or not. It is enherited and updated from previous states to its successors
    #Scores: scores for both players 1 and 2 according to the utility function
    #Alpha&Beta: alpha and beta for the state (and successors)
    #v: final utility, which is ultimately derived from the scores given by the utility function
    def __init__(self, parent, board_state, skip_board, isMax):
        self.board_state = board_state
        self.skip_board = skip_board
        self.scores = [0,0]
        self.alpha = -math.inf
        self.beta = math.inf
        self.v = 0
    
    #Calculates the final value for the utility v based on the state score for both players
    #The function performs a weighted average of the score, based on how offensive or defensive the AI should be
    #The offensiveness argument must be between 0 and 1. The higher the value, the more the algorithm will value moves
    #   that improve its chance of winning. At the same time, the lower the value, the more the algorithm will be deffensive
    #   and value moves that stop the opponent from winning
    def final_utility(self, offensiveness):
        offensive_score = offensiveness * scores[1]
        deffensive_score = -1 * (1-offensiveness) * scores[2]
        final = offensive_score + deffensive_score
        self.v = final
        return final;
        

class UtilityCN:
    #Utility class that is unique for a game and is used for utility calculation
    #Object initialization stores the size of the board (x and y), the length of a winning sequence n (Connect-4 : n = 4)
    #Stores the score weights for sequences of 0, 1, 2, 3 and 4 pieces owned by the same player
    #Example: score_weights = [0, 10, 25, 100, 10000] means
    #   sequences of 0 get 0 points
    #   sequences of 1 get 10 points
    #   sequences of 2 get 25 points
    #   sequences of 3 get 100 points
    #   sequences of 4 get 10000 points
    def __init__(self,x ,y , n, score_weights):
        self.x = x
        self.y = y
        self.n = n
        self.score_weights = score_weights
    
    #Utility function that takes a board_state and the bitmap skip_board
    def utility_cn_1(self, board_state, skip_board):
        scores = np.zeros((1,2)) #Array that stores the score of both players as the function loops through the cells and directions
        d=0 #Indicate current direction, for reference of the skip_board bitmap d:(dx,dy)-> 0:(1,0) - 1:(1,1) - 2:(0,1) - 3:(1,-1)
        for dx, dy in [(1,0),(1,1),(0,1),(1,-1)]:#Loops through directions/ dx dy combinations
            for i in range(x): #Loops through rows
                for j in range(y): #Loops through columns
                    if skip_board[d][i][j] != 0: #Checks if current cell and cirection should not be checked anymore
                        this = board_state[i][j] #Gets the value/piece in current cell (0-empty, 1-current player, 2-opponent)
                        sequence = 1 if this != else 0 #Initializes the sequence size if the first cell is not empty
                        #Iterative variables for step
                        i_step = i
                        j_step = j
                        for step in range(self.n-1): #Iterate steps from current cell
                            i_step += dx
                            j_step += dy
                            #Checks for off-bounds steps
                            if i_step >= self.x or i_step < 0 or j_step >= self.y or j_step < 0:
                                skip_board[d][i][j] = 1 #Set this cell and direction to be skipped
                                sequence = 0 #Reset sequence value to 0
                                break;
                            next = board_state[i_step][j_step] #Gets next cell
                            if this == 0 and next > 0:
                                # If all cells so far were empty and the next is not, update this sequence to match the player with piece on next cell
                                this = next
                                sequence = 1
                            elif this != next:
                                # If the cells dont match and are from different players, this sequence cant be a winning sequence for either
                                # Adds cell and direction to skip_board
                                # Resets sequence to 0
                                skip_board[d][i][j] = 1
                                sequence = 0
                                break;
                            else:
                                # Else, the piece is from the same player and the sequence count increases
                                sequence += 1
            #Adds score based on sequence and weights predefined in the class
            scores[this-1] += self.score_weights[sequence]
            d += 1 #Moves direction
        return scores, skip_board; #Returns the score for the state and the updated skip_board to be inherieted