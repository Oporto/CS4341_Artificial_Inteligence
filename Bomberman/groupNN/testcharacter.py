# This is necessary to find the main code
import sys
import heapq
import math
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]

# Node class for A* to keep track of score
class Node:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score

class TestCharacter(CharacterEntity):

    discount = 0.9
    lrate = 0.2
    followed_q = False

# constructs a grid that is equivalent to the current world state
    def constructGrid(self, wrld):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()
        grid = [[0 for i in range(width)]for j in range(height)]

        while i < height:
            while j < width:
                if wrld.empty_at(j, i):
                    grid[i][j] = 0
                elif wrld.exit_at(j, i):
                    grid[i][j] = 1
                elif wrld.wall_at(j, i):
                    grid[i][j] = 2
                elif wrld.bomb_at(j, i):
                    grid[i][j] = 3
                elif wrld.explosion_at(j, i):
                    grid[i][j] = 4
                elif wrld.monsters_at(j, i):
                    grid[i][j] = 5
                elif wrld.characters_at(j, i):
                    grid[i][j] = 6
                j+=1
            j = 0
            i += 1
        return grid

    # prints out the given grid
    def printGrid(self, wrld, grid):
        i = 0
        j = 0
        width = wrld.width()
        height = wrld.height()

        while i < height:
            while j < width:
                print(grid[i][j], end='')
                j+=1
            j=0
            i+=1
            print("\n")

    #checks for type of cell in surrounding, giving the list direction tuples as a return
    # type 1 is exit
    # type 2 is monster
    #checks for type of cell in surrounding 
    #checks for type of cell in surrounding

    def check_surroundings(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = dict([(i,[]) for i in range(7)])
        
        for dx in [-1, 0, 1]:
            
            x = thisx + dx
            
            # Avoid out-of-bound indexing
            if (x >=0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >=0) and (y < wrld.height()):
                            #Check cases
                            if (wrld.empty_at(x,y)):
                                ls = finds[0]
                                ls.append((dx,dy))
                                finds[0] = ls
                            elif (wrld.exit_at(x,y)):
                                ls = finds[1]

                                ls.append((dx,dy))
                                finds[1] = ls
                            elif (wrld.wall_at(x,y)):
                                ls = finds[2]
                                ls.append((dx,dy))

                                ls.append((dx, dy))
                                finds[1] = ls
                            elif (wrld.wall_at(x,y)):
                                ls = finds[2]
                                ls.append((dx, dy))
                                finds[2] = ls
                            elif (wrld.bomb_at(x,y)):
                                ls = finds[3]
                                ls.append((dx, dy))
                                finds[3] = ls
                            elif (wrld.explosion_at(x,y)):
                                ls = finds[4]
                                ls.append((dx, dy))
                                finds[4] = ls
                            elif (wrld.monsters_at(x,y)):
                                ls = finds[5]
                                ls.append((dx, dy))
                                finds[5] = ls
                            elif (wrld.characters_at(x,y)):
                                ls = finds[6]
                                ls.append((dx, dy))
                                finds[6] = ls
        return finds;

    # returns nodes surrounding the current position of the character
    def get_neighbors(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = [Node(-1, -1, -1)]*8
        count = 0
        danger = 0
        monsterLoc = self.find_monsters(wrld)

        for dx in [-1, 0, 1]:
            x = thisx + dx
            # Avoid out-of-bound indexing
            if (x >= 0) and (x < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    y = thisy + dy
                    # Skip current cell
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y >= 0) and (y < wrld.height()):
                            for pos in monsterLoc:
                                coord = pos[0], pos[1]
                                currentcoord = wrld.me(self).x, wrld.me(self).y
                                dist = abs(self.manhattan_distance(coord, currentcoord))
                                if dist <= 4:
                                    print("DANGER", dist)
                                    danger = True
                            if danger:
                                finds[count] = (Node(x, y, 50))
                            elif wrld.empty_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.exit_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.wall_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.bomb_at(x, y):
                                finds[count] = (Node(x, y, 10))
                            elif wrld.explosion_at(x, y):
                                finds[count] = (Node(x, y, 10))
                            elif wrld.monsters_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.characters_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            count += 1
                            danger = False
        return finds

    # Manhattan distance
    def manhattan_distance(self, x1y1, x2y2):
        return abs(x1y1[0] - x2y2[0]) + abs(x1y1[1] - x2y2[1])

    # returns a tuple of the exit. If no exit is found returns (0,0)
    def find_exit(self, wrld):
        w = 0
        h = 0

        while w < wrld.width():
            while h < wrld.height():
                if wrld.exit_at(w, h):
                    return w, h
                h += 1
            w += 1
            h = 0
        return 0, 0

    # heuristic function for A*
    def heuristic(self, a, b):
        (x1, y1) = a[0], a[1]
        (x2, y2) = b[0], b[1]
        return abs(x1 - x2) + abs(y1 - y2)

    # A* implementation
    def astar(self, wrld, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)

        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current[0] == -1 or current[1] == -1:
                continue

            if current == goal:
                break

            # just finished making the check get_neighbors, now time to change this part to the new method and make it work
            i = 0
            neighbors = self.get_neighbors(wrld, current[0], current[1])

            for node in neighbors:
                new_cost = cost_so_far[current] + node.score
                if node.x == -1 or node.y == -1:
                    continue
                if (node.x, node.y) not in cost_so_far or new_cost < cost_so_far[(node.x, node.y)]:
                    cost_so_far[(node.x, node.y)] = new_cost
                    priority = new_cost + self.heuristic(goal, current)
                    frontier.put((node.x, node.y), priority)
                    came_from[(node.x, node.y)] = current
                i+=1

        path = came_from, cost_so_far
        newpath = self.make_sense_of_path(path, start, goal)
        return newpath

    # returns the path from goal node to start node
    def make_sense_of_path(self, path, start, goal):
        current = path[0][goal]
        newpath = [goal]

        while current != start:
            newpath.append(current)
            current = path[0][current]

        return newpath

    def getMove(self, path, wrld):
        pathLength = len(path) - 1
        nextMove = path[pathLength]

        newMove = nextMove[0] - wrld.me(self).x, nextMove[1] - wrld.me(self).y

        return newMove

    def getSafe(self, wrld, x, y):
        unsafe = []
        safe = [(0,0), (0,1), (0,-1), (1,0), (-1,0), (1,1), (-1, -1), (1,-1), (-1,1)]

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                current = (dx, dy)
                if x + dx < wrld.width() and y + dy < wrld.height():
                    if wrld.wall_at(x + dx, y+dy):
                        if current in safe:
                            unsafe.append(current)
                            safe.remove(current)
                # check for monsters
                for i in range(-3, 3):
                    for j in range(-3, 3):
                        if x + dx + i < wrld.width():
                            if y + dy + j < wrld.height():
                                if wrld.monsters_at(x+dx+i, y+dy+j) and i in range(-2, 2) and j in range(-2,2):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.bomb_at(x + dx + i, y + dy + j) and i in range(-3, 3) and j in range(-3,3):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)
                                if wrld.explosion_at(x + dx + i, y + dy + j) and i in range(-1, 1) and j in range(-1,1):
                                    if current in safe:
                                        unsafe.append(current)
                                        safe.remove(current)

        return safe


    def find_monsters(self, wrld):
        i = 0
        j = 0
        monsterpos = []

        while i < wrld.width():
            while j < wrld.height():
                if wrld.monsters_at(i, j):
                    monster = (i, j)
                    monsterpos.append(monster)
                j+=1
            i+=1
            j=0
        return monsterpos

    # returns the distance to the nearest monster normalized between 0.0 and 1.0
    def ft_monster_distance(self, wrld, x, y):
        closestMonster = -1
        i = 0
        monsters = self.find_monsters(wrld)
        for pos in monsters:
            current = abs(pos[0] - x) + abs(pos[1] - y)
            if current < closestMonster or closestMonster == -1:
                closestMonster = current

        if closestMonster == -1:
            closestMonster == 0
            return 0

        return 1/(1+closestMonster)

    # returning reasonable numbers
    # returns distance to exit normalized between 0.0 and 1.0
    def ft_exit_distance(self, wrld, x, y):
        exit = self.find_exit(wrld)
        first = abs(exit[0] - x) + abs(exit[1] - y)
        return 1/(1+first)

    # returning good numbers
    # retuns the 8 - the number of free moves normalized between 0.0 and 1.0
    def ft_trapped(self, wrld, x, y):
        surroundings = self.check_surroundings(wrld, x, y)
        moves = self.getSafe(wrld, x, y)
        if len(moves) < 3:
            return 1
        else:
            return 0

    
    def save_qchoice(self, wrld, x, y, ft0):
        ft1 = self.ft_monster_distance(wrld, x, y)
        ft2 = self.ft_exit_distance(wrld, x, y)
        ft3 = self.ft_trapped(wrld, x, y)
        ft4 = self.ft_bomb_distance(wrld,x,y)
        ft5 = self.ft_isInBombRange(wrld,x,y)

        # save the values for next iteration to update weights
        f.open("features.txt","W")
        for ft in [ft0,ft1,ft2,ft3,ft4,ft5]:
            f.write(ft)
        f.close()
        
        f.open("qval.txt","W")
        f.write(self.calc_qvalue(wrld,x,y,ft0))
        f.close()

    # calculate q value for the given location
    def calc_qvalue(self, wrld, x, y, ft0):
    
        
        f = open("weights.txt")
        weights = f.read().splitlines()
        print(weights[0], weights[1], weights[2], weights[3], weights[4], weights[5])
        
    
        w0=float(weights[0])
        w1=float(weights[1])
        w2=float(weights[2])
        w3=float(weights[3])
        w4=float(weights[4])
        w5=float(weights[5])
        
    
        f.close()
        
        ft1 = self.ft_monster_distance(wrld, x, y)
        ft2 = self.ft_exit_distance(wrld, x, y)
        ft3 = self.ft_trapped(wrld, x, y)
        ft4 = self.ft_bomb_distance(wrld,x,y)
        ft5 = self.ft_isInBombRange(wrld,x,y)

        # save the values for next iteration to update weights
        

        return w0*ft0 + w1*ft1 + w2*ft2 + w3*ft3 + w4*ft4 + w5*ft5

    # go through next possible moves and generate a qvalue for each, return the best
    def calc_best_next_state(self, wrld, x, y):
        possibleMoves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        bestQValue = 0

        for r in possibleMoves:
            next_x = x + r[0]
            next_y = y + r[1]
            if next_x in range(wrld.width()) and next_y in range(wrld.height()):
                newQValue = self.calc_qvalue(wrld, x+r[0], y+r[1], 0)
                if newQValue > bestQValue:
                    bestQValue = newQValue

        return bestQValue


    # calculate the new weights
    def calc_weights(self, difference):
        f = open("features.txt")
        fts = f.read().splitlines()
    
        ft0=float(fts[0])
        ft1=float(fts[1])
        ft2=float(fts[2])
        ft3=float(fts[3])
        ft4=float(fts[4])
        ft5=float(fts[5])
    
        f.close()
    
        f = open("weights.txt")
        weights = f.read().splitlines()
        print(weights[0], weights[1], weights[2], weights[3], weights[4], weights[5])
        
    
        w0=float(weights[0])
        w1=float(weights[1])
        w2=float(weights[2])
        w3=float(weights[3])
        w4=float(weights[4])
        w5=float(weights[5])
        
    
        f.close()
        # wi = wi + learning rate * difference * calculated value
        w1 = w1 + self.lrate * difference * ft1
        w2 = w2 + self.lrate * difference * ft2
        w3 = w3 + self.lrate * difference * ft3
        w4 = w4 + self.lrate * difference * ft4
        w5 = w5 + self.lrate * difference * ft5
        
        i = 0
        f = open("weights.txt", "w")
        while i < 6:
            if i == 0:
                str0 = "%f\n" % self.w0
                f.write(str0)
            if i == 1:
                str1 = "%f\n" % self.w1
                f.write(str1)
            if i == 2:
                str2 = "%f\n" % self.w2
                f.write(str2)
            if i == 3:
                str3 = "%f\n" % self.w3
                f.write(str3)
            if i == 4:
                str4 = "%f\n" % self.w4
                f.write(str4)
            if i == 5:
                str5 = "%f\n" % self.w5
                f.write(str5)
            i += 1
        f.close()

    # if there is a monster within the given range
    def monsterNear(self, wrld, x, y):
        for r in range (-4,4):
            for c in range (-4,4):
                if r + x < wrld.width():
                    if y + c < wrld.height():
                        if wrld.monsters_at(r+x, y+c):
                            return True
        return False


    # main qlearning function
    def qLearn(self, wrld, x, y, a_star):
        possibleMoves = [(0,0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        bestQValue = -100
        bestQMove = (0,0)
        qvals = dict()
        # iterate through all possible moves for character and monster
        for char in possibleMoves:
            if char == a_star:
                is_a_star = 1
            else:
                is_a_star = 0
            currCharPos = x + char[0], y + char[1]
            if wrld.wall_at(currCharPos[0], currCharPos[1]):
                qvals[char] = -10000
                continue
            
            wrld.me(self).move(char[0], char[1])

            #go through all the possible monster positions
            wrld2, events = wrld.next()

            # calculate the q value of the new state
            newQValue = self.calc_qvalue(wrld2, wrld2.me(self).x, wrld2.me(self).y, is_a_star)
            # if this is the best qvalue for a state found so far, save it
            qvals[char] = newQValue
            if newQValue > bestQValue:
                bestQValue = newQValue
                bestQMove = char
            

        # return best possible move
        
        return bestQMove, qvals
        
    def ft_bomb_distance(self, wrld, x, y):
        for i in range(0, wrld.width()):
            for j in range(0, wrld.height()):
                if wrld.bomb_at(i,j):
                    dist = abs(i - x) + abs(j - y)
                    return 1/(1+dist)
                    
    def ft_isInBombRange(self, wrld, x,y):
        bomb_range = wrld.expl_range
        for i in range(0, wrld.width()):
            for j in range(0, wrld.height()):
                if wrld.bomb_at(i,j):
                    if i == x:
                        if abs(j - y) <= bomb_range:
                            return 1
                    elif j == y:
                        if abs(i - x) <= bomb_range:
                            return 1
        return 0
                
    def send_move(self,wrld,move,is_astar):
        wrld.me(self).move(move[0], move[1])
        w2 = wrld.next()
        me2 = w2.me(self)
        self.save_qchoice(w2, me2.x, me2.y, is_astar)
        self.followed_q = True
        self.move(move[0],move[1])
        
    def update_w():
        f.open("reward.txt")
        rw = float(f.read().splitlines()[0])
        f.close()
        actualQValue = rw + self.discount * self.calc_best_next_state(wrld, me.x, me.y)
        f.open("qval.txt")
        q = float(f.read().splitline[0])
        f.close()
        diff = actualQValue - q
        self.calc_weights(diff)
        
    def do(self, wrld):
        me = wrld.me(self)
        if self.followed_q:
            self.update_w()
        surroundings = self.check_surroundings(wrld, me.x, me.y)
         #First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1][0][0], surroundings[1][0][1])
        start = me.x, me.y
        goal = self.find_exit(wrld)

        path = self.astar(wrld, start, goal)
        astar_move = self.getMove(path, wrld)
        
        move, all_moves = self.qLearn(wrld, me.x, me.y, astar_move)
        if wrld.wall_at(x + astar_move[0], y + astar_move[1]):
            threshold = 100
            stay_score = all_moves[(0,0)]
            if stay_score > threshold:
                self.followed_q = False
                self.place_bomb()
        
        if move == astar_move:
            is_astar = True
        else:
            is_astar = False
            
        self.send_move(wrld, move, is_astar)

    # if the game is ended either by death or winning
    def done(self, wrld):
        f.open("reward.txt", "w")
        me = wrld.me(self)
        if wrld.exit_at(me.x,me.y):
            f.write("1000")
        elif wrld.explosion_at(me.x,me.y):
            f.write("-1000")
        elif wrld.monster_at(me.x,me.y):
            f.write("-1000")
        else:
            f.write("-0.1")
        f.close()
        print("NEW WEIGHTS CALCULATED AT END OF GAME")




