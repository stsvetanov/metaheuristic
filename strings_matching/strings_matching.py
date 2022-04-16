'''
Generate string that is closer to the target.
To calculate the distance between strings, compare each digits.
Example:
    Target = 1234
    Test = 2235
    Estimation: 1 + 0 + 0 + 1 = 2

    Implemented methods:
        random_search        combinations
        ga_search
'''

from utils import random_search, ga_search, abc_search, local_search

TARGET = "Lorem Ipsum is simply dummy text of the printing and typesetting industry"
NUMBER_OF_ITERATIONS = 150
POPULATION_SIZE = 300  # Required for ga_search only


def main():
    user_input = input("Type: \n 1 for Random Search \n 2 for GA \n 3 for ABC \n 4 for Local Search \n")
    print('Target solution: {}'.format(TARGET))
    if user_input == '1':
        random_search(TARGET, NUMBER_OF_ITERATIONS)
    elif user_input == '2':
        ga_search(TARGET, NUMBER_OF_ITERATIONS, POPULATION_SIZE)
    elif user_input == '3':
        abc_search(TARGET, NUMBER_OF_ITERATIONS, POPULATION_SIZE)
    elif user_input == '4':
        local_search(TARGET, NUMBER_OF_ITERATIONS)


if __name__ == '__main__':
    main()
