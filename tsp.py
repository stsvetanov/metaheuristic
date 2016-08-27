'''
Solves TSP problem
'''

from tsp_abc import tsp_abc
from tsp_local_search import tsp_local_search
from tsp_ga import tsp_ga

NUMBER_OF_ITERATIONS = 250
NUMBER_OF_CITIES = 25
POPULATION_SIZE = 150


def main():

    user_input = input("Type: \n 1 for TSP-ABC \n 2 for TSP-Local \n")
    print('Solving TSP with {} cities'.format(NUMBER_OF_CITIES))
    if user_input == '1':
        tsp_abc(NUMBER_OF_CITIES, NUMBER_OF_ITERATIONS)
    elif user_input == '2':
        tsp_local_search(NUMBER_OF_CITIES, NUMBER_OF_ITERATIONS)
    elif user_input == '3':
        tsp_ga(NUMBER_OF_CITIES, NUMBER_OF_ITERATIONS, POPULATION_SIZE)


if __name__ == '__main__':
    main()
