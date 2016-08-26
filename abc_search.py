from utils import generate_population, estimate_population, select_population, mutate_solution, estimate_solution
from local_search import local_search


def abc_search(target, number_of_iterations=50):
    scouts = 10
    workers = 50
    best_solution = None
    global_solutions = generate_population(target, scouts)

    for iterations_counter in range(number_of_iterations):
        estimated_global_solutions = estimate_population(global_solutions[:scouts], target)
        selected_global_solutions = select_population(estimated_global_solutions)
        local_solutions = workers_activities(target, workers, selected_global_solutions)
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

        global_solutions = elite_solutions

        # for elites in elite_solutions:
        #     global_solutions.append(elites)

    print("Best solution {} -> {}".format(best_solution, estimate_solution(best_solution, target)))


def workers_activities(target, workers, selected_global_solutions):
    solutions = []
    counter = 0
    dev = 2
    for s in selected_global_solutions:
        for _ in range(int(workers / dev)):
            solutions.append(local_search(target, 50, s))
        dev *= 2
        if counter > 3:
            break
    return solutions


'''
1 - 50
2 - 20
3 - 15
4 - 10
5 - 5
'''
