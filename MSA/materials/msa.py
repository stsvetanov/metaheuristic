import pandas as pd

alignments = {}

with open('../dataset/BB11001.fa') as file_handler:
    for line in file_handler:
        if line.startswith('>'):
            key = line[0:].strip()
            value = [ch.strip() for ch in next(file_handler)]
            alignments[key] = value

print(alignments)
df1 = pd.DataFrame(alignments)
print(df1)
df2 = df1.rename(columns=df1.iloc[0]).loc[1:]
print(df2)

