import timeit

# import phylopandas as ph
import numpy as np
from utils import amino_acid_to_position, blosum62mt2, read_fasta

# df1 = ph.read_fasta('H1N1_Protein_NS2_149.fa')

df1 = read_fasta(filename='dataset/H1N1_Protein_NS2_149.fa')
# print(df1.columns.values)
# print(df1.info)

alignment = [np.fromstring(sequence, dtype=np.uint8) for sequence in df1.get("sequence")]

alignment = np.array(alignment)

sum_total = 0

start_time = timeit.default_timer()
for column in alignment.T[:5]:
    column_len = len(column)
    sum_column = 0
    for i in range(column_len - 1):
        position_first = amino_acid_to_position.get(column[i])
        position_second = amino_acid_to_position.get(column[i + 1])
        sum_column += blosum62mt2[position_first][position_second]
    sum_total += sum_column

print(sum_total)
print(timeit.default_timer() - start_time)
