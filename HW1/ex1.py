class ConnectFour:

    def __init__(self, board, w, h):
        """Class constructor"""
        # Board data
        self.board = board
        # Board width
        self.w = w
        # Board height
        self.h = h

    def isLineAt(self, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y)
           in direction (dx,dy)"""
        this_cell = self.board[x][y] #Gets player for this cell
        if this_cell == 0:
            return False; # no player with this cell
        for i in range(3): # Iterate through dx dy steps 3 times
            next_x = x + dx
            next_y = y + dy
            if next_x < self.h and next_x >= 0 and next_y < self.w and next_y >=0: #If next step is in the board
                next_cell = self.board[next_x][next_y]
                if this_cell != next_cell: # Compares this cell with next, stoping if they are different
                    return False;
                this_cell = next_cell # Moves forward
                x = next_x
                y = next_y
            else:
                return False; #Reached out of bounds of board
        return True; #If all 3 steps were taken and the piece was always from the same player, return true

    def isAnyLineAt(self, x, y):
        """Return True if a line of identical symbols exists starting at (x,y)
           in four directions"""
        #The oposite directions do not need to be checked as they will be from the opposite end of the line
        return (self.isLineAt(x, y, 1, 0) or # Horizontal (right)
                self.isLineAt(x, y, 0, 1) or # Vertical (up)
                self.isLineAt(x, y, 1, 1) or # Diagonal 45 (up right)
                self.isLineAt(x, y, 1, -1)) # Diagonal -45 (down right)

    def getOutcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and
           0 for no winner"""
        # Your code here, use isAnyLineAt()
        if self.w < 4 or self.h < 4: #No possible winner with board that is not at least 4x4
            return 0;
        
        #looks for winner starting at every position a line can start and be in one of the possible directions:
        #Up, right, up and right, down and right
        for x in range(self.h):
            for y in range(self.w):
                if (x < self.h-3 or y < self.w-3) and self.isAnyLineAt(x,y):
                    #No line cant start where x and y are in the highest 3 possible values (Top right 3x3 area)
                    return self.board[x][y];
        return 0; #no winner found

    def printOutcome(self):
        """Prints the winner of the game"""
        o = self.getOutcome()
        if o == 0:
            print("No winner")
        else:
            print("Player", o, " won")
