## CS4341_Artificial_Inteligence

Official WPI Course Description:
CS 4341. INTRODUCTION TO ARTIFICIAL INTELLIGENCE Cat. I This course studies the problem of making computers act in ways which we call "intelligent". Topics include major theories, tools and applications of artificial intelligence, aspects of knowledge representation, searching and planning, and natural language understanding. Students will be expected to complete projects which express problems that require search in state spaces, and to propose appropriate methods for solving the problems.

Projects in this course:
# Misc_Exercises:
ex1.py - (**Terminal state scoring for Connect-4 board game**): 
  Connect-4 is a turn-based two-player game in which you win if you can string four of your tokens in a horizontal, vertical, or diagonal sequence. In this exercise, a Python class was created in order to, given a board  configuration, calculate its outcome.
  
          *Expected Output:*
          *W = 7
          H = 6
          BOARD1 = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
          c = ConnectFour(BOARD1 , W, H)
          c.printOutcome ()
          # No winner
          BOARD2 = [[1,1,1,1,2,1,0],[0,2,2,2,0,0,0],[0,0,2,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
          c = ConnectFour(BOARD2 , W, H)
          c.printOutcome ()
          # Player 1 won*
ex2.py - (**Recursion Exercise**): Created a recursive function that takes two strings and checks if they are the reverse of each other
          
          Expected Output:
          print("<empty >, <empty > -> ", isreverse("", ""))# True
          print("a, a -> ", isreverse("a", "a"))# True
          print("ab , ba -> ", isreverse("ab", "ba"))# True
          print("abc , cba  -> ", isreverse("abc", "cba"))# True
          print("abcd , cba  -> ", isreverse("abcd", "cba"))# False
ex3.py - (**Jaccard Index**): Wrote a program that calculates the Jaccard Index of two text files. The purpose of this coefficient is to generate a crude estimate of the similarity of two text files, which is useful for natural language processing.
          
          Expected Output:
          FNAME1 = "alice_ascii.txt"
          FNAME2 = "glass_ascii.txt"
          print("Jaccard  index  between", FNAME1 , "and", FNAME2 , jaccard(FNAME1 , FNAME2 ))
          # Jaccard  index  between  alice_ascii.txt (Alice in Wonderland) and  glass_ascii.txt (Through the looking glass)
          # 0.4730329208498716
# Connect-N_AI:
The aim of this project is to make an AI for the game ConnectN, which is a more general version of Connect-4. If you don’t know Connect-4, try it out here: https://www.gimu.org/connect-four-js/jQuery/alphabeta/index.html. The AI for this assignment was done using a Mini-Max Alpha-Beta algorithm that explores board states up to a certain pre-determined depth and uses a heuristic function to evaluate the leaf nodes of the search. At the end of the assignment, the Alpha-Beta-Agent class of each student was instantiated for a class tournament, with a time limit of 15 seconds per turn. The developed code is in alpha_beta_agent.py, while the game and tournament programs were provided by the Professor.

**Board State Heuristic**

The strategy for evaluating a board is counting the number of sequences of N cells that could in future turns become a winning Connect-N sequence. This means these sequences have a combination of empty cells and cells from only one player. The value of this sequence is then evaluated based on how many cells from that player are in that sequence. For example (for N = 4): “0010”, “1000”, and “0200” are sequences of value 1; “0101”, “0110” and “2200” are sequences of value 2; “1110”, “0222” and “1101” are sequences of value 3; “1111” and “2222” are sequences of value 4; “0000”, “2100”, “1112” and “2121” are sequences of value 0. It also stores the score weights for each of those sequences. With both players scores calculated, the heuristic function combines them using an offensiveness/defensiveness weight balancing. Several heuristics functions with this algorithm were compared. The variation between them was with the offensiveness and score_weights parameters.

**Min-Max Alpha-Beta pruning**

The utility function was wrapped inside the max_value and min_value functions of the min-max alpha-beta algorithm provided by the lecture. In addition, the max_value function also returns the action a which corresponds to the column number that a piece would be placed next for the corresponding utility that is returned by the function. This is only needed for when it returns to the go function, which needs to know which action to take as the AI player. Furthermore, the terminal test was broken down into three major steps. The max_value and min_value functions first check if the given board state has a winner. If there is a winner, it returns very high or low values as the utility, depending on who is winning. It then checks for a tie, or if the state has not more possible plays to be made. Lastly, it checks if the pruning reached the maximum given depth, which then triggers it to call the utility function on the given state. Lastly, the depth of the search can be determined by the class instantiation, but a heuristic function to determine the max depth of a single turn based on the given board state was created. It predicts that the number of pruned nodes and the width of the search tree will reduce as the game goes on, allowing the maximum depth to be higher within the same time frame.

**Apha-Beta Agent testing and optimization**

By testing multiple agents against each other and against random players, different parameters on instantiation (offensiveness and score weights) were tested. At first, very distinct values were alternated, and smaller variations were then made on the winning configurations for a new tournament set and so on. This primitive iteration of the agent’s configuration could be in the future improved by using a genetic algorithm running tournaments within generations. The genetic “code” would be the combination of the offensiveness and score weights attributes.

