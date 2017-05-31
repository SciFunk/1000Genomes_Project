import sys
import gzip
from collections import Counter

header = []
header_length = None

pop_map = {}

# get parent pop for each individual ID
with open('pop_locations.txt') as infile:
    infile.readline()
    for line in infile:
        bits = line.strip().split('\t')
        ID, pop = bits[:2]
        pop_map[ID] = pop

final_pop_info = Counter()

with gzip.open('C:\\Users\\SciFunk\\Downloads\\chr1small.vcf.gz') as data:
    for line in data:
        if line.startswith(##):
            continue
        if line.startswith("#"): # is header
            header = line.strip().split('\t')[9:]
            header_length = len(header)  #use in calculation below
            continue
        bits = line.strip().split('\t')[9:]
        bits = [sum(map(int, b.split('|'))) for b in bits]
        fraction = (sum(bits) / (2 * header_length)) * 100
        if fraction >= 0.5:
            continue

        pop_counts = Counter()
        pop_max = Counter()  #gives total number of each pop
        for ID, snps in zip(header, bits):
            pop = pop_map[ID]
            pop_counts[pop] += snps
            pop_max[pop] += 2

        for pop, count in pop_counts.items():
            percentage = (count / pop_max[pop]) * 100
            if percentage > 5:
                final_pop_info[pop] += 1


# print a tab-separated summary of the data
for k, v in sorted(final_pop_info.items()):
    print('{}\t{}'.format(k, v))
