from Lecture_67_Meta.PWM.utils import generate_population, estimate_population, estimate_solution, sort_population, mutate_population


def search(target, number_of_iterations, population_size):
    scouts = int(population_size/10)
    workers = population_size - scouts
    best_solution = None
    global_solutions = generate_population(target, scouts)

    for iterations_counter in range(number_of_iterations):
        estimated_global_solutions = estimate_population(global_solutions[:scouts], target)
        selected_global_solutions = sort_population(estimated_global_solutions)
        local_solutions = mutate_population(selected_global_solutions[:15])
        estimated_local_solutions = estimate_population(local_solutions, target)
        selected_local_solutions = sort_population(estimated_local_solutions)
        elite_solutions = selected_local_solutions[:10]
        best_solution_in_generation = selected_local_solutions[0]
        best_solution_in_generation_score = estimate_solution(best_solution_in_generation, target)

        print("Best solution in iter {} is {} -> {}".format(iterations_counter, best_solution_in_generation,
                                                            best_solution_in_generation_score))

        if best_solution is None:
            best_solution = best_solution_in_generation

        if estimate_solution(best_solution_in_generation, target) < estimate_solution(best_solution, target):
            best_solution = best_solution_in_generation

        if estimate_solution(best_solution, target) == 0:
            break

        global_solutions = elite_solutions

    return best_solution


def main():
    number_of_iterations = 10
    population_size = 50

    k = 400
    exp = 2.25

    target = k**exp

    print("Target {}".format(target))

    best_d, best_p, best_s = search(target, number_of_iterations, population_size)

    print(best_d)
    print(best_p)
    print(best_s)

    with open('output.txt', 'a') as f:
        f.write(str(best_d))
        f.write("\n")
        f.write(str(best_p))
        f.write("\n")
        f.write(str(best_s))


if __name__ == '__main__':
    main()
