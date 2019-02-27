# This is necessary to find the main code
import sys
import heapq
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

    # the location of the character TODO update each iteration
    currentLoc = (0, 0)


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
    def check_surroundings(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = dict([(i,[]) for i in range(7)])
        count = 0
        
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
                            if wrld.empty_at(x,y):
                                finds[0] = (dx, dy)
                            elif wrld.exit_at(x,y):
                                finds[1] = (dx, dy)
                            elif wrld.wall_at(x,y):
                                finds[2] = (dx, dy)
                            elif wrld.bomb_at(x,y):
                                finds[3] = (dx, dy)
                            elif wrld.explosion_at(x,y):
                                finds[4] = (dx, dy)
                            elif wrld.monsters_at(x,y):
                                finds[5] = (dx, dy)
                            elif wrld.characters_at(x,y):
                                finds[6] = (dx, dy)
                            count += 1
        return finds

    # returns nodes surrounding the current position of the character
    def get_neighbors(self, wrld, thisx, thisy):
        # First check if exit is 1 move away\
        finds = [0]*4
        count = 0

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
                            # Check cases
                            if dx == 1 and dy == 1 :
                                print("nah")
                            elif dx == -1 and dy == -1 :
                                print("nah")
                            elif wrld.empty_at(x, y):
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
        return finds

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
        frontier.put(Node(wrld.me(self).x, wrld.me(self).y, 0), 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        grid = self.constructGrid(wrld)

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            # just finished making the check surroundings2, now time to change this part to the new method and make it work
            i = 0
            neighbors = self.get_neighbors(wrld, wrld.me(self).x, wrld.me(self).y)

            while i < len(neighbors):
                new_cost = cost_so_far[current] + 1
                if neighbors[i] not in cost_so_far or new_cost < cost_so_far[neighbors[i].cost]:
                    cost_so_far[neighbors[i]] = new_cost
                    priority = new_cost + self.heuristic(goal, neighbors[i])
                    frontier.put(next, priority)
                    came_from[next] = current
                i+=1

        return came_from, cost_so_far

    def do(self, wrld):
        # Your code here
        # First check if exit is 1 move away
        me = wrld.me(self)
        surroundings = self.check_surroundings(wrld, me.x, me.y)
        if len(surroundings[1]) > 0:
            return surroundings[1][0]

        # Get the current location and the exit location (if possible)
        start = wrld.me(self).x, wrld.me(self).y
        goal = self.find_exit(wrld)
        newsurroundings = self.get_neighbors(wrld, me.x, me.y)

        grid = self.constructGrid(wrld)
        self.printGrid(wrld, grid)
        #path = self.astar(wrld, start, goal)

        pass



