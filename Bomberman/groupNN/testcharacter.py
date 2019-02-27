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
    def get_safe_moves(wrld, surroundings, me):
        safe = [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if me.x + dx in range(0,wrld.width) and me.y in range(0,wrld.height)]
        #Bomb, monster, explosion and character check
        for dir in surroundings[3]:
            safe.remove(dir)
        for dir in surroundings[4]:
            safe.remove(dir)
        for dir in surroundings[5]:
            safe.remove(dir)
        for dir in surroundings[6]:
            safe.remove(dir)
        #Check for bomb range
        bomb_range = wrld.expl_range
        for (dx,dy) in safe:
            #x direction
            for i in range(-bomb_range, bomb_range+1):
                if i != 0 and me.x + i in range(0,wlrd.width) and wrld.bomb_at(me.x + i, me.y):
                    safe.remove((dx,dy))
                    break;
        for (dx,dy) in safe:
            #y direction
            for j in range(-bomb_range, bomb_range+1):
                if j != 0 and me.y + j in range(0,wlrd.height) and wrld.bomb_at(me.x , me.y + j):
                    safe.remove((dx,dy))
                    break;
        
        #Check cells near monster
        monst_range = 2
        for (dx,dy) in safe:
            for i in range(-monst_range, monst_range+1):
                for j in range(-monst_range, monst_range+1):
                    check_x = me.x+dx+i
                    check_y = me.y+dy+j
                    if check_x > 0 and check_x < wlrd.width and check_x != me.x:
                        if check_y > 0 and check_y < wlrd.height and check_y != me.y:
                            if wlrd.monster_at(check_x, check_y):  
                                safe.remove((dx,dy))
        return safe;
        
    def do(self, wrld):
        # Your code here
        
        me = wrld.me(self)
        surroundings = self.check_surroundings(wlrd, me.x, me.y)
        # First check if exit is 1 move away
        if len(surroundings[1]) > 0:
            self.move(surroundings[1][0])
            pass
        safe_moves = self.get_safe_moves(wlrd, surroundings, me.x, me.y)
        move_x, move_y = next(itr(safe_moves))
        self.move(move_x, move_y)
        pass
