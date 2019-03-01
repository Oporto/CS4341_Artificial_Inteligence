# This is necessary to find the main code
import sys
import heapq
import math
import random

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
    lastQValue = 0
    lastft1 = 0
    lastft2 = 0
    lastft3 = 0
    lastxvalue = 0
    lastyvalue = 0

    f = open("weights.txt")
    weights = f.read().splitlines()
    print(weights[0], weights[1], weights[2])
    i = 0

    w1=float(weights[0])
    w2=float(weights[1])
    w3=float(weights[2])

    f.close()



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
            i+=1
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
        return finds

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
                            #for pos in monsterLoc:
                                #coord = pos[0], pos[1]
                                #currentcoord = wrld.me(self).x, wrld.me(self).y
                                #dist = abs(self.manhattan_distance(coord, currentcoord))
                                #if dist <= 4:
                                #    print("DANGER", dist)
                                #    danger = True
                            #if danger:
                             #   finds[count] = (Node(x, y, 50))
                            if wrld.empty_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.exit_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.wall_at(x, y):
                                finds[count] = (Node(x, y, 100))
                            elif wrld.bomb_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.explosion_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.monsters_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            elif wrld.characters_at(x, y):
                                finds[count] = (Node(x, y, 1))
                            count += 1
                            #danger = False
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

    def get_safe_moves(self, wrld, surroundings, me):
        ww = wrld.width()
        wh = wrld.height()
        safe = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if me.x + dx in range(0, ww) and me.y in range(0, wh):
                    safe.add((dx, dy))
        #Bomb, monster, explosion and character check
        if wrld.bomb_at(me.x, me.y):
            safe.remove((0,0))
        for dir in surroundings[3]:
            safe.remove(dir)
        for dir in surroundings[4]:
            safe.remove(dir)
        for dir in surroundings[5]:
            safe.remove(dir)
        for dir in surroundings[6]:
            safe.remove(dir)
        #Check for bomb range
        bomb_range = wrld.expl_range + 1
        notSafeList = set()
        for (dx,dy) in safe:
            #x direction
            for i in range(-bomb_range, bomb_range+1):
                if me.x + dx + i in range(0,wrld.width()) and wrld.bomb_at(me.x +dx+ i, me.y):
                    notSafeList.add((dx,dy))
        for (dx,dy) in safe:
            #y direction
            for j in range(-bomb_range, bomb_range+1):
                if me.y + dy+ j in range(0,wrld.height()) and wrld.bomb_at(me.x , me.y+dy + j):
                    notSafeList.add((dx,dy))
        for x in notSafeList:
            safe.remove(x)
        print("Not Safe List")
        print(notSafeList)
        
        #Check cells near monster
        monst_range = 2
        for (dx,dy) in safe:
            for i in range(-monst_range, monst_range+1):
                for j in range(-monst_range, monst_range+1):
                    check_x = me.x+dx+i
                    check_y = me.y+dy+j
                    if check_x > 0 and check_x < wrld.width() and check_x != me.x:
                        if check_y > 0 and check_y < wrld.height() and check_y != me.y:
                            if wrld.monsters_at(check_x, check_y):
                                safe.remove((dx,dy))
        return safe

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

        # find the monsters
        i = 0
        current = (-1, -1)
        monsters = self.find_monsters(wrld)
        #TODO take more than one monster into account
        if len(monsters) != 0:
            current = monsters[0]

        # astar to the monsters
        start = (x,y)

        if start[0] < 0 or start[1] < 0:
            return 0
        if current[0] < 0 or current[1] < 0:
            return 0

        if start == current:
            return 1

        path = self.astar(wrld, start, current)
        length = len(path)
        return 1/ (1+length)

    # returning reasonable numbers
    # returns distance to exit normalized between 0.0 and 1.0
    def ft_exit_distance(self, wrld, x, y):

        # find the exit
        exit = self.find_exit(wrld)
        start = (x,y)

        #astar to the exit
        if start == exit:
            return 1
        path = self.astar(wrld, start, exit)
        length = len(path)

        return 1/(1+length)

    # returning good numbers
    # retuns the 8 - the number of free moves normalized between 0.0 and 1.0
    def ft_trapped(self, wrld, x, y):
        surroundings = self.check_surroundings(wrld, x, y)
        moves = self.getSafe(wrld, x, y)
        if len(moves) < 3:
            return 1
        else:
            return 0

    def calc_reward(self, wrld, x, y):
        if wrld.monsters_at(x, y):
            print("LOST!!!!!!")
            return -100
        elif wrld.exit_at(x, y):
            print("WIN!!!!!!!")
            return 200
        elif wrld.explosion_at(x, y):
            return -100
        elif wrld.bomb_at(x, y):
            return -100
        return 1

    def end_calc_reward(self, wrld, x, y):
        if wrld.exit_at(x, y):
            return 100
        else:
            return -100

    # calculate q value for the given location
    def calc_qvalue(self, wrld, x, y):
        ft1 = self.ft_monster_distance(wrld, x, y)
        ft2 = self.ft_exit_distance(wrld, x, y)
        ft3 = self.ft_trapped(wrld, x, y)

        print("Exit distance: ", ft2)

        # save the values for next iteration to update weights
        self.lastft1 = ft1
        self.lastft2 = ft2
        self.lastft3 = ft3

        return self.w1*ft1 + self.w2*ft2 + self.w3*ft3

    # go through next possible moves and generate a qvalue for each, return the best
    def calc_best_next_state(self, wrld, x, y):
        possibleMoves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        bestQValue = 0

        for r in possibleMoves:
            if x+r[0] >= wrld.width() or x+r[0] < 0:
                continue
            if y+r[1] >= wrld.height() or y+r[1] < 0:
                continue
            if wrld.wall_at(x+r[0], y+r[1]):
                continue
            newQValue = self.calc_qvalue(wrld, x+r[0], y+r[1])
            if newQValue > bestQValue:
                bestQValue = newQValue

        return bestQValue

    # use to calculate actual value
    def calc_state(self, wrld, x, y):
        return self.calc_reward(wrld, x, y) + self.discount * self.calc_best_next_state(wrld, x, y)

    # calculate the difference between q1 and q2
    def calc_difference(self, q1, q2):
        return q1-q2

    # calculate the new weights
    def calc_weights(self, difference, ft1, ft2, ft3):
        print("FT1, FT2, FT3", ft1, ft2, ft3)

        # wi = wi + learning rate * difference * calculated value
        self.w1 = self.w1 + self.lrate * difference * ft1
        self.w2 = self.w2 + self.lrate * difference * ft2
        self.w3 = self.w3 + self.lrate * difference * ft3
        print("w1, w2, w3: ", self.w1, self.w2, self.w3)

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
    def qLearn(self, wrld, x, y):
        possibleMoves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        bestQValue = -100
        bestQMove = (0,0)
        monsterPos = self.find_monsters(wrld)

        # iterate through all possible moves for character and monster
        for char in possibleMoves:
            currCharPos = x + char[0], y + char[1]

            if currCharPos[0] >= wrld.width() or currCharPos[0] < 0:
                continue
            if currCharPos[1] >= wrld.height() or currCharPos[1] < 0:
                continue
            if wrld.wall_at(currCharPos[0], currCharPos[1]):
                continue
            # add move to be checked
            wrld.me(self).move(char[0], char[1])

            #go through all the possible monster positions
            i = 0
            # generate new world given current state
            wrld2, events = wrld.next()

            # calculate the q value of the new state
            newQValue = self.calc_qvalue(wrld2, currCharPos[0], currCharPos[1])

            # if this is the best qvalue for a state found so far, save it
            if newQValue > bestQValue:
                bestQValue = newQValue
                bestQMove = char
            '''
            for pos in monsterPos:
                for monster in possibleMoves:

                    # check if the move is a wall, ignore if so
                    currMonsPos = pos[0] + monster[0], pos[1] + monster[1]
                    if currMonsPos[0] >= wrld.width() or currMonsPos[0] < 0:
                        continue
                    if currMonsPos[1] >= wrld.height() or currMonsPos[1] < 0:
                        continue
                    if wrld.wall_at(currMonsPos[0], currMonsPos[1]):
                        continue

                    # add monster move to be checked
                    currMonster = wrld.monsters_at(pos[0], pos[1])
                    currMonster[i].move(monster[0], monster[1])

                    # generate new world given current state
                    wrld2, events = wrld.next()

                    # calculate the q value of the new state
                    newQValue = self.calc_qvalue(wrld2, currCharPos[0], currCharPos[1])

                    # if this is the best qvalue for a state found so far, save it
                    if newQValue > bestQValue:
                        bestQValue = newQValue
                        bestQMove = char
                        '''
            i += 1

        # save the best qValue as it will be used to calculate weights in next iteration
        self.lastQValue = bestQValue

        # return best possible move
        return bestQMove


    def do(self, wrld):
        me = wrld.me(self)

        # if we want to update weights
        if self.lastQValue != 0:
            reward = self.calc_reward(wrld, me.x, me.y)
            actualQValue = reward + self.discount * self.calc_best_next_state(wrld, me.x, me.y)
            difference = self.calc_difference(actualQValue, self.lastQValue)
            self.calc_weights(difference, self.lastft1, self.lastft2, self.lastft3)
            print("NEW WEIGHTS CALCULATED AT START OF ITERATION reward: ", reward)

        currentQValue = 0
        newQValue = 0
        bestQValue = 0
        bestQMove = (0,0)

        surroundings = self.check_surroundings(wrld, me.x, me.y)
         #First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1][0][0], surroundings[1][0][1])
        start = me.x, me.y
        goal = self.find_exit(wrld)
        safe_moves = self.get_safe_moves(wrld, surroundings, me)

        #path = self.astar(wrld, start, goal)
        #move = self.getMove(path, wrld)

        #if self.monsterNear(wrld, me.x, me.y):
        move = self.qLearn(wrld, me.x, me.y)

        self.lastxvalue = me.x + move[0]
        self.lastyvalue = me.y + move[1]

        self.move(move[0], move[1])

        print("Move: ", move[0], move[1])
        #print("Exit value: ", self.ft_exit_distance(wrld, 0, 1))
        #print("Monster value: ", self.ft_monster_distance(wrld, 0, 0))

        pos = self.find_monsters(wrld)
        for i in pos:
            print("monster pos: ", i[0], i[1])

        # save the new weights
        i = 0
        f = open("weights.txt", "w")
        while i < 3:
            if i == 0:
                str1 = "%f\n" % self.w1
                f.write(str1)
            if i == 1:
                str2 = "%f\n" % self.w2
                f.write(str2)
            if i == 2:
                str3 = "%f\n" % self.w3
                f.write(str3)
            i += 1
        f.close()
      #  else:
       #     self.move(move[0], move[1])

    # if the game is ended either by death or winning
    def done(self, wrld):
        reward = self.end_calc_reward(wrld, self.lastxvalue, self.lastyvalue)
        actualQValue = reward + self.discount * self.calc_best_next_state(wrld, self.lastxvalue, self.lastyvalue)
        difference = self.calc_difference(actualQValue, self.lastQValue)
        self.calc_weights(difference, self.lastft1, self.lastft2, self.lastft3)

        print("NEW WEIGHTS CALCULATED AT END OF GAME REWARD: ", reward)

        # save the new weights
        i = 0
        f = open("weights.txt", "w")
        while i < 3:
            if i == 0:
                str1 = "%f\n" % self.w1
                f.write(str1)
            if i == 1:
                str2 = "%f\n" % self.w2
                f.write(str2)
            if i == 2:
                str3 = "%f\n" % self.w3
                f.write(str3)
            i += 1
        f.close()
