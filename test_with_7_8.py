from math import  pi, atan2
import numpy as np
rot_mat_78 = np.array([[0.6568164047443409, -0.043573155101551554, -0.7527905356825456, 250.00258107533455],
                       [0.5530656598847987, 0.7064351987813519, 0.4416646757201036, 218.62264641280308],
                       [0.512553008297591, -0.706435198781352, 0.4880970432279236, -609.2053983216418],
                       [0, 0, 0, 1]])

X_stl7 = np.array ([[-72.92],[45.00], [20.50],[1]])
X_stl8 = np.array ([[-72.92],[45.00], [-9.50],[1]])

l7 = np.array([[ 190.20778301],
 [ 215.91389925],
 [-671.92609288] ,[1]]) #4x1
l8 = np.array([[ 201.80499482],
 [ 209.10977706],
 [-679.44553491] , [1]])

stl7 = np.linalg.pinv(rot_mat_78)@l7
print ('stl7', stl7)
stl8 = np.linalg.pinv(rot_mat_78)@l8
print ('stl8', stl8)

#error
mse7 = np.sum((stl7[1:] - X_stl7[1:])**2)
mse8 = np.sum((stl8[1:] - X_stl8[1:])**2)
#rotation angles
# R31 = rot_mat_45[2,0]
# R32 = rot_mat_45[2,1]
# R33 = rot_mat_45[2,2]
# R21 = rot_mat_45[1,0]
# R11 = rot_mat_45[0,0]
#
# theta_x = atan2(R32, R33)
# theta_y = atan2(-R31, np.sqrt((R32)**2 + (R33)**2))
# theta_z = atan2(R21,R11)



