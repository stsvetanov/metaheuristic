# -*- coding: utf-8 -*-
"""
Hill Climbing aka Gradient Descent is local search method.

@author: Simeon Tsvetanov
"""
import random
import matplotlib.pyplot as plt

solutions = [3, 5, 6, 7, 8, 6, 4, 3, 2, 5, 6, 7, 9, 23, 35, 12, 6, 5, 4, 10, 15, 13, 8, 9, 12, 15, 4]
x_axis_len = len(solutions)
plt.axis([0, x_axis_len, 0, 35])
for idx, value in enumerate(solutions):
    plt.plot(idx, value, 'ro')
plt.show()


def gradient():
    s = random.randrange(len(solutions) - 1)    
    print("Initial Solution {} -> Cost {}".format(s, solutions[s]))
    
    while solutions[s] < solutions[s + 1] or solutions[s] < solutions[s - 1]:
        if solutions[s] < solutions[s + 1]:
            s += 1
        else:
            s += 1
        print("Current best solution value: ", solutions[s])
    return solutions[s]
 
number_of_iteration = 1
best_solution = 0 # Iterative Local Search extends Hill Climbing

for _ in range(number_of_iteration):
    s = gradient()
    if best_solution < s:
        best_solution = s
       
print("Best solutions", best_solution)

"""
TO DO
Add search in math functions
Add visual representation
"""