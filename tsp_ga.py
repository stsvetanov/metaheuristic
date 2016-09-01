from utils_tsp import create_tsp_map, generate_population_tsp, estimate_population_tsp, select_population, estimate_solution_tsp
from utils_tsp import generate_subglobal_solution_tsp
from tsp_local_search import tsp_local_search
import random


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
