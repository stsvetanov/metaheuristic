d_min = 38
d_max = 1962
p_min = 4680
p_max = 65528
s_min = 0
s_max = 420


def estimate_solution(solution: list, target: int) -> int:
    d = solution[0]
    p = solution[1]
    s = solution[2]
    score = d/((s+1)*p)
    diff = abs(target - score)
    return diff


def search(target):
    solution = (d_min, s_max, p_max)
    solution_value = estimate_solution(solution, target)

    for d in range(d_min, d_max):
        print(d)
        for p in range(p_min, p_max):
            for s in range(s_min, s_max):
                next_solution = (d, p, s)
                if estimate_solution(next_solution, target) < solution_value:
                    solution = next_solution
    return solution


def main():
    k = 400
    exp = 2.25

    d = []
    p = []
    s = []

    target = k**exp

    print("Target {}".format(target))

    best_d, best_p, best_s = search(target)

    d.append(best_d)
    p.append(best_p)
    s.append(best_s)

    print(d)
    print(p)
    print(s)

    with open('output.txt', 'a') as f:
        f.write(str(d))
        f.write("\n")
        f.write(str(p))
        f.write("\n")
        f.write(str(s))


if __name__ == '__main__':
    main()
