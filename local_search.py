from utils import generate_solution, estimate_solution, mutate_solution


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
    # print("Best Solution:", s, " Value:", e)
    return s