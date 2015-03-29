import numpy as np 
import scipy.spatial.distance as d
import matplotlib.pyplot as plt

# Helper Functions
def qsort(a, i):
	'''
	Sort array. 
	'''
    return sorted(a, key = lambda arr: arr[i])

def search(a, pos, value_start, value_end):
	'''
	Search for a value within ordered lists. 
	Never used directly -> helper of helper.
	'''
	if len(a)<1:
		return []
	empty = []
	i = 0
	for x in a:
		if x[pos] < value_end and x[pos]>=value_start:
			empty.append(x)
			i+=1
		elif x[pos]<value_start:
			i+=1
		else:
			return empty
	return empty

def density(arr, depth, width, points_d, points_w ):
	'''
	Split region into smaller rectangles -> get density in each 
	rectangle
	'''
	# arr is a depth sorted array
	# depth, width are the image dimension
	# points_d, points_w are the number of points across depth and width.
	density = []
	depths = np.linspace(0, depth, points_d, endpoint = True)
	depths = depths.astype(int)
	widths = np.linspace(0, width, points_w,  endpoint = True)
	widths = widths.astype(int)

	for i in range(len(depths)-1):
		a = search(arr, 0, depths[i], depths[i+1])
		b = qsort(a,1)
		for j in range(len(widths)-1):
			c = search(b, 1, widths[j], widths[j+1])
			density.append(len(c))
	return density

def hist(array, block, title, xlab, ylab):
	'''
	Generate histogram from given data in array
	putting it into bins (#bins = block) with the given
	title and labels
	'''
	hist, bins = np.histogram(array, bins=block)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.title(title)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.show()
	return plt.bar(center, hist, align='center', width=width)

def force_init_hex(n, radius, limit_x, limit_y):
	'''
	Initial setup is hexagonally packed.  
	'''
   	x_range = np.arange(radius, limit_x, 2*radius)
   	y_range = np.arange(radius, limit_y, 2*radius)
   	i = 0
   	shift = 1* radius
   	positions = []
   	while i<n:
   		for y in y_range:
   			for x in x_range:
   				positions.append([float(x+shift),float(y)])
   				i+=1
   			if shift == 1* radius:
   				shift = 0.
   			else:
   				shift = 1*radius	
   	positions = positions[:n]
   	return np.array(positions)

def force_init(n, radius, limit_x, limit_y):
	'''
	Initial setup is square packed. 
	'''
   	x_range = np.arange(radius, limit_x, 2*radius)
   	y_range = np.arange(radius, limit_y, 2*radius)
   	i = 0
   	positions = []
   	while i<n:
   		for y in y_range:
   			for x in x_range:
   				positions.append([float(x),float(y)])
   				i+=1
   				
   	positions = positions[:n]
   	return np.array(positions)

def entropy(centers):
	'''
	Calculates natural length scale of balls
	Sets entropy to be std.dev in natural length scale 
	normalized against natural length scale
	'''
	dist = []
	N = len(centers)
	for i in range(N):
		ind1 = np.random.randint(0,N)
		ind2 = np.random.randint(0,N)
		distance = (centers[ind1][0]-centers[ind2][0])**2 + (centers[ind1][1]-centers[ind2][1])**2
		distance = distance**0.5
		dist.append(distance)
	norm = float(sum(dist))/float(len(dist))
	entropy = np.std(dist)/norm
	return dist, entropy
	
def profile(arr, depth, j):
	'''
	Returns density profile along j'th axis
	j = 0 = x
	j = 1 = y
	'''
	# arr is a depth sorted array
	# depth/width is the profile direction
	# points_d is the number of points across depth
	profile = []
	step = 1.
	current = 0.
	window = 10.
	depths = []
	while current+window<depth:
		a = search(arr, j, current, current+window)
		profile.append(len(a))
		current += step
		depths.append(current+window/2.)
		
	return depths, profile
