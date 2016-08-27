from utils_tsp import generate_solution_tsp, estimate_solution_tsp, generate_neighbor_solution_tsp, create_tsp_map


def tsp_local_search(number_of_cities=20, number_of_moves=50, solution=None, tsp_map=None):
    # best_solution = None

    if tsp_map is None:
        tsp_map = create_tsp_map(number_of_cities)
    # else:
    #     tsp_map = tsp_map

    if solution is None:
        s = generate_solution_tsp(number_of_cities)
    else:
        s = list(solution)

    e = estimate_solution_tsp(s, tsp_map)

    # print("Initial Solution {} Value  {}".format(s, e))
    for x in range(number_of_moves):
        ss = generate_neighbor_solution_tsp(s)
        ee = estimate_solution_tsp(ss, tsp_map)
        # print("Neighbor Solution ", ss, "Value ", ee)
        # if best_solution is None:
        #     best_solution = s

        if ee < e:  # If neighbor solution is better that current, accept it as current.
            e = ee
            s = ss
    # print("Best Solution:", s, " Value:", e)
    return s
