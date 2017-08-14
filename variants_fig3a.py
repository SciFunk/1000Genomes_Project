import gzip
import sys
import math

def variants_to_blank_dict(samplenames, variants):
  pairs_dict = dict(zip(samplenames, variants))
  entriesToRemove = ('#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT')
  for k in entriesToRemove:
      pairs_dict.pop(k, None)
  blank_dict = {'ESN': 0, 'GWD': 0, 'LWK': 0, 'MSL': 0, 'YRI': 0, 'ACB': 0, 'ASW': 0, 'CLM': 0,
        'MXL': 0, 'PEL': 0, 'PUR': 0, 'CDX': 0, 'CHB': 0, 'CHS': 0, 'JPT': 0, 'KHV': 0,
        'CEU': 0, 'GBR': 0, 'FIN': 0, 'IBS': 0, 'TSI': 0, 'BEB': 0, 'GIH': 0, 'ITU': 0,
        'PJL': 0, 'STU': 0}
  for keys in pairs_dict.keys():  # pairs_dict.keys = list of the keys in pairs_dict
    entry1 = pairs_dict[keys]     #number of variants
    entry2 = sample_info[keys]    #['GBR', 'EUR', 'female']
    pop = entry2[0]
    try:
        blank_dict[pop] += float(entry1)
    except KeyError:
         blank_dict[pop] = entry1
  return(blank_dict)

pop_locations = open('pop_locations.txt', 'r')
#pop_locations = open('C:\\Users\\SciFunk\\Downloads\\pop_locations.txt', 'r')
sample_info = {}
for line in pop_locations:
  spline = line.split()
  sample_info[spline[0]] = spline[1:] #can use 1:3 if you only want pos 1:3 as values

pop_percents = {'ESN': 10,'GWD': 11,'LWK': 9,'MSL': 8,'YRI': 10,'ACB': 8,
              'ASW': 6,'CLM': 9,'MXL': 6,'PEL': 8,'PUR': 10,'CDX': 9,
              'CHB': 10,'CHS': 10,'JPT': 10,'KHV': 9,'CEU': 9,'GBR': 9,
              'FIN': 9,'IBS': 10,'TSI': 10,'BEB': 8,'GIH': 10,'ITU': 10,
              'PJL': 9,'STU': 10}

samplenames = [] #a list of samplenames format ['HG00102', 'HG00103', 'HG00105',...]
final_dict = {'ESN': 0, 'GWD': 0, 'LWK': 0, 'MSL': 0, 'YRI': 0, 'ACB': 0, 'ASW': 0, 'CLM': 0,
      'MXL': 0, 'PEL': 0, 'PUR': 0, 'CDX': 0, 'CHB': 0, 'CHS': 0, 'JPT': 0, 'KHV': 0,
      'CEU': 0, 'GBR': 0, 'FIN': 0, 'IBS': 0, 'TSI': 0, 'BEB': 0, 'GIH': 0, 'ITU': 0,
      'PJL': 0, 'STU': 0}

with gzip.open(sys.argv[1]) as data: #instead of data = gzip.open((sys.argv[1]),"rb"), this will read file line-by-line
#with gzip.open('C:\\Users\\SciFunk\\Downloads\\Working\\chr1small.vcf.gz') as data:
    for line in data:
      if line.startswith('##'): #skip all ~250 comment lines
          continue
      elif line.startswith('#'): #extract line with sample information
          samplenames = line.split()
      else:
        spline = line.split()
        u = spline.count("2|2")
        w = spline.count("0|0")
        x = spline.count("0|1")
        y = spline.count("1|0")
        z = spline.count("1|1")
        positions = []
        theSum = x + y + 2*z
        zeroSum = x + y + 2*w
        if u == 0:
            if zeroSum < 25:
                for i,j in enumerate(spline): #i is the index of the element, j is the element itself
                  if j == '0|1':
                    positions.append(i)
                  if j == '1|0':
                    positions.append(i)
                  if j == '0|0':
                    positions.append(i)
                variants = len(samplenames)*[0]
                for i in positions:
                  variants[i] += 1
                blank_dict = variants_to_blank_dict(samplenames, variants)
                for key in blank_dict:
                    if blank_dict[key] > pop_percents[key]:
                        final_dict[key] += 1
                        print key
                        print "blank_dict:", blank_dict[key]
                        print "final_dict:", final_dict[key]
                        print spline
            if theSum < 25:
                for i,j in enumerate(spline): #i is the index of the element, j is the element itself
                  if j == '0|1':
                    positions.append(i)
                  if j == '1|0':
                    positions.append(i)
                  if j == '1|1':
                    positions.append(i)
                variants = len(samplenames)*[0]
                for i in positions:
                  variants[i] += 1
                blank_dict = variants_to_blank_dict(samplenames, variants)
                for key in blank_dict:
                    if blank_dict[key] > pop_percents[key]:
                        final_dict[key] += 1
                        print key
                        print "blank_dict:", blank_dict[key]
                        print "final_dict:", final_dict[key]


    print final_dict

    # dict2 = readDict("variants_fig3a.txt"," ")
    # for keys in dict2.keys():
    #   dict2[keys] += final_dict[keys]
    # writeDict(dict2,"variants_fig3a.txt"," ")
