from utils_tsp import create_tsp_map, generate_population_tsp, estimate_population_tsp, select_population, estimate_solution_tsp
from utils_tsp import generate_subglobal_solution_tsp
from tsp_local_search import tsp_local_search


def tsp_abc(number_of_cities=20, number_of_iterations=50):
    scouts = 15
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
