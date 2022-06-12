import string
from random import random
from Bio import SeqIO
import random

import numpy as np
import pandas as pd


def generate_solution(alignment):
    new_alignment = []
    max_seq_len = 0
    for sequence in alignment:
        seq_len = len(sequence)
        number_of_gaps = np.random.randint(0, seq_len / 3)
        for _ in range(number_of_gaps):
            index = random.randint(0, seq_len - 1)
            sequence = sequence[:index] + '-' + sequence[index:]
        new_alignment.append(sequence)
        sequence_len = len(sequence)
        if sequence_len > max_seq_len:
            max_seq_len = sequence_len

    for index, sequence in enumerate(new_alignment):
        if len(sequence) < max_seq_len:
            new_alignment[index] += '-' * (max_seq_len - len(sequence))
            # for i in range(max_seq_len - len(sequence)):
            #     if random.random() < 0.5:
            #         new_alignment[index] += '-'
            #     else:
            #         new_alignment[index] = '-' + new_alignment[index]
    return new_alignment


def generate_population(size, alignment):
    return [generate_solution(alignment) for _ in range(size)]


def read_fasta(
    filename,
    schema='fasta',
    seq_label='sequence',
    use_uids=False,
    **kwargs):
    """Use BioPython's sequence parsing module to convert any file format to
    a Pandas DataFrame.

    The resulting DataFrame has the following columns:
        - name
        - id
        - description
        - sequence
    """

    # Prepare DataFrame fields.
    data = {
        'id': [],
        seq_label: [],
        'description': [],
        'label': []
    }
    if use_uids:
        data['uid'] = []

    # Parse Fasta file.
    for i, s in enumerate(SeqIO.parse(filename, format=schema, **kwargs)):
        data['id'].append(s.id)
        data[seq_label].append(str(s.seq))
        data['description'].append(s.description)
        data['label'].append(s.name)

        if use_uids:
            data['uid'].append(get_random_id(10))

    # Port to DataFrame.
    return pd.DataFrame(data)

def get_random_id(length):
    """Generate a random, alpha-numerical id."""
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


def estimate_solution(alignment):
    sum_total = 0
    for index_sequence in range(len(alignment) - 1):
        sequence_len = len(alignment[index_sequence])
        sum_column = 0
        for column in range(sequence_len - 1):
            if alignment[index_sequence][column] == '-' or alignment[index_sequence + 1][column] == '-':
                continue
            position_first = amino_acid_to_position.get(ord(alignment[index_sequence][column]))
            position_second = amino_acid_to_position.get(ord(alignment[index_sequence + 1][column]))
            sum_column += blosum62mt2[position_first][position_second]
        sum_total += sum_column
    return sum_total


def estimate_population(population):
    estimated_population = {tuple(solution): estimate_solution(solution) for solution in population}
    print(estimated_population)
    sorted_population = sorted(estimated_population, key=lambda x: estimated_population[x])
    return sorted_population


def estimate_solution_np(solution):
    sum_total = 0
    for column in solution.T[:5]:
        column_len = len(column)
        sum_column = 0
        for i in range(column_len - 1):
            position_first = amino_acid_to_position.get(column[i])
            position_second = amino_acid_to_position.get(column[i + 1])
            sum_column += blosum62mt2[position_first][position_second]
        sum_total += sum_column
    return sum_total


amino_acid_order = "ABCDEFGHIKLMNPQRSTVWXYZ"
amino_acid_to_position = {np.uint8(ord(amino_acid)): position for position, amino_acid in enumerate(amino_acid_order)}

blosum62mt2 = np.array(
[
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -6, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-4,  8, -6, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2,  2, -8,  4, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-4, -6, -4, -6, -6, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, -2, -6, -2, -4, -6, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-4,  0, -6, -2,  0, -2, -4, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2, -6, -2, -6, -6,  0, -8, -6,  8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2,  0, -6, -2,  2, -6, -4, -2, -6, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2, -8, -2, -8, -6,  0, -8, -6,  4, -4,  8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2, -6, -2, -6, -4,  0, -6, -4,  2, -2,  4, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-4,  6, -6,  2,  0, -6,  0,  2, -6,  0, -6, -4, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2, -4, -6, -2, -2, -8, -4, -4, -6, -2, -6, -4, -4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2,  0, -6,  0,  4, -6, -4,  0, -6,  2, -4,  0,  0, -2, 10, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2, -2, -6, -4,  0, -6, -4,  0, -6,  4, -4, -2,  0, -4,  2, 10, 0, 0, 0, 0, 0, 0, 0],
    [2,  0, -2,  0,  0, -4,  0, -2, -4,  0, -4, -2,  2, -2,  0, -2,  8, 0, 0, 0, 0, 0, 0],
    [0, -2, -2, -2, -2, -4, -4, -4, -2, -2, -2, -2,  0, -2, -2, -2,  2, 10, 0, 0, 0, 0, 0],
    [0, -6, -2, -6, -4, -2, -6, -6,  6, -4,  2,  2, -6, -4, -4, -6, -4,  0, 8, 0, 0, 0, 0],
    [-6, -8, -4, -8, -6,  2, -4, -4, -6, -6, -4, -2, -8, -8, -4, -6, -6, -4, -6, 22, 0, 0, 0],
    [0, -2, -4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -4, -2, -2,  0,  0, -2, -4, -2,  0, 0],
    [-4, -6, -4, -6, -4,  6, -6,  4, -2, -4, -2, -2, -4, -6, -2, -4, -4, -4, -2,  4, -2, 14, 0],
    [-2,  2, -6,  2,  8, -6, -4,  0, -6,  2, -6, -2,  0, -2,  6,  0,  0, -2, -4, -6, -2, -4,  8]
    ]
)

blosum62mt2 = blosum62mt2.T + blosum62mt2
np.fill_diagonal(blosum62mt2, np.diag(blosum62mt2))
