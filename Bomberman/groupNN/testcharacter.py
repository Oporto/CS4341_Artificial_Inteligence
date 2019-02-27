# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

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
                            if (wlrd.empty_at(x,y)):
                                ls = finds[0]
                                ls.append(dx,dy)
                                finds[0] = ls
                            elif (wlrd.exit_at(x,y)):
                                ls = finds[1]
                                ls.append(dx,dy)
                                finds[1] = ls
                            elif (wlrd.wall_at(x,y)):
                                ls = finds[2]
                                ls.append(dx,dy)
                                finds[2] = ls
                            elif (wlrd.bomb_at(x,y)):
                                ls = finds[3]
                                ls.append(dx,dy)
                                finds[3] = ls
                            elif (wlrd.explosion_at(x,y)):
                                ls = finds[4]
                                ls.append(dx,dy)
                                finds[4] = ls
                            elif (wlrd.monsters_at(x,y)):
                                ls = finds[5]
                                ls.append(dx,dy)
                                finds[5] = ls
                            elif (wlrd.characters_at(x,y)):
                                ls = finds[6]
                                ls.append(dx,dy)
                                finds[6] = ls
        return finds;
    def get_safe_moves(surroundings):
        not_safe = set()
        #Bomb, explosion and character check
        for dir in surroundings[3] or in surroundings[3] or in surroundings[6]:
            not_safe.add(dir)
        #monster check
        for dir in surroundings[5]:
            
            if dir[0]*dir[1] == 0:
                
                if dir[0] == 0:
                    lst = [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if dy != -dir[1]]
                elif dir[1] == 0:
                    lst = [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if dx != -dir[0]]
                
            else:
                lst = [(0,0), (dir[0],0), (0,dir[1])]
            not_safe.update(lst)
        safe = [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if (dx,dy) not in not_safe]
        return safe;
        
    def do(self, wrld):
        # Your code here
        
        me = wrld.me(self)
        surroundings = self.check_surroundings(wlrd, me.x, me.y)
        # First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1])
            pass
        safe_moves = self.get_safe_moves(surroundings)
        
        pass
