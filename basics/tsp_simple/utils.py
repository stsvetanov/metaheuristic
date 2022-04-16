import random
from random import shuffle
import math
import matplotlib.pyplot as plt


def create_tsp_map(number_of_cities):
    min_distance = 1
    max_distance = 10
    tsp_map = [[random.randint(min_distance, max_distance) for x in range(number_of_cities)] for y in range(2)]
    return tsp_map


def generate_solution_tsp(solution_size):
    solution = [i for i in range(solution_size)]
    shuffle(solution)
    return solution


def generate_population_tsp(solution_size, population_size):
    population = []
    for y in range(population_size):
        population.append(generate_solution_tsp(solution_size))
    return population


def estimate_solution_tsp(solution: str, tsp: list) -> int:
    value = 0
    solution_len = len(solution)
    for index in range(solution_len - 1):
        city = solution[index]
        next_city = solution[index + 1]
        value += distance(tsp, city, next_city)
    return value


def distance(tsp, i, j):
    dx = tsp[0][i] - tsp[0][j]
    dy = tsp[1][i] - tsp[1][j]
    return math.sqrt(dx * dx + dy * dy)


def estimate_population_tsp(population: list, target: str) -> dict:
    estimated_population = {}
    for solution in population:
        estimated_population[tuple(solution)] = estimate_solution_tsp(solution, target)
    return estimated_population


def generate_neighbor_solution_tsp(solution):
    solution_len = len(solution)
    neighbor_solution = []
    for city in solution:
        neighbor_solution.append(city)

    el1 = random.randint(0, solution_len - 2) # pick two random elements to swap
    # element2 = random.randint(0, solution_len - 1)
    neighbor_solution[el1], neighbor_solution[el1 + 1] = neighbor_solution[el1 + 1], neighbor_solution[el1]
    return neighbor_solution


def generate_subglobal_solution_tsp(solution):
    solution_len = len(solution)
    subglobal_solution = []
    for city in solution:
        subglobal_solution.append(city)
    element1 = random.randint(0, solution_len - 2) # pick two random elements to swap
    element2 = random.randint(0, solution_len - 1)
    subglobal_solution[element1], subglobal_solution[element2] = subglobal_solution[element2], subglobal_solution[element1]
    return subglobal_solution


def select_population(estimated_population: dict):
    selection = sorted(estimated_population, key=lambda x: estimated_population[x])
    return selection


def plot_tsp_map(tsp_map):
    plt.plot(tsp_map[0], tsp_map[1], 'ro')
    plt.axis([0, 10, 0, 10])
    plt.show()


def tsp_local_search(number_of_cities=20, number_of_moves=50, solution=None, tsp_map=None):
    # best_solution = None

    if tsp_map is None:
        tsp_map = create_tsp_map(number_of_cities)
    # else:
    #     tsp_map = tsp_map

    if solution is None:
        s = generate_solution_tsp(number_of_cities)
    else:
        s = list(solution)

    e = estimate_solution_tsp(s, tsp_map)

    # print("Initial Solution {} Value  {}".format(s, e))
    for x in range(number_of_moves):
        ss = generate_neighbor_solution_tsp(s)
        ee = estimate_solution_tsp(ss, tsp_map)
        # print("Neighbor Solution ", ss, "Value ", ee)

        if ee < e:  # If neighbor solution is better that current, accept it as current.
            e = ee
            s = ss
    # print("Best Solution:", s, " Value:", e)
    return s


def tsp_ga(number_of_cities=20, number_of_iterations=50, population_size = 100):
    best_solution = None
    tsp_map = create_tsp_map(number_of_cities)
    initial_solutions = generate_population_tsp(number_of_cities, population_size)

    for iterations_counter in range(number_of_iterations):
        estimated_population = estimate_population_tsp(initial_solutions, tsp_map)
        selection = select_population(estimated_population)
        elite_solutions = selection[:50]

        offsprings = crossover_tsp(elite_solutions)
        estimated_offsprings = estimate_population_tsp(offsprings, target)
        selected_offsprings = select_population(estimated_offsprings)

        best_solution_in_generation = selected_offsprings[0]
        best_solution_in_generation_score = estimate_solution_tsp(best_solution_in_generation, tsp_map)

        print("Best solution in iter {} is {} -> {}".format(iterations_counter, best_solution_in_generation, best_solution_in_generation_score))

        if best_solution is None:
            best_solution = best_solution_in_generation

        if estimate_solution_tsp(best_solution_in_generation, tsp_map) < estimate_solution_tsp(best_solution, tsp_map):
            best_solution = best_solution_in_generation

        for solutions in elite_solutions:
            initial_solutions.append(list(solutions))

    print("Best solution {} -> {}".format(best_solution, estimate_solution_tsp(best_solution, tsp_map)))


def crossover_tsp(elite_solutions):
    parent1 = elite_solutions[0]
    parent2 = elite_solutions[1]
    cross_point1 = random.randint(0, len(parent1))
    cross_point2 = random.randint(0, len(parent2))
    consecutive_alleles = parent1[cross_point1, cross_point2]
    offspring1 = 1
    '''
    TODO

    Complete the function using order one crossover
    http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/Order1CrossoverOperator.aspx
    '''
    pass


def tsp_abc(number_of_cities=20, number_of_iterations=50):
    scouts = 151

    workers = 100
    best_solution = None

    tsp_map = create_tsp_map(number_of_cities)

    initial_solutions = generate_population_tsp(number_of_cities, scouts)

    for iterations_counter in range(number_of_iterations):
        estimated_global_solutions = estimate_population_tsp(initial_solutions, tsp_map)
        selected_global_solutions = select_population(estimated_global_solutions)
        local_solutions = workers_activities(tsp_map, workers, selected_global_solutions[:scouts], number_of_cities)
        estimated_local_solutions = estimate_population_tsp(local_solutions, tsp_map)
        selected_local_solutions = select_population(estimated_local_solutions)
        elite_solutions = selected_local_solutions[:scouts]
        best_solution_in_generation = selected_local_solutions[0]
        best_solution_in_generation_score = estimate_solution_tsp(best_solution_in_generation, tsp_map)

        print("Best solution in iter {} is {} -> {}".format(iterations_counter, best_solution_in_generation, best_solution_in_generation_score))

        if best_solution is None:
            best_solution = best_solution_in_generation

        if estimate_solution_tsp(best_solution_in_generation, tsp_map) < estimate_solution_tsp(best_solution, tsp_map):
            best_solution = best_solution_in_generation

        initial_solutions = scouts_activities(elite_solutions)
        for solutions in elite_solutions:
            initial_solutions.append(list(solutions))

    print("Best solution {} -> {}".format(best_solution, estimate_solution_tsp(best_solution, tsp_map)))


def workers_activities(tsp_map, workers, selected_global_solutions, number_of_cities):
    solutions = []
    counter = 0
    dev = 2
    for s in selected_global_solutions:
        for _ in range(int(workers / dev)):
            solutions.append(tsp_local_search(tsp_map=tsp_map, number_of_moves=50, solution=s, number_of_cities=number_of_cities))
            dev *= 2
        if counter > 3:
            break
    return solutions


def scouts_activities(initial_solutions):
    global_solutions = []
    for solution in initial_solutions:
        global_solutions.append(generate_subglobal_solution_tsp(list(solution)))
    return global_solutions