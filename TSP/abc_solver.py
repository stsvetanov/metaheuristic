import random

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import squareform, pdist


class ABCSolver:
    def __init__(self, file_name, number_of_iterations, population_size):
        self.file_name = file_name
        self.number_of_iterations = number_of_iterations
        self.population_size = population_size
        self.number_of_scouts = int(self.population_size / 5)
        self.number_of_workers = self.population_size - self.number_of_scouts
        self.best_solution = None
        self.number_of_elite_solutions = int(self.population_size / 20)
        self.distance_matrix = None
        self.number_of_cities = None

    def load_coordinates(self) -> list:
        data = np.loadtxt(self.file_name)
        # with open(self.file_name) as file_handler:
        #     data = [[int(digit) for digit in line.split()] for line in file_handler]
        return squareform(pdist(data, 'euclidean'))

    def generate_random_solution(self):
        return random.sample(range(0, self.number_of_cities), self.number_of_cities)

    def generate_population(self, population_size):
        return [self.generate_random_solution() for _ in range(population_size)]

    def estimate_population(self, population: list) -> dict:
        estimated_population = {tuple(solution): self.estimate_solution(solution) for solution in
                                population}
        sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
        return sorted_population

    def workers_activity(self, elite_solutions):
        solutions = []
        counter = self.number_of_workers
        for solution in elite_solutions:
            solutions.append(self.local_search(counter, solution))
            counter = int(counter / 1.5)
            if counter < 2:
                break
        return solutions

    def local_search(self, counter, solution):
        solution_value = self.estimate_solution(solution)
        for i in range(counter):
            next_solution = self.create_local_solution(solution)
            next_solution_value = self.estimate_solution(next_solution)
            if next_solution_value < solution_value:
                solution = next_solution
                solution_value = next_solution_value
        return solution

    def create_local_solution(self, solution):
        solution = list(solution)
        for swapped in range(len(solution)):
            swapWith = int(random.random() * len(solution))
            solution[swapWith], solution[swapped] = solution[swapped], solution[swapWith]
        return solution


    def estimate_solution(self, solution: list) -> int:
        distance = 0
        for i in range(len(solution)):
            distance += self.distance_matrix[solution[i - 1]][solution[i]]
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
        self.distance_matrix = self.load_coordinates()
        self.number_of_cities = len(self.distance_matrix)
        initial_population = self.generate_population(self.number_of_scouts)

        for iterations_counter in range(self.number_of_iterations):
            estimated_population = self.estimate_population(initial_population)
            elite_solutions = estimated_population[:self.number_of_elite_solutions]
            local_solutions = self.workers_activity(elite_solutions)
            estimated_local_solutions = self.estimate_population(local_solutions)

            new_population = self.generate_population(self.number_of_scouts)
            estimated_new_population = self.estimate_population(new_population)
            for solution in estimated_new_population[:self.number_of_elite_solutions]:
                estimated_local_solutions.append(solution)

            elite_solutions = estimated_local_solutions[:self.number_of_elite_solutions]
            best_solution_in_generation = estimated_local_solutions[0]
            best_solution_in_generation_score = self.estimate_solution(best_solution_in_generation)

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

            initial_population = elite_solutions
            self.plotTSP(self.best_solution, self.distance_matrix)

        return self.best_solution, best_solution_score
