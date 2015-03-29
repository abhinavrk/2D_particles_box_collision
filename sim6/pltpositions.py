import numpy as np
import matplotlib.pyplot as plt
'''
Plot positions
'''
limit_x = limit_y = 100
position = np.loadtxt('positions.txt', delimiter = ',')

x = position[:,0]
y = position[:,1] 
plt.plot(x,y, 'ro')
plt.ylim([0,limit_y])
plt.xlim([0,limit_x])
plt.show()