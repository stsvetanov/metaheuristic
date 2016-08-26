import random
import string

tsp = [[0, 2, 5, 3, 2], [2, 0, 2, 3, 2], [5, 2, 0, 1, 3], [3, 3, 1, 0, 1], [2, 2, 3, 1, 0]]


def generate_solution(solution_size):
    for ch in range(solution_size):
        solution = "".join((random.choice(string.ascii_letters + " " + string.digits) for _ in range(solution_size)))
        # solution = "".join((random.choice(string.digits) for x in range(solution_size)))
    return solution


def generate_population(target, population_size):
    solution_size = len(target)
    population = []
    for y in range(population_size):
        population.append(generate_solution(solution_size))
    return population


def estimate_solution(solution: str, target: str) -> int: # In the context of Genetic Algorithms, this function is called "fitness"
    value = 0
    for index, ch in enumerate(solution):
        value += abs(ord(ch) - ord(target[index]))
    return value


def estimate_population(population: list, target: str) -> dict:
    estimated_population = {}
    for solution in population:
        estimated_population[solution] = estimate_solution(solution, target)

    # ordered_population = []
    # for solution, value in estimated_population.items():
    #     ordered_population.append((value, solution))
    # ordered_population.sort()
    # ordered_population.sort()
    # # print(ordered_population)
    return estimated_population


def mutate_population(elite_solutions):
    for index, mutated_solution in enumerate(elite_solutions):
        elite_solutions[index] = mutate_solution(mutated_solution)
    return elite_solutions


def mutate_solution(solution):
    num_low = 0
    num_len = len(solution)
    index = random.randint(num_low, num_len -1)

    mutated_solution = solution[:index] + random.choice(string.ascii_letters + " " + string.digits) + solution[index + 1:]
    return mutated_solution


def select_population(estimated_population: dict):
    selection = sorted(estimated_population, key=lambda x: estimated_population[x])
    return selection
