# CS4341_Artificial_Inteligence

Official WPI Course Description:
CS 4341. INTRODUCTION TO ARTIFICIAL INTELLIGENCE Cat. I This course studies the problem of making computers act in ways which we call "intelligent". Topics include major theories, tools and applications of artificial intelligence, aspects of knowledge representation, searching and planning, and natural language understanding. Students will be expected to complete projects which express problems that require search in state spaces, and to propose appropriate methods for solving the problems.

Projects in this course:
# HW1:
  Exercise 1 - ex1.py - (**Terminal state scoring for Connect-4 board game**): Connect-4 is a turn-based two-player game in which you win if you can string four of your tokens in a horizontal, vertical, or diagonal sequence. In this exercise, a Python class was created in order to, given a board  configuration, calculate its outcome. 
          Expected Output:
          W = 7
          H = 6
          BOARD1 = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
          c = ConnectFour(BOARD1 , W, H)
          c.printOutcome ()
          # No winner
          BOARD2 = [[1,1,1,1,2,1,0],[0,2,2,2,0,0,0],[0,0,2,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
          c = ConnectFour(BOARD2 , W, H)
          c.printOutcome ()
          # Player 1 won
  Exercise 2 - ex2.py - (**Recursion**): Created a recursive function that takes two strings and checks if they are the reverse of each other
          Expected Output:
          print("<empty >, <empty > -> ", isreverse("", ""))# True
          print("a, a -> ", isreverse("a", "a"))# True
          print("ab , ba -> ", isreverse("ab", "ba"))# True
          print("abc , cba  -> ", isreverse("abc", "cba"))# True
          print("abcd , cba  -> ", isreverse("abcd", "cba"))# False
  Exercise 3 - ex3.py - (**Jaccard Index**): Wrote a program that calculates the Jaccard Index of two text files. The purpose of this coefficient is to generate a crude estimate of the similarity of two text files, which is useful for natural language processing.
          Expected Output:
          FNAME1 = "alice_ascii.txt"
          FNAME2 = "glass_ascii.txt"
          print("Jaccard  index  between", FNAME1 , "and", FNAME2 , jaccard(FNAME1 , FNAME2 ))
          # Jaccard  index  between  alice_ascii.txt (Alice in Wonderland) and  glass_ascii.txt (Through the looking glass)
          # 0.4730329208498716
# HW2:
