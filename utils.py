import random


def generate_solution(solution_size):
    num_low = 0
    num_high = 9
    solution = ''
    for ch in range(solution_size):
        solution += str(random.randint(num_low, num_high))
    return solution


def estimate_solution(solution: str, target: str) -> int: # In the context of Genetic Algorithms, this function is called "fitness"
    value = 0
    for index, ch in enumerate(solution):
        value += abs(int(ch) - int(target[index]))
    return value


def generate_population(target, population_size):
    solution_size = len(target)
    population = []
    for y in range(population_size):
        population.append(generate_solution(solution_size))
    return population