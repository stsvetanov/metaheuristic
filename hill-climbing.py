# -*- coding: utf-8 -*-
"""
Hill climbing or Gradient Desent is local search method.

@author: Simeon Tsvetanov
"""
import random
solutions = [3,5,6,7,6,4,3,5,6,7,9,23,35,12,6,5,4,23,24,15,13,8,9,12,15,4]

"""
Generate random solutions form the list
s  is the index of the element
solutions[s] is the value of the solution s
"""
s = solutions[random.randrange(len(solutions) -1)]
print("Initial Solution Value: ", solutions[s], "Solution Index: ", s)
while(solutions[s] < solutions[s+1]):
    s=s+1
    print("Current best solution value: ", solutions[s])
    
print("Local maximum found: ", solutions[s])

"""
TO DO
Add functionality to search in both directions
Add search in math functions
Add visual representation
"""