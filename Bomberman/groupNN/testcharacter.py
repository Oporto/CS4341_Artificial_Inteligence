# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    #checks for type of cell in surrounding, giving the list direction tuples as a return
    # type 1 is exit
    # type 2 is monster
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
                                finds[0].append(dx,dy)
                            elif (wlrd.exit_at(x,y)):
                                finds[1].append(dx,dy)
                            elif (wlrd.wall_at(x,y)):
                                finds[2].append(dx,dy)
                            elif (wlrd.bomb_at(x,y)):
                                finds[3].append(dx,dy)
                            elif (wlrd.explosion_at(x,y)):
                                finds[4].append(dx,dy)
                            elif (wlrd.monsters_at(x,y)):
                                finds[5].append(dx,dy)
                            elif (wlrd.characters_at(x,y)):
                                finds[6].append(dx,dy)
        return finds;
    def do(self, wrld):
        # Your code here
        # First check if exit is 1 move away
        me = wrld.me(self)
        surroundings = check_surroundings(wlrd, me.x, me.y)
        if len(surroundings[1]) > 0:
            #return surroundings[1][0]
        
        pass
