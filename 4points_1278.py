#testing with 4 points, 1,2,7,8
import numpy as np
from math import pi, atan2
rotation_matrix_4pts = np.array([[-0.08750108382897172, -0.03062355143123814, -0.995693606701626, 196.5882646445594],
                                 [-0.989372409893596, -0.11384882109618948, 0.0904471142510642, 22.954248797713717],
                                 [-0.11612835515106767, 0.9930260037042061, -0.020336201640457265, -771.7157160687659],
                                 [0, 0, 0, 1]])
# stl points true value
X_stl1 = np.array ([[145.46],[-5.02], [15.52],[1]])
X_stl2 = np.array ([[145.46 ],[-5.02], [-39.51],[1]])
X_stl7 = np.array ([[-72.92],[45.00], [20.50],[1]])
X_stl8 = np.array ([[-72.92],[45.00], [-9.50],[1]])

# average points from script
l1 = np.array([[ 164.87264043],
 [-240.70988071],
 [-838.54659486],[1]])
l2 = np.array([[ 227.25838386],
 [-246.31320939],
 [-834.12601688],[1]])
l7 = np.array([[ 190.20778301],
 [ 215.91389925],
 [-671.92609288] ,[1]]) #4x1
l8 = np.array([[ 201.80499482],
 [ 209.10977706],
 [-679.44553491] , [1]])

# print backcalculation result
stl1 = np.linalg.pinv(rotation_matrix_4pts)@l1
print ('stl1', stl1)
stl2 = np.linalg.pinv(rotation_matrix_4pts)@l2
print ('stl2', stl2)
stl7 = np.linalg.pinv(rotation_matrix_4pts)@l7
print ('stl7', stl7)
stl8 = np.linalg.pinv(rotation_matrix_4pts)@l8
print ('stl8', stl8)

#error
mse1 = np.sum((stl1[1:] - X_stl1[1:])**2)
mse2 = np.sum((stl2[1:] - X_stl2[1:])**2)
mse7 = np.sum((stl7[1:] - X_stl7[1:])**2)
mse8 = np.sum((stl8[1:] - X_stl8[1:])**2)