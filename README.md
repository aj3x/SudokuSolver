# Sudoku Solver
## Intro
Input using a basic GUI interface, this program will give a solution to any sudoku board, if it exists.

## Abstract
This is a trial and error algorithm that reduces the number of searches required by quickly reducing the number of possible outcomes at every step. 

## Algorithm
First create an array of 9 True elements for every square in the grid. If any block contains a number remove that number from the array of intersecting squares, this will tell us which numbers are still available for a given square. Sort the list of unfilled squares from fewest possiblities to highest. 
Go through this list, filling in all the squares with only one possibility. Once we run out of singles, make a guess as to which number is the correct one for a given square and save this decision in a list. If a dead end or contradiction is encountered jump back to the previous decision and try the other path. Continue until either the problem is solved or all possibilites are looked through.
