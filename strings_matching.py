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

TARGET = '00000000'
NUMBER_OF_ITERATIONS = 40

POPULATION_SIZE = 1000


def main():
    print('Target solution: {}'.format(TARGET))
    #random_search(TARGET, NUMBER_OF_ITERATIONS)
    ga_search(TARGET, NUMBER_OF_ITERATIONS, POPULATION_SIZE)


if __name__ == '__main__':
    main()



