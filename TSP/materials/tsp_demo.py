import numpy as np
from cvxpy import *
from scipy.spatial.distance import pdist, squareform

# Based on formulation described
#    @ https://en.wikipedia.org/wiki/Travelling_salesman_problem (February 2016)

np.random.seed(1)

N = 5
positions = np.random.rand(N, 2)
distances = squareform(pdist(positions, 'euclidean'))
print(positions)
print(distances)

# VARS
x = Bool(N, N)
u = Int(N)

# CONSTRAINTS
constraints = []
for j in range(N):
    indices = list(range(0, j)) + list(range(j + 1, N))
    constraints.append(sum_entries(x[indices, j]) == 1)
for i in range(N):
    indices = list(range(0, i)) + list(range(i + 1, N))
    constraints.append(sum_entries(x[i, indices]) == 1)

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            constraints.append(u[i] - u[j] + N*x[i, j] <= N-1)

# OBJ
obj = Minimize(sum_entries(mul_elemwise(distances, x)))

# SOLVE
prob = Problem(obj, constraints)
prob.solve(verbose=False)
print(prob.value)
x_sol = np.array(x.value.T)

""" Plotting part """
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, sharex=True, sharey=True)         # Prepare 2 plots
ax[0].set_title('Raw nodes')
ax[1].set_title('Optimized tour')
ax[0].scatter(positions[:, 0], positions[:, 1])             # plot A
ax[1].scatter(positions[:, 0], positions[:, 1])             # plot B
start_node = 0
distance = 0.
for i in range(N):
    start_pos = positions[start_node]
    next_node = np.argmax(x_sol[start_node])
    end_pos = positions[next_node]
    ax[1].annotate("",
            xy=start_pos, xycoords='data',
            xytext=end_pos, textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))
    distance += np.linalg.norm(end_pos - start_pos)
    start_node = next_node

textstr = "N nodes: %d\nTotal length: %.3f" % (N, distance)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14, # Textbox
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()