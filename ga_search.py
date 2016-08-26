from utils import generate_population, estimate_solution, estimate_population, mutate_population, select_population
import random


def ga_search(target, number_of_iterations=50, population_size=100):
    best_solution = None
    initial_population = generate_population(target, population_size)

    for iterations_counter in range(number_of_iterations):
        estimated_population = estimate_population(initial_population, target)
        # selection = sorted(estimated_population.items(), key=lambda x: x[1])
        # selection = [key for key, value in estimated_population.items()]
        selection = select_population(estimated_population)
        elite_solutions = selection[:50]
        offsprings = crossover(elite_solutions)
        estimated_offsprings = estimate_population(offsprings, target)
        selected_offsprings = select_population(estimated_offsprings)
        best_solution_in_generation = selected_offsprings[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, target)
        # counter1 += int(best_solution_in_generation[1])

        print("Best solution in iteration {} is {} -> {}".format(iterations_counter, best_solution_in_generation, best_solution_in_generation_score))

        if best_solution is None:
            best_solution = best_solution_in_generation

        if estimate_solution(best_solution_in_generation, target) < estimate_solution(best_solution, target):
            best_solution = best_solution_in_generation
            best_solution_score = estimate_solution(best_solution, target)
            elite_solutions.append(best_solution)

        initial_population = mutate_population(selection)
        for elites in elite_solutions:
            initial_population.append(elites)
    print("Best solution {} -> {}".format(best_solution, best_solution_score))


def crossover(selection):
    parent1 = selection[0]
    parent2 = selection[1]
    cross_point = int(len(parent1)/2)
    offspring1 = parent1[:cross_point] + parent2[cross_point:]
    offspring2 = parent2[:cross_point] + parent1[cross_point:]
    return offspring1, offspring2
