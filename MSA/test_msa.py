from abc_solver import ABCSolver

if __name__ == '__main__':
    ABCSolver(file_name="dataset/BB11001.fa", number_of_iterations=10, population_size=700).run()
    # ABCSolver(file_name="dataset/H1N1_Protein_NS2_149.fa", number_of_iterations=10, population_size=70).run()
