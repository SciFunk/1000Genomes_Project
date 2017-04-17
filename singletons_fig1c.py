import gzip
import sys
#from collections import defaultdict #simpler/more automated than using dict to make a dictionary of lists, uses default key value

singletonpos = [] #list of positions with singletons to tie to sample name, format [14, 16, 273]
samplenames = [] #a list of samplenames format ['HG00102', 'HG00103', 'HG00105',...]

with gzip.open(sys.argv[1]) as data: #instead of data = gzip.open((sys.argv[1]),"rb"), this will read file line-by-line
  for line in data: #sort through all lines to get singletons
      if line.startswith('##'): #skip all ~250 comment lines
          continue
      elif line.startswith('#'): #extract line with sample information
          samplenames = line.split()
      spline = line.split()
      x = spline.count("1|0")
      y = spline.count("0|1")
      if x + y == 1:
          if x > 0:
              index = spline.index("1|0")
              singletonpos.append(index)
          else:
              index2 = spline.index("0|1")
              singletonpos.append(index2)
  #    index3 = spline.index("1")
   #   singletonpos.append(index3)
            
#print samplenames 
#print singletonpos

singletons = len(samplenames)*[0]
#print singletons

for i in singletonpos:
    singletons[i] += 1
#print singletons

pop_locations = open('pop_locations.txt', 'r')
sample_info = {}
for line in pop_locations:
  spline = line.split()
  sample_info[spline[0]] = spline[1:] #can use 1:3 if you only want pos 1:3 as values
            # defines key      values

pairs_dict = dict(zip(samplenames, singletons)) #zip creates a paired list from my two separate lists, unordered from previous two lists

entriesToRemove = ('#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT')
for k in entriesToRemove:
    pairs_dict.pop(k, None)

#pairs_dict looks like {HG00102: 1, HG00103: 3, ...}
#sample_info looks like {HG00102: ['ACB', 'AFR', 'female'], ...}

new_dict = {}
for keys in pairs_dict.keys():  # pairs_dict.keys = list of the keys in pairs_dict
  entry1 = pairs_dict[keys] #number of singletons
  entry2 = sample_info[keys] #['GBR', 'EUR', 'female'] 
  pop = entry2[0]
  try:
      new_dict[pop] += int(entry1)
  except KeyError:
      new_dict[pop] = entry1
print new_dict

# see http://stackoverflow.com/questions/11026959/writing-a-dict-to-txt-file-and-reading-it-back
def writeDict(dict, filename, sep):
    with open(filename, "a") as f:
        for i in dict.keys():            
            f.write(i + " " + str(dict[i]) + "\n")
            
def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = int(values[1])
        return(dict)
 
dict2 = readDict("outputSingletons.txt"," ")
for keys in dict2.keys():
  dict2[keys] += new_dict[keys]
writeDict(dict2,"outputSingletons.txt"," ")





  
