import random
import numpy as np
import matplotlib.pyplot as plt


def load_coordinates(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        data = [[int(coordinates) for coordinates in line.split()] for line in f]
    return np.array(data)


def generate_solution(number_of_cities):
    return random.sample(range(0, number_of_cities), number_of_cities)


def generate_population(number_of_cities, population_size):
    return [generate_solution(number_of_cities) for _ in range(population_size)]


def estimate_solution(solution: list, distance_matrix: list) -> int:
    distance = 0
    for i in range(len(solution)):
        distance += distance_matrix[solution[i-1]][solution[i]]
    return distance


def estimate_population(population: list, distance_matrix: list) -> dict:
    # estimated_population = {}
    # for solution in population:
    #     solution = tuple(solution)
    #     estimated_population[solution] = estimate_solution(solution, distance_matrix)
    # return estimated_population
    estimated_population = {tuple(solution): estimate_solution(solution, distance_matrix) for solution in population}
    sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
    return sorted_population


def sort_population(estimated_population: dict):
    sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
    return sorted_population


def create_local_population(elite_solutions):
    for index, mutated_solution in enumerate(elite_solutions):
        elite_solutions[index] = create_local_solution(mutated_solution)
    return elite_solutions


def create_local_solution(solution):
    mutationRate = 0.03
    solution = list(solution)
    for swapped in range(len(solution)):
        if random.random() < mutationRate:
            swapWith = int(random.random() * len(solution))
            solution[swapWith], solution[swapped] = solution[swapped], solution[swapWith]

    # solution = list(solution)
    # num_low = 0
    # num_len = len(solution)
    # index1, index2 = random.sample(range(num_low, num_len - 1), 2)
    #
    # solution[index1], solution[index2] = solution[index2], solution[index1]

    return solution


def workers_activity(workers, selected_global_solutions, distance_matrix):
    solutions = []
    counter = len(selected_global_solutions)
    for solution in selected_global_solutions:
        for _ in range(workers):
            solutions.append(local_search(counter, solution, distance_matrix))
        counter = int(counter/5)
        if counter < 2:
            break
    return solutions


def local_search(number_of_iter, solution, distance_matrix):
    solution_value = estimate_solution(solution, distance_matrix)
    # print(f"Initial solution: {solution} - {solution_value}")
    for i in range(number_of_iter):
        next_solution = create_local_solution(solution)
        next_solution_value = estimate_solution(next_solution, distance_matrix)
        if next_solution_value < solution_value:
            solution = next_solution
            solution_value = next_solution_value
        # elif random.randint(1, number_of_iter) < i/10:
        #     solution = next_solution
        #     solution_value = next_solution_value
    return solution


def plotTSP(path, points, num_iters=1):
    """
    path: List of lists with the different orders in which the nodes are visited
    points: coordinates for the different nodes
    num_iters: number of paths that are in the path list

    """

    # Unpack the primary TSP path and transform it into a list of ordered
    # coordinates

    x = [];
    y = []
    for i in path:
        x.append(float(points[i][0]))
        y.append(float(points[i][1]))

    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x)) / float(100)


    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                  color='g', length_includes_head=True)

    # Set axis too slitghtly larger than the set of x and y
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()
