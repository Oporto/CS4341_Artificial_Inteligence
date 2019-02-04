import math
import agent
import time
from functools import reduce

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    def __init__(self, name, score_weights, offensiveness):
        super().__init__(name)
        # Max search depth
        self.__score_weights = score_weights
        self.__offensiveness = offensiveness
    # Heuristic that determines the maximum depth based on turn
    def __depth_heuristic(self, state):
        turn = 0
        for r in state.board:
            for c in r:
                if c != 0:
                    turn += 1
        if turn < 2:
            self.__board_x = state.h
            self.__board_y = state.w
            self.__connect_n = state.n
        if turn <state.h:
            depth = 2
        elif turn < 2 * state.h + state.w:
            depth = 4
        elif (turn < (state.h-2) * (state.w-1) and state.n == 4) or turn < (state.h-1) * (state.w-1):
            depth = 6
        else:
            depth = (state.h * state.w) - turn
        return depth;
    # Computes the value, action of a max value node in pruning
    def __max_value(self, state, depth, alpha, beta):
        win_state = state.get_outcome()
        if win_state == state.player:
            return self.__score_weights[4], -1;
        elif win_state != 0:
            return -self.__score_weights[4], -1;
        if len(state.free_cols()) == 0:
            return 0, -1;
        if depth >= 0:
            utility = self.__utility(state.board, state.player)
            return utility, -1;
        
        else:
            best = (-math.inf,-1)
            for s, a in self.__get_successors(state):
                new_utility = self.__min_value(s, depth + 1, alpha, beta)
                if new_utility >= best[0]:
                    best = (new_utility, a)
                alpha = max(alpha, best[0])
                if best[0] >= beta:
                    return best;
        return best;
    # Computes the value, action of a max value node in pruning
    def __min_value(self, state, depth, alpha, beta):
        
        win_state = state.get_outcome()
        if win_state == state.player:
            return self.__score_weights[4];
        elif win_state != 0:
            return -self.__score_weights[4];
        if len(state.free_cols()) == 0:
            return 0
        if depth >= 0:
            return self.__utility(state.board, state.player);
        else:
            worst = math.inf

            for s, a in self.__get_successors(state):
                new_utility, a = self.__max_value(s, depth + 1, alpha, beta)
                worst = min(worst, new_utility)
                beta = min(beta, worst)
                if worst <= alpha:
                    return worst;
        return worst;
            
        
    # Pick a column for the agent to play (External interface).
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        turn = 0
        depth = -self.__depth_heuristic(brd)
        utility, action = self.__max_value(brd, depth, -math.inf, math.inf)
        if action < 0 or action > 6:
            action = abs(action % 7) #This line should not be relevant unless something goes wrong and the function returns an action
        return action;

    # Get the successors of the given board.
    def __get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return [];
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ;

    #Utility function that takes a board_state and its player value
    def __utility(self, board_state, player):
        scores = [0,0] #Array that stores the score of both players as the function loops through the cells and directions
        for dx, dy in [(1,0),(1,1),(0,1),(1,-1)]:#Loops through directions/ dx dy combinations
            for i in range(self.__board_x): #Loops through rows
                for j in range(self.__board_y): #Loops through columns
                    this = board_state[i][j] #Gets the value/piece in current cell (0-empty, 1-current player, 2-opponent)
                    sequence = 1 if this != 0 else 0 #Initializes the sequence size if the first cell is not empty
                    #Iterative variables for step
                    i_step = i
                    j_step = j
                    for step in range(self.__connect_n-1): #Iterate steps from current cell
                        i_step += dx
                        j_step += dy
                        #Checks for off-bounds steps
                        if i_step >= self.__board_x or i_step < 0 or j_step >= self.__board_y or j_step < 0:
                            sequence = 0 #Reset sequence value to 0
                            break;
                            
                        next = board_state[i_step][j_step] #Gets next cell
                        if this == 0 and next > 0:
                            # If all cells so far were empty and the next is not, update this sequence to match the player with piece on next cell
                            this = next
                            sequence = 1
                        elif this != next:
                            if next == 0:
                                continue;
                            # If the cells dont match and are from different players, this sequence cant be a winning sequence for either
                            # Resets sequence to 0
                            sequence = 0
                            break;
                        else:
                            # Else, the piece is from the same player and the sequence count increases
                            if this > 0:
                                sequence += 1
                        #Adds score based on sequence and weights predefined in the class
                    scores[this-1] += self.__score_weights[sequence]
        score = self.__offensiveness * scores[0] - (1 - self.__offensiveness) * scores[1]
        if player == 2:
            score = -1 * score
        return score; #Returns the score for the state
#Final agent for class tournament (After testing and crude optimization)
THE_AGENT = AlphaBetaAgent("DeVasconcellosOportoPedro", [0,10,50,5000,1000000], 0.35)