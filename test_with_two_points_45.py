import numpy as np
from math import  pi, atan2
#rotation matrix for 4 and 5
import numpy as np
from math import  pi, atan2

rot_mat_45= np.array([[0.0, -0.6411220402496992, -0.7674389418748984, 199.02282042751108],
                      [0.9899130158903282, 0.10872803702741465, -0.0908319048301879, -389.9625753722497],
                      [0.14167646583295002, -0.759697797463063, 0.6346550524173401, -766.9110767578458],
                      [0, 0, 0, 1]])

X_stl4 = np.array ([[145.06],[45.00], [20.50],[1]])
X_stl5 = np.array ([[145.06],[45.00], [-9.50],[1]])

l4 = np.array( [[ 152.8431996 ],
 [-243.52405837],
 [-766.21508261],
                [1]]) #4x1

l5 = np.array([[ 179.05962927],
 [-240.42115583],
 [-787.89549084],
                [1]])
stl4 = np.linalg.pinv(rot_mat_45)@l4
print ('stl4', stl4)
stl5 = np.linalg.pinv(rot_mat_45)@l5
print ('stl5', stl5)

#error
mse4 = np.sum((stl4[1:] - X_stl4[1:])**2)
mse5 = np.sum((stl5[1:] - X_stl5[1:])**2)
#rotation angles
R31 = rot_mat_45[2,0]
R32 = rot_mat_45[2,1]
R33 = rot_mat_45[2,2]
R21 = rot_mat_45[1,0]
R11 = rot_mat_45[0,0]

theta_x = atan2(R32, R33)
theta_y = atan2(-R31, np.sqrt((R32)**2 + (R33)**2))
theta_z = atan2(R21,R11)





# T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
# calib_mat = T_tool_tip@rotation_matrix
# l11 = np.array([[295.63906894], [214.27023654], [-688.37736541],[1]])
# l10 = np.array([[255.29174604], [215.1138189], [-740.91453825],[1]])
#
# X_stl11 = np.array ([[-72.92],[-5.00], [-39.50],[1]])
# X_stl10 = np.array ([[-72.92],[5.00], [20.50],[1]])




stl11 = np.linalg.inv(rotation_matrix)@l11
print ('stl11', stl11)
stl10 = np.linalg.inv(rotation_matrix)@l10
print ('stl10', stl10)
mse11 = np.sum((stl11[1:] - X_stl11[1:])**2)
mse10 = np.sum((stl10[1:] - X_stl10[1:])**2)

print('mse11=', mse11, '\n', 'mse10=', mse10)

#find rotation angles
R31 = rotation_matrix[2,0]
R32 = rotation_matrix[2,1]
R33 = rotation_matrix[2,2]
R21 = rotation_matrix[1,0]
R11 = rotation_matrix[0,0]
R12 = rotation_matrix[0,1]
R13 = rotation_matrix[0,2]

# theta_x = atan2(r32,r33), theta_y= atan2(-r31, sqrt(r32^2 + r33^2)), theta_z = atan2(r21, r11)

theta_x = atan2(R32, R33)
theta_y = atan2(-R31, np.sqrt((R32)**2 + (R33)**2))
theta_z = atan2(R21,R11)

print('Imfusion matrix', rotation_matrix)
print('theta_x, theta_y, theta_z=', theta_x*180/pi, theta_y*180/pi, theta_z*180/pi)
