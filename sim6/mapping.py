from helpers import *
'''
Generate the same plots as for the actual images. 
'''
depth = width = 128
position = np.loadtxt('positions.txt', delimiter = ',')
centers = position
name = 'hexpacking' #Name of file - also add path if you want to store it in some other folder

#X-sorted centers
depth_sort = qsort(centers, 0) 

#Y-sorted centers
width_sort = qsort(centers, 1)

#Net Total Density Distribution in x and y
denxy = density(depth_sort, depth, width, 10, 10)

#Profiles in x and y direction
depthsx, profilex = profile(depth_sort, depth, 0)
depthsy, profiley = profile(width_sort, width, 1)

#Entropy of system
rand_dist, entropy1 = entropy(depth_sort)
hist(denxy, 20, 'Histogram showing the density distribution of \
	ball bearings', 'Density', 'Frequency')
plt.savefig(name+'denxy.png')
plt.close()

plt.subplot(2,1,1)
plt.plot(depthsx, profilex)
plt.title('X-Profile for entropy is: {0}'.format(entropy1))
plt.xlabel('x')
plt.ylabel('Frequency')
plt.subplot(2,1,2)
plt.title('Y-Profile')
plt.xlabel('y')
plt.ylabel('Frequency')
plt.plot(depthsy, profiley)
plt.savefig(name+"profiles.png")
plt.close()
print entropy1

#-------------sparse-------------------
mask = position[:,1] > depth/2.
centers = position[mask] 
name = 'hexpackingsparse'

#X-sorted centers
depth_sort = qsort(centers, 0) 

#Y-sorted centers
width_sort = qsort(centers, 1)

#Net Total Density Distribution in x and y
denxy = density(depth_sort, depth, width, 10, 10)

#Profiles in x and y direction
depthsx, profilex = profile(depth_sort, depth, 0)
depthsy, profiley = profile(width_sort, width, 1)

#Entropy of system
rand_dist, entropy1 = entropy(depth_sort)
hist(denxy, 20, 'Histogram showing the density distribution \
 of ball bearings', 'Density', 'Frequency')
plt.savefig(name+'denxy.png')
plt.close()

plt.subplot(2,1,1)
plt.plot(depthsx, profilex)
plt.title('X-Profile for entropy is: {0}'.format(entropy1))
plt.xlabel('x')
plt.ylabel('Frequency')
plt.subplot(2,1,2)
plt.title('Y-Profile')
plt.xlabel('y')
plt.ylabel('Frequency')
plt.plot(depthsy, profiley)
plt.savefig(name+"profiles.png")
plt.close()
print entropy1