'''
Generate string that is closer to the target.
To calculate the distance between strings, compare each digits.
Example:
    1234 and 2235 -> 1 + 0 + 0 + 2 = 5

    Implemented methods:
        random_search
        ga_search
'''

from random_search import random_search
from ga_search import ga_search
from abc_search import abc_search
from local_search import local_search

TARGET = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

print(len(TARGET))

NUMBER_OF_ITERATIONS = 150

POPULATION_SIZE = 1024 # Needed for ga_search only
1


def main():
    # choices = {'a': 1, 'b': 2}
    # result = choices.get(key, 'default')

    user_input = input("Type: \n 1 for Random Search \n 2 for GA \n 3 for ABC \n 4 for Local Search \n")
    print('Target solution: {}'.format(TARGET))
    if user_input == '1':
        random_search(TARGET, NUMBER_OF_ITERATIONS)
    elif user_input == '2':
        ga_search(TARGET, NUMBER_OF_ITERATIONS, POPULATION_SIZE)
    elif user_input == '3':
        abc_search(TARGET, NUMBER_OF_ITERATIONS)
    elif user_input == '4':
        local_search(TARGET, NUMBER_OF_ITERATIONS)


if __name__ == '__main__':
    main()
