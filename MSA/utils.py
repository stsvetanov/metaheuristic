import string
from random import random
from Bio import SeqIO

import numpy as np
import pandas as pd


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


def estimate_solution(solution):
    pass


amino_acid_order = "ABCDEFGHIKLMNPQRSTVWXYZ";
amino_acid_to_position = {np.uint8(ord(amino_acid)): position for position, amino_acid in enumerate(amino_acid_order)}

blosum62mt2 = np.tril(
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
