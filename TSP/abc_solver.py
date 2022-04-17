import random

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import squareform, pdist


class ABCSolver:
    def __init__(self, file_name, number_of_iterations, population_size):
        self.file_name = file_name
        self.number_of_iterations = number_of_iterations
        self.population_size = population_size
        self.scouts = int(self.population_size / 3)
        self.workers = self.population_size - self.scouts
        self.best_solution = None
        self.number_of_elites = int(self.population_size / 10)

    def load_coordinates(self, filename: str) -> list:
        with open(filename, 'r', encoding='utf-8') as f:
            data = [[int(coordinates) for coordinates in line.split()] for line in f]
        return squareform(pdist(np.array(data), 'euclidean'))

    def generate_random_solution(self, number_of_cities):
        return random.sample(range(0, number_of_cities), number_of_cities)

    def generate_population(self, number_of_cities, population_size):
        return [self.generate_random_solution(number_of_cities) for _ in range(population_size)]

    def estimate_population(self, population: list, distance_matrix: list) -> dict:
        estimated_population = {tuple(solution): self.estimate_solution(solution, distance_matrix) for solution in
                                population}
        sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
        return sorted_population

    def workers_activity(self, workers, selected_global_solutions, distance_matrix):
        solutions = []
        counter = len(selected_global_solutions)
        for solution in selected_global_solutions:
            for _ in range(workers):
                solutions.append(self.local_search(counter, solution, distance_matrix))
            counter = int(counter / 5)
            if counter < 2:
                break
        return solutions

    def create_local_solution(self, solution):
        mutationRate = 0.03
        solution = list(solution)
        for swapped in range(len(solution)):
            if random.random() < mutationRate:
                swapWith = int(random.random() * len(solution))
                solution[swapWith], solution[swapped] = solution[swapped], solution[swapWith]
        return solution

    def local_search(self, number_of_iter, solution, distance_matrix):
        solution_value = self.estimate_solution(solution, distance_matrix)
        # print(f"Initial solution: {solution} - {solution_value}")
        for i in range(number_of_iter):
            next_solution = self.create_local_solution(solution)
            next_solution_value = self.estimate_solution(next_solution, distance_matrix)
            if next_solution_value < solution_value:
                solution = next_solution
                solution_value = next_solution_value
            # elif random.randint(1, number_of_iter) < i/10:
            #     solution = next_solution
            #     solution_value = next_solution_value
        return solution

    def estimate_solution(self, solution: list, distance_matrix: list) -> int:
        distance = 0
        for i in range(len(solution)):
            distance += distance_matrix[solution[i - 1]][solution[i]]
        return distance

    def plotTSP(self, path, points, num_iters=1):
        x = [];
        y = []
        for i in path:
            x.append(float(points[i][0]))
            y.append(float(points[i][1]))

        plt.plot(x, y, 'co')

        a_scale = float(max(x)) / float(100)

        plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
                  color='g', length_includes_head=True)
        for i in range(0, len(x) - 1):
            plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                      color='g', length_includes_head=True)

        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)
        plt.show()

    def run(self):
        distance_matrix = self.load_coordinates(self.file_name)
        # global_solutions = generate_population(number_of_cities, scouts)
        global_solutions = self.generate_population(len(distance_matrix), self.scouts)

        for iterations_counter in range(self.number_of_iterations):
            estimated_global_solutions = self.estimate_population(global_solutions, distance_matrix)
            local_solutions = self.workers_activity(self.workers, estimated_global_solutions[:self.number_of_elites], distance_matrix)
            estimated_local_solutions = self.estimate_population(local_solutions, distance_matrix)

            new_population_size = len(local_solutions) - len(estimated_local_solutions)
            new_population = self.generate_population(len(distance_matrix), new_population_size * 10)
            estimated_new_population = self.estimate_population(new_population, distance_matrix)
            for solution in estimated_new_population[:int(new_population_size / 10)]:
                estimated_local_solutions.append(solution)

            elite_solutions = estimated_local_solutions[:self.number_of_elites]
            best_solution_in_generation = estimated_local_solutions[0]
            best_solution_in_generation_score = self.estimate_solution(best_solution_in_generation, distance_matrix)

            # print(f"Best solution in iter {iterations_counter} is {best_solution_in_generation} -> {best_solution_in_generation_score}")
            print(f"Best solution score in iter {iterations_counter} is {best_solution_in_generation_score}")
            print(f"Number of local solutions: {len(local_solutions)}")
            print(f"Number of local estimated_local_solutions: {len(estimated_local_solutions)}")
            print(f"Number of elites: {len(elite_solutions)}")

            if self.best_solution is None:
                self.best_solution = best_solution_in_generation
                best_solution_score = best_solution_in_generation_score

            if best_solution_in_generation_score < best_solution_score:
                self.best_solution = best_solution_in_generation
                best_solution_score = best_solution_in_generation_score
            # elif random.randint(1, number_of_iterations) < iterations_counter:
            #     elite_solutions.append(best_solution_in_generation)

            if self.estimate_solution(self.best_solution, distance_matrix) == 0:
                break

            global_solutions = elite_solutions
            self.plotTSP(self.best_solution, distance_matrix)

        return self.best_solution, best_solution_score