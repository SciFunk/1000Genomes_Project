import gzip
import sys
from collections import defaultdict

positions = [] #list of positions with variants to tie to sample name, format [14, 16, 273]
samplenames = [] #a list of samplenames, format ['HG00102', 'HG00103', 'HG00105',...]

with gzip.open(sys.argv[1]) as data: #instead of data = gzip.open((sys.argv[1]),"rb"), this will read file line-by-line
  for line in data:
    if line.startswith('##'): #skip all ~250 comment lines
      continue
    elif line.startswith('#'): #extract line with sample information
      samplenames = line.split()
    else:
      spline = line.split()
    for i,j in enumerate(spline): #i is the index of the element, j is the element itself
      if j == '0|1':
        positions.append(i)
      if j == '1|0':
        positions.append(i)
      if j == '1|1':
        positions.append(i)

print positions

variants = len(samplenames)*[0]
#print singletons

for i in positions:
    variants[i] += 1
#print singletons

pop_locations = open('pop_locations.txt', 'r')
sample_info = {}
for line in pop_locations:
  spline = line.split()
  sample_info[spline[0]] = spline[1:] #can use 1:3 if you only want pos 1:3 as values
            # defines key      values

pairs_dict = dict(zip(samplenames, variants)) #zip creates a paired list from my two separate lists, unordered from previous two lists

entriesToRemove = ('#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT')
for k in entriesToRemove:
    pairs_dict.pop(k, None)


#pairs_dict looks like {HG00102: 1, HG00103: 3, ...}
#sample_info looks like {HG00102: ['ACB', 'AFR', 'female'], ...}

new_dict = {}
for key in pairs_dict:
    sample_values = sample_info[key] #['GBR', 'EUR', 'female']
    pop = sample_values[0]
    new_dict[key] = pop, pairs_dict[key]

def writeDict(dict, filename, sep):
    with open(filename, "w") as f:
        for keys in dict.keys():
            dict_values = dict[keys]
            pop = dict_values[0]
            number = dict_values[1]
            f.write(keys + " " + pop + " " + str(number) + "\n")
def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            line = line.strip("\n")
            values = line.split(sep)
            dict[values[0]] = (values[1], values[2])
        return(dict)

dict2 = readDict("output.txt"," ")     
print dict2
for keys in dict2.keys():
  new_dict_values = new_dict[keys]
  number = int(new_dict_values[1])
  dict2_values = dict2[keys]
  entry1 = dict2_values[0]
  entry2 = int(dict2_values[1])
  entry2 += number                 #this won't write back to dict2 by itself
  dict2[keys] = (entry1, entry2)
print dict2
writeDict(dict2,"output.txt"," ")

#writeDict(new_dict,"output.txt",":")  #use this for first file to get all entries in output file
