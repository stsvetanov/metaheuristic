import random

from utils import read_fasta, estimate_solution


class ABCSolver:
    def __init__(self, file_name, number_of_iterations, population_size):
        self.population_to_elites_ration = 20
        self.workers_to_scouts_ratio = 5
        self.file_name = file_name
        self.number_of_iterations = number_of_iterations
        self.population_size = population_size
        self.number_of_scouts = int(self.population_size / self.workers_to_scouts_ratio)
        self.number_of_workers = self.population_size - self.number_of_scouts
        self.best_solution = None
        self.best_solution_value = 0
        self.number_of_elite_solutions = int(self.population_size / self.population_to_elites_ration)
        self.initial_solution = self.load_sequences()
        self.population = None
        self.number_of_seq_in_alignment = len(self.initial_solution)

    def load_sequences(self) -> list:
        initial_alignment_df = read_fasta(self.file_name)
        return [sequence for sequence in initial_alignment_df.get("sequence")]

    def create_solution(self, solution=None):
        alignment_len = 0
        if not solution:
            solution = []
            for sequence in self.initial_solution:
                seq_len = len(sequence)
                number_of_gaps = random.randint(0, int(seq_len / 3))

                for _ in range(number_of_gaps):
                    index = random.randint(0, seq_len - 1)
                    sequence = sequence[:index] + '-' + sequence[index:]

                solution.append(sequence)
                sequence_len = len(sequence)
                if sequence_len > alignment_len:
                    alignment_len = sequence_len
        else:
            sequence_number = random.randint(0, self.number_of_seq_in_alignment - 1)
            solution = list(solution)
            sequence = solution[sequence_number]
            position = random.randint(0, len(sequence) - 1)

            if sequence[position] == '-':
                solution[sequence_number] = sequence[:position] + sequence[position + 1:] + '-'
            else:
                solution[sequence_number] = sequence[:position] + '-' + sequence[position:]
            sequence_len = len(sequence)
            if sequence_len > alignment_len:
                alignment_len = sequence_len

        for index, sequence in enumerate(solution):
            if len(sequence) < alignment_len:
                solution[index] += '-' * (alignment_len - len(sequence))
        return solution

    def generate_population(self):
        return [self.create_solution() for _ in range(self.number_of_scouts)]

    def estimate_population(self):
        estimated_population = {tuple(solution): estimate_solution(solution) for solution in self.population}
        sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x], reverse=True)
        return sorted_population

    def workers_activity(self, elite_solutions):
        solutions = []
        counter = self.number_of_workers
        for solution in elite_solutions:
            solutions.append(self.local_search(counter, solution))
            counter = int(counter / 2)
            if counter < 2:
                break
        return solutions

    def local_search(self, counter, solution):
        for i in range(counter):
            solution_value = estimate_solution(solution)
            next_solution = self.create_solution(solution)
            next_solution_value = estimate_solution(next_solution)
            if next_solution_value > solution_value:
                print(solution_value, next_solution_value)
                solution = next_solution
        return solution

    def print_solution(self, solution):
        for index, sequence in enumerate(self.best_solution):
            print(f'{index}: {sequence}')

    def run(self):
        for iterations_counter in range(self.number_of_iterations):
            self.population = self.generate_population()
            estimated_solutions = self.estimate_population()
            self.population = self.workers_activity(estimated_solutions)
            estimated_local_solutions = self.estimate_population()
            print(estimated_local_solutions)

            best_solution_in_generation = estimated_local_solutions[0]
            best_solution_in_generation_score = estimate_solution(best_solution_in_generation)

            print(f"Best solution in iter {iterations_counter} is {best_solution_in_generation}: {best_solution_in_generation_score}")
            print(f"Number of local solutions: {len(estimated_local_solutions)}")
            print(f"Number of local estimated_local_solutions: {len(estimated_local_solutions)}")

            if self.best_solution is None or best_solution_in_generation_score > self.best_solution_value:
                self.best_solution = best_solution_in_generation
                self.best_solution_value = best_solution_in_generation_score

            self.population += self.generate_population()
            estimated_new_population = self.estimate_population()

            self.population = estimated_local_solutions[:self.number_of_elite_solutions] + estimated_new_population

        self.print_solution(self.best_solution)
        print(self.best_solution_value)
