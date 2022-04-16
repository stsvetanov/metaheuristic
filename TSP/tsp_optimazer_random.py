import random

import numpy as np
from scipy.spatial.distance import pdist, squareform

np.random.seed(1)
N = 20
city_coordinates = np.random.rand(N, 2)

distance_matrix = squareform(pdist(city_coordinates, 'euclidean'))
print(distance_matrix)


def estimate_solution(solution: list, distance_matrix: list) -> int:
    distance = 0
    for i in range(N):
        distance += distance_matrix[solution[i-1]][solution[i]]
    return distance


def generate_solution(number_of_cities):
    return random.sample(range(0, number_of_cities), number_of_cities)


def search(number_of_iter):
    solution = generate_solution(N)
    solution_value = estimate_solution(solution, distance_matrix)
    print(f"Initial solution: {solution} - {solution_value}")
    for _ in range(number_of_iter):
        next_solution = generate_solution(N)
        next_solution_value = estimate_solution(next_solution, distance_matrix)
        if next_solution_value < solution_value:
            solution = next_solution
            solution_value = next_solution_value
            print(f"Current solution: {solution} - {solution_value}")
    return solution


def main():
    best_solution = search(10000)
    print(f"Best solution: {best_solution} - {estimate_solution(best_solution, distance_matrix)}")


if __name__ == '__main__':
    main()
