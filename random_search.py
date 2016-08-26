from utils import generate_solution, estimate_solution


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