from utils import generate_population, estimate_population, estimate_solution, workers_activity, load_coordinates, plotTSP
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random


def search(number_of_cities, number_of_iterations, population_size):
    np.random.seed(1)
    city_coordinates = np.random.rand(number_of_cities, 2)

    # city_coordinates = load_coordinates("att48_xy.txt")
    print(city_coordinates)

    distance_matrix = squareform(pdist(city_coordinates, 'euclidean'))

    scouts = int(population_size/10)
    workers = population_size - scouts
    best_solution = None
    # global_solutions = generate_population(number_of_cities, scouts)
    global_solutions = generate_population(len(city_coordinates), scouts)

    for iterations_counter in range(number_of_iterations):
        estimated_global_solutions = estimate_population(global_solutions, distance_matrix)
        local_solutions = workers_activity(workers, estimated_global_solutions[:15], distance_matrix)
        estimated_local_solutions = estimate_population(local_solutions, distance_matrix)

        new_population_size = len(local_solutions) - len(estimated_local_solutions)
        new_population = generate_population(len(city_coordinates), new_population_size * 10)
        estimated_new_population = estimate_population(new_population, distance_matrix)
        for solution in estimated_new_population[:int(new_population_size/10)]:
            estimated_local_solutions.append(solution)

        elite_solutions = estimated_local_solutions[:15]
        best_solution_in_generation = estimated_local_solutions[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, distance_matrix)

        # print(f"Best solution in iter {iterations_counter} is {best_solution_in_generation} -> {best_solution_in_generation_score}")
        print(f"Best solution score in iter {iterations_counter} is {best_solution_in_generation_score}")
        print(f"Number of local solutions: {len(local_solutions)}")
        print(f"Number of local estimated_local_solutions: {len(estimated_local_solutions)}")
        print(f"Number of elites: {len(elite_solutions)}")

        if best_solution is None:
            best_solution = best_solution_in_generation
            best_solution_score = best_solution_in_generation_score

        if best_solution_in_generation_score < best_solution_score:
            best_solution = best_solution_in_generation
            best_solution_score = best_solution_in_generation_score
        # elif random.randint(1, number_of_iterations) < iterations_counter:
        #     elite_solutions.append(best_solution_in_generation)

        if estimate_solution(best_solution, distance_matrix) == 0:
            break

        global_solutions = elite_solutions
        plotTSP(best_solution, city_coordinates)

    return best_solution, best_solution_score


def main():
    number_of_iterations = 50
    population_size = 500
    number_of_cities = 35

    best_solution, best_solution_score = search(number_of_cities, number_of_iterations, population_size)

    # print(f"Best solution: {best_solution} -> {best_solution_score}")
    print(f"Best solution score: {best_solution_score}")


if __name__ == '__main__':
    main()
