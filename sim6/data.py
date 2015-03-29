import numpy as np
'''
Calculate difference in entropy between sparse and non-sparse sections. Code finds
the average difference in entropy and the standard deviation in the average difference
of entropy. The standard deviation may need to be divided number of observations 
(to get Standard Error of the mean) 
'''
a = open("entropy_all.txt")
b = open("entropy_sparse.txt")

all_name = []
sparse_name = []
all_val = []
sparse_val = []
avg = []

for line in a:
	words = line.split(',')
	all_name.append(words[0])
	all_val.append(float(words[1]))

for line in b:
	words = line.split(',')
	sparse_name.append(words[0])
	sparse_val.append(float(words[1]))

for i in range(len(sparse_name)):
	for j in range(len(all_name)):
		if sparse_name[i] == all_name[j]:
			diff = +sparse_val[i] - all_val[j]
			avg.append(diff)

print 'average: ', sum(avg)/float(len(avg))
print 'std: ', np.std(avg)
