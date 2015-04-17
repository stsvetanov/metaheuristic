# -*- coding: utf-8 -*-
"""
Hill climbing aka Gradient Desent is local search method.

@author: Simeon Tsvetanov
"""

import random
solutions = [3,5,6,7,8,6,4,3,2,5,6,7,9,23,35,12,6,5,4,10,15,13,8,9,12,15,4]
    
def HillClimbing():
    s = random.randrange(len(solutions) - 1)    
    print("Initial Value", solutions[s], "Initial Index", s)
    
    while(solutions[s] < solutions[s + 1] or solutions[s] < solutions[s - 1]):
        if (solutions[s] < solutions[s + 1]):       
            s = s + 1
        else:
            s = s - 1
        print("Current best solution value: ", solutions[s])
    return solutions[s]
 
iter = 5
Best_ILS = 0 # Iterative Local Search extends Hill Climbing

for x in range(0, iter):
    s = HillClimbing()
    if(Best_ILS < s):
        Best_ILS = s
       
print("Best solutions", Best_ILS)

"""
TO DO
Add functionality to search in both directions
Add search in math functions
Add visual representation
"""