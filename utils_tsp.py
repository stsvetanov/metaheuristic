import random
from random import shuffle
import math


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
    element1 = random.randint(0, solution_len - 1) # pick two random elements to swap
    element2 = random.randint(0, solution_len - 1)
    solution[element1], solution[element2] = solution[element2], solution[element1]
    return solution


def select_population(estimated_population: dict):
    selection = sorted(estimated_population, key=lambda x: estimated_population[x])
    return selection
