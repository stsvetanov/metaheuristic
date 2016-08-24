from utils import generate_population, estimate_solution


def ga_search(target, number_of_iterations=50, population_size=100):
    best_solution = None
    elite_solutions = None
    for iterations_counter in range(number_of_iterations):
        population = generate_population(target, population_size)
        if elite_solutions is not None:
            for elites in elite_solutions:
                population.append(elites)
        estimated_population = estimate_population(population, target)
        # selection = sorted(estimated_population.items(), key=lambda x: x[1])
        # selection = [key for key, value in estimated_population.items()]
        selection = select_population(estimated_population)
        elite_solutions = selection[:10]
        offsprings = crossover(selection)
        estimated_offsprings = estimate_population(offsprings, target)
        selected_offsprings = select_population(estimated_offsprings)
        best_solution_in_generation = selected_offsprings[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, target)
        # counter1 += int(best_solution_in_generation[1])

        print("Best solution in iteration {} is {} -> {}".format(iterations_counter, best_solution_in_generation, best_solution_in_generation_score))
        iterations_counter += 1

        if best_solution is None:
            best_solution = best_solution_in_generation
            # print(best_solution)

        # ace = best_solution, best_solution_in_generation
        # offsprings = crossover(ace)
        # best_solutions_in_generation = estimate_population(offsprings, target)
        # best_solution_in_generation = best_solutions_in_generation[0]
        # counter2 += best_solution_in_generation[1]

        if estimate_solution(best_solution_in_generation, target) < estimate_solution(best_solution, target):
            best_solution = best_solution_in_generation
            best_solution_score = estimate_solution(best_solution, target)
    print("Best solution {} -> {}".format(best_solution, best_solution_score))
    # print("Accuracy 1 {}, Accuracy 2 {}".format(counter1/number_of_iterations, counter2/number_of_iterations))


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


def select_population(estimated_population: dict):
    selection = sorted(estimated_population, key=lambda x: estimated_population[x])
    return selection


def crossover(selection):
    parent1 = selection[0]
    parent2 = selection[1]
    cross_point = int(len(parent1)/2)
    offspring1 = parent1[:cross_point] + parent2[cross_point:]
    offspring2 = parent2[:cross_point] + parent1[cross_point:]
    return offspring1, offspring2
