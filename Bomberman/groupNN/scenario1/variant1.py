# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(TestCharacter("Quinn", # name
                              "Q",  # avatar
                              0, 0, # position
                              "weight1v1.txt" # filename for the learned weights
))

# Run!
g.go()
