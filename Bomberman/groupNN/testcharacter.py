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
        # First check if exit is 1 move away
        m = wrld.me(self)
        for dx in [-1, 0, 1]:
            finds = []
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
                                finds.append((x,y,0))
                            elif (wlrd.exit_at(x,y)):
                                finds.append((x,y,1))
                            elif (wlrd.wall_at(x,y)):
                                finds.append((x,y,2))
                            elif (wlrd.bomb_at(x,y)):
                                finds.append((x,y,3))
                            elif (wlrd.explosion_at(x,y)):
                                finds.append((x,y,4))
                            elif (wlrd.monsters_at(x,y)):
                                finds.append((x,y,5))
                            elif (wlrd.characters_at(x,y)):
                                finds.append((x,y,6))
        return finds;
    def do(self, wrld):
        # Your code here
        # First check if exit is 1 move away
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (m.x+dx >=0) and (m.x+dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (m.y+dy >=0) and (m.y+dy < wrld.height()):
        pass
