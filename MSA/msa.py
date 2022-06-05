import numpy as np
from utils import read_fasta, estimate_population, generate_population

initial_alignment_df = read_fasta(filename='dataset/BB11001-m.fa')

# initial_alignment = [np.fromstring(sequence, dtype=np.uint8) for sequence in initial_alignment_df.get("sequence")]
initial_alignment = [sequence for sequence in initial_alignment_df.get("sequence")]

# initial_alignment = np.array(initial_alignment)

population = generate_population(size=20, alignment=initial_alignment)
print(population)
print(estimate_population(population))
#
# print(f'Estimated sequence value: {estimated_value}')
