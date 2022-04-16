import random
import string
import time


def generate_solution(solution_size):
    return "".join((random.choice(string.ascii_letters + " " + string.digits) for _ in range(solution_size)))


def generate_population(target, population_size):
    solution_size = len(target)
    return [generate_solution(solution_size) for _ in range(population_size)]


def estimate_solution(solution: str, target: str) -> int: # In the context of Genetic Algorithms, this function is called "fitness"
    value = 0
    for index, ch in enumerate(solution):
        value += abs(ord(ch) - ord(target[index]))
    return value

    # return sum(abs(ord(ch_solution) - ord(ch_target)) for ch_solution, ch_target in zip(solution, target))
    # m = map(lambda x: abs(ord(x[0]) - ord(x[1])), zip(solution, target))
    # return reduce(lambda x, y: x + y, m)


def estimate_population(population: list, target: str) -> dict:
    return {solution: estimate_solution(solution, target) for solution in population}


def mutate_population(elite_solutions):
    return [mutate_solution(elite_solution) for elite_solution in elite_solutions]


def mutate_solution(solution):
    solution_len = len(solution)
    index_to_replace = random.randint(0, solution_len - 1)
    element_to_replace = random.choice(string.ascii_letters + " " + string.digits)
    return solution[:index_to_replace] + element_to_replace + solution[index_to_replace + 1:]


def select_population(estimated_population: dict):
    return sorted(estimated_population, key=lambda x: estimated_population[x])


def local_search(target, number_of_moves=50, solution=None):
    if solution is None:
        solution_size = len(target)
        s = generate_solution(solution_size)
    else:
        s = solution
    e = estimate_solution(s, target)
    # print("Initial Solution {} Value  {}".format(s, e))
    for x in range(number_of_moves):
        ss = mutate_solution(s)
        ee = estimate_solution(ss, target)
        # print("Neighbor Solution ", ss, "Value ", ee)
        if ee < e:  # If neighbor solution is better that current, accept it as current.
            e = ee
            s = ss
            # print("New best {} -> {}".format(s, e))
    print("Best Solution in local search:", s, " Value:", e)
    return s


def random_search(target, number_of_moves=50):
    solution_size = len(target)
    s = generate_solution(solution_size)
    e = estimate_solution(s, target)
    print("Initial Solution {} Value  {}".format(s, e))
    for x in range(number_of_moves):
        ss = generate_solution(solution_size)
        ee = estimate_solution(ss, target)
        print("Neighbor Solution ", ss, "Value ", ee)
        if ee < e:  # If neighbor solution is better that current, accept it as current.
            e = ee
            s = ss
    print("Best Solution:", s, " Value:", e)


def abc_search(target, number_of_iterations=50, population_size=100):
    start_time = time.time()
    scouts = int(population_size/10)
    workers = population_size - scouts
    best_solution = None
    global_solutions = generate_population(target, scouts)

    for iterations_counter in range(number_of_iterations):
        estimated_global_solutions = estimate_population(global_solutions[:scouts], target)
        selected_global_solutions = select_population(estimated_global_solutions)
        local_solutions = workers_activity(target, workers, selected_global_solutions[:15])
        estimated_local_solutions = estimate_population(local_solutions, target)
        selected_local_solutions = select_population(estimated_local_solutions)
        elite_solutions = selected_local_solutions[:10]
        best_solution_in_generation = selected_local_solutions[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, target)

        print("Best solution in iter {} is {} -> {}".format(iterations_counter, best_solution_in_generation, best_solution_in_generation_score))

        if best_solution is None:
            best_solution = best_solution_in_generation

        if estimate_solution(best_solution_in_generation, target) < estimate_solution(best_solution, target):
            best_solution = best_solution_in_generation

        if estimate_solution(best_solution, target) == 0:
            break

        global_solutions = elite_solutions

    print("Best solution: {} -> {}".format(best_solution, estimate_solution(best_solution, target)))
    print("--- %s seconds ---" % (time.time() - start_time))


def workers_activity(target, workers, selected_global_solutions):
    solutions = []
    counter = len(selected_global_solutions)
    for s in selected_global_solutions:
        for _ in range(workers):
            solutions.append(local_search(target, counter, s))
        counter = int(counter/3)
        if counter < 2:
            break
    return solutions


def ga_search(target, number_of_iterations=50, population_size=100):
    best_solution = None
    initial_population = generate_population(target, population_size)

    for iterations_counter in range(number_of_iterations):
        estimated_population = estimate_population(initial_population, target)
        selection = select_population(estimated_population)
        elite_solutions = selection[:50]
        offsprings = crossover(elite_solutions)
        estimated_offsprings = estimate_population(offsprings, target)
        selected_offsprings = select_population(estimated_offsprings)
        best_solution_in_generation = selected_offsprings[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, target)

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
    print("Best solution: {} -> {}".format(best_solution, best_solution_score))


def crossover(selection):
    parent1 = selection[0]
    parent2 = selection[1]
    cross_point = int(len(parent1)/2)
    offspring1 = parent1[:cross_point] + parent2[cross_point:]
    offspring2 = parent2[:cross_point] + parent1[cross_point:]
    return offspring1, offspring2
