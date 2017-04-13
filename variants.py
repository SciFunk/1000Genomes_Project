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

ds = [pairs_dict, sample_info]
new_dict = {}
for key in pairs_dict:
    new_dict[key] = tuple(new_dict[key] for new_dict in ds)

print new_dict

def writeDict(dict, filename, sep):
    with open(filename, "w") as f:
        for i in dict.keys():
            f.write(i + " " + str(dict[i]) + "\n")
def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = int(values[1])
        return(dict)

#dict2 = readDict("outputSingletons.txt"," ")     comment out for first file
#for keys in dict2.keys():
#  dict2[keys] += new_dict[keys]
#writeDict(dict2,"outputSingletons.txt"," ")

writeDict(new_dict,"outputSingletons.txt"," ")  #use this for first file to get all entries in output file
