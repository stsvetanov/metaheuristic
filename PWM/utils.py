import random

d_min = 38
d_max = 1962
p_min = 4680
p_max = 65528655286552865528
s_min = 0
s_max = 420420420


def generate_solution():
    solution = []
    solution.append(random.randint(d_min, d_max))
    solution.append(random.randint(p_min, p_max))
    solution.append(random.randint(s_min, s_max))
    return solution


def generate_population(target, population_size):
    population = []
    for y in range(population_size):
        population.append(generate_solution())
    return population


def estimate_solution(solution: list, target: int) -> int: # In the context of Genetic Algorithms, this function is called "fitness"
    d = solution[0]
    p = solution[1]
    s = solution[2]
    score = d/((s+1)*p)
    diff = abs(target - score)
    #print("Solution {} - Score {} - diff {}".format(solution, score, diff))
    return diff


def estimate_population(population: list, target: int) -> dict:
    estimated_population = {}
    for solution in population:
        solution = tuple(solution)
        estimated_population[solution] = estimate_solution(solution, target)
    return estimated_population


def sort_population(estimated_population: dict):
    sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
    return sorted_population


def mutate_population(elite_solutions):
    for index, mutated_solution in enumerate(elite_solutions):
        elite_solutions[index] = mutate_solution(mutated_solution)
    return elite_solutions


def mutate_solution(solution):
    solution = list(solution)
    num_low = 0
    num_len = len(solution)
    index = random.randint(num_low, num_len-1)
    k = random.randint(0, 5)

    if k < 3:
        if index < 1 and (d_min < solution[index] < d_max):
            solution[index] = solution[index] + random.randint(-1, 1)
        elif index < 2 and (p_min < solution[index] < p_max):
            solution[index] = solution[index] + random.randint(-1, 1)
        elif index < 3 and (s_min < solution[index] < s_max):
            solution[index] = solution[index] + random.randint(-1, 1)

    else:
        if index < 1:
            solution[index] = random.randint(d_min, d_max)
        elif index < 2:
            solution[index] = random.randint(p_min, p_max)
        else:
            solution[index] = random.randint(s_min, s_max)

    mutated_solution = solution
    return mutated_solution