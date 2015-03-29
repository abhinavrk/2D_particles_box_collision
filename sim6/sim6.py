from helpers import *
# ---------------------------------------------------------------------------------
# Actual Simulation Code

# 2D container parameters
limit_x = 128
limit_y = 128

#Number and radius of particles
number_of_particles = 2878
radius = 1.0

# Initialize positions (hexagonal packing)
position = force_init_hex(number_of_particles, radius, limit_x, limit_y)
a = np.random.randn(number_of_particles/2, 2)
b = np.random.randn(number_of_particles,) /25.0 #very small random variation upon constant vel

# Symmetric Random Velocity
velocity = np.vstack((a, a[::-1]))
velocity[:, 1] = 0.5 # Standard positive velocity
velocity[:,1] += b[:]

l=0
c = np.amax(abs(velocity))
gain = 1.0 # No gain in terms of collisions
alpha = 0.025 # Learning Rate/Time Step
loss = 0.9998**2 # Frictional loss
ball_loss = 1 # Ball-ball collisional loss
wall_loss = -1.0 # Wall-ball collision loss
gravity = .138/26.9 #cm/s/s
while c > 0.01 and l<20000:
	# Assume velocity dies down extremely slowly. 
	# Need 5000 cycles at least
	# Frictional loss
	velocity*=loss

	#Check if particles collide with a wall:

	# Masks for particles beyond the boundary
	xmax = position[:, 0] > limit_x - radius
	xmin = position[:, 0] < radius
	ymax = position[:, 1] > limit_y - radius
	ymin = position[:, 1] < radius

	velocity[xmax | xmin, 0] *= wall_loss
	velocity[ymax | ymin, 1] *= wall_loss

	# Force maximum positions - Only needed if time steps are large
	position[xmax, 0] = limit_x - radius 
	position[ymax, 1] = limit_y - radius 
	position[xmin, 0] = radius 
	position[ymin, 1] = radius 

	#Calculate distances between particles:
	pair_dist = d.cdist(position, position)
	pair_d = np.triu(pair_dist<=2*radius, k=1) # k=1 to exclude the diagonal
	a = np.zeros((len(position),1))
	for i, j in zip(*np.nonzero(pair_d)):
		vi = velocity[i,:]
		vj = velocity[j,:]
		si = position[i,:]
		sj = position[j,:]
		a[i] = 1.0
		a[j] = 1.0
		#Physically accurate ball-ball interactions simulated
		vi_new = vi + (np.dot(vj-vi, sj-si) * (sj-si))/float(np.dot(sj-si, sj-si))
		vj_new = vj + (np.dot(vi-vj, sj-si) * (sj-si))/float(np.dot(sj-si, sj-si))
		velocity[i,:] = vi_new
		velocity[j,:] = vj_new	

	# Moderated ball-ball collision approach
	# Assuming 0.5% loss for ball ball collision
	for index in a:
		velocity[index[0],:] *= ball_loss

	# # Try to simulate the 3 tier system
	# xmask1 = (position[:, 0] > x1 - radius) & (position[:,0]< x1 + radius)
	# xmask2 = (position[:, 0] > x2 - radius) & (position[:,0]< x2 + radius)
	# ymask1 = (position[:, 1] > y1 - radius) & (position[:,1]< y1 + radius)
	# ymask2 = (position[:, 1] > y2 - radius) & (position[:,1]< y2 + radius)

	# velocity[xmask1|xmask2, 1] *= 1.0075
	# velocity[ymask1|ymask2, 0] *= 1.01

	# Update position add grav to velocity
	position += alpha * velocity
	velocity[:,1] -= gravity * alpha

	if l%50 ==0:
		x = position[:,0]
		y = position[:,1] 
		plt.plot(x,y, 'ro')
		plt.ylim([0,limit_y])
		plt.xlim([0,limit_x])
		name = 'dist{0}.png'.format(l)
		plt.savefig(name)
		plt.close()
	
	c = np.amax(abs(velocity))
	l += 1
	print l-1, c


# Analysis
np.savetxt('positions.txt', position, delimiter = ',')

depth_sort = qsort(position, 0) 
den = density(depth_sort, limit_x, limit_y, 10, 10)
den1 = []

for item in den:
	if item>10:
		den1.append(item)

hist(den1, 50, 'Histogram showing density distribution of simulated distribution',
 'Density of ball bearings', 'Frequency')
plt.savefig('density_hist1.png')
plt.close()

hist(den1, 25, 'Histogram showing density distribution of simulated distribution',
 'Density of ball bearings', 'Frequency')
plt.savefig('density_hist2.png')
plt.close()

hist(den1, 10, 'Histogram showing density distribution of simulated distribution',
 'Density of ball bearings', 'Frequency')
plt.savefig('density_hist3.png')
plt.close()

c = d.pdist(position)
hist(c, 50, 'Histogram showing the pair-distribution of all ball bearings',
 'Distance between ball bearings', 'Frequency') # Histogram representation for average ball density
plt.savefig('p_dist_hist.png')