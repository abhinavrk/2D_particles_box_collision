import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as d

'''
Code to fix ball-ball positions if code time-step is too large. Only to be used for preliminary 
analysis. If code use is required then something is wrong with simulation. Usually its just a 
time-step issue. 
'''

limit_x = limit_y = 100
radius = 1
position = np.loadtxt('positions.txt', delimiter = ',')

def hist(array, block, title, xlab, ylab):
	hist, bins = np.histogram(array, bins=block)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.title(title)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.show()
	return plt.bar(center, hist, align='center', width=width)

c = d.pdist(position)
hist(c, 50, 'Histogram showing the pair-distribution of all ball bearings', 
'Distance between ball bearings', 'Frequency') # Histogram representation for average pixel density
plt.savefig('p_dist_hist_unadj.png')
plt.close()

l =0
pair_dist = d.cdist(position, position)
while np.any(pair_dist) and l<201:
	#Calculate distances
	pair_d = np.triu(pair_dist<=2*radius, k=1) # k=1 to exclude the diagonal
	for i, j in zip(*np.nonzero(pair_d)):
		# Fix positions
		# Move along the direction of the vector.
		# Basically a unit shift
		vec = (position[i][:] - position[j][:])
		norm = np.linalg.norm(vec)
		uvec = vec/norm
		# Swap positions
		position[i][:] += uvec
		position[j][:] -= uvec
	pair_dist = d.cdist(position, position)
	print l
	l+=1


xmax = position[:, 0] > limit_x - radius
xmin = position[:, 0] < radius
ymax = position[:, 1] > limit_y - radius
ymin = position[:, 1] < radius



# Force maximum positions
position[xmax|xmin|ymin|ymax] = [-10000, -10000]
positions = []
for x,y in position:
	if x == -10000 or y== -10000:
		pass
	else:
		positions.append([x,y])
positions = np.array(positions)
x = positions[:,0]
y = positions[:,1] 
plt.plot(x,y, 'ro')
plt.ylim([0,limit_y])
plt.xlim([0,limit_x])
plt.show()
np.savetxt('positions_adjusted.txt', positions, delimiter = ',')
plt.close()
c = d.pdist(positions)
hist(c, 50, 'Histogram showing the pair-distribution of all ball bearings', 
'Distance between ball bearings', 'Frequency') # Histogram representation for average pixel density
plt.savefig('p_dist_hist_adj.png')
