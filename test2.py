from math import atan2, pi

import numpy as np
##averaged points from NDI
# X_ndi =np.array([[216.400,257.59,220.51,259.03],[243.061,246.71,257.52,242.49],[-1007.001, -1005.94,-1085.49,-1081.34],[1, 1, 1, 1]])
# print('X_avg_pts=',X_ndi)
#
# ##Calibration matrix from tool to tip of stylus
# T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
# print('T_tool_tip=', T_tool_tip)
#
# ##measured points from phantom stl
#
# #7, 8, 10, 11
# X_stl = np.array ([[-72.92, -72.92, -72.92, -72.92],[45.00, 45.00, 5.00, -5.00], [20.50, -9.50, 20.50, -39.50],[1,1,1,1]])
# print('X_stl=', X_stl)
#
# #1,2,4,5
# X_stl2= np.array([[145.46, 145.46, 145.06, 145.06],[-5.02, -5.02, 45.00, 45.00],[15.52, -39.51, 20.50, -9.50],[1, 1, 1, 1]])
# print('X_stl2=', X_stl2)
#
# # calibrated_matrix = np.array([[1.0, 0.0, 0.0, 263.2933504383834], [0.0, 1.0, 0.0, 169.44191557107513], [0.0, 0.0, 1.0, -689.3961054221871], [0, 0, 0, 1]]) @ T_tool_tip
# calibrated_matrix = T_tool_tip @ np.array ([[-0.3541511072988597, -0.4381135438727337, 0.8262163856244111, 167.32632526312318], [-0.7493974633836316, -0.3955610483024122, -0.5309754221619633, 188.48109586906952], [0.5594465435349206, -0.8072099973000648, -0.1882327951916432, -587.9180412876891], [0, 0, 0, 1]])
# print(calibrated_matrix)
# print('array', np.array ([[-0.3541511072988597, -0.4381135438727337, 0.8262163856244111, 167.32632526312318], [-0.7493974633836316, -0.3955610483024122, -0.5309754221619633, 188.48109586906952], [0.5594465435349206, -0.8072099973000648, -0.1882327951916432, -587.9180412876891], [0, 0, 0, 1]]))

#####################################################################
#testing the matrix value with points 10 and 11
import numpy as np
from math import  pi, atan2
rotation_matrix = np.array ([[-0.7924732615277306, -0.06799655968598178, -0.6061044444932503, 211.920265036712],
                             [0.0312914806777264, 0.9879242888565274, -0.15174466291873343, 215.53222819329184],
                             [0.6091034173279578, -0.13921949345618015, -0.7807758702990307, -677.6475014062862],
                             [0, 0, 0, 1]])
T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
calib_mat = T_tool_tip@rotation_matrix
l11 = np.array([[295.63906894], [214.27023654], [-688.37736541],[1]])
l10 = np.array([[255.29174604], [215.1138189], [-740.91453825],[1]])

X_stl11 = np.array ([[-72.92],[-5.00], [-39.50],[1]])
X_stl10 = np.array ([[-72.92],[5.00], [20.50],[1]])

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

print('Imfusion matrix', calib_mat)
print('theta_x, theta_y, theta_z=', theta_x*180/pi, theta_y*180/pi, theta_z*180/pi)

##################################################################################################



##################################################################################################
#testing the matrix value with points 4, 5, 7, 8, 10, 11
import numpy as np
from math import pi, atan2
rotation_matrix_Imfusion = np.array([[-0.335724669460062, -0.4279631670401988, -0.839128401362303, 209.8644806194942], [-0.9116031705133709, -0.07671971498406384, 0.4038486657681743, 28.45002532730437], [-0.23721004579465568, 0.9005340709765992, -0.36437587898269336, -748.9177741600465], [0, 0, 0, 1]])
T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
calibrated_matrix = T_tool_tip@rotation_matrix_Imfusion
print('calibrated matrix-6points- with stylus',calibrated_matrix)
l11 = np.array([[1,0,0,295.63906894], [0,1,0,214.27023654], [0,0,1,-688.37736541],[0,0,0,1]])
l10 = np.array([[1,0,0,255.29174604], [0,1,0,215.1138189], [0,0,1,-740.91453825],[0,0,0,1]])
l8 =  np.array([[1,0,0,278.62649975], [0,1,0,161.00431415], [0,0,1,-660.46044652],[0,0,0,1]])
l7 =  np.array([[1,0,0,263.29335044], [0,1,0,169.44191557], [0,0,1,-689.39610542],[0,0,0,1]])
l5 =  np.array([[1,0,0,58.21396156], [0,1,0,-300.38515053], [0,0,1,-754.0867269],[0,0,0,1]])
l4 =  np.array([[1,0,0,29.0952322], [0,1,0,-299.92088442], [0,0,1,-798.89840965],[0,0,0,1]])

stl4 = np.linalg.pinv(calibrated_matrix)@l4
print ('stl4', stl4)
stl5 = np.linalg.pinv(calibrated_matrix)@l5
print ('stl5', stl5)
stl7 = np.linalg.pinv(calibrated_matrix)@l7
print ('stl7', stl7)
stl8 = np.linalg.pinv(calibrated_matrix)@l8
print ('stl8', stl8)
stl10 = np.linalg.pinv(calibrated_matrix)@l10
print ('stl10', stl10)
stl11 = np.linalg.pinv(calibrated_matrix)@l11
print ('stl11', stl11)

#find rotation angles
R31 = rotation_matrix_Imfusion[2,0]
R32 = rotation_matrix_Imfusion[2,1]
R33 = rotation_matrix_Imfusion[2,2]
R21 = rotation_matrix_Imfusion[1,0]
R11 = rotation_matrix_Imfusion[0,0]
R12 = rotation_matrix_Imfusion[0,1]
R13 = rotation_matrix_Imfusion[0,2]

# theta_x = atan2(r32,r33), theta_y= atan2(-r31, sqrt(r32^2 + r33^2)), theta_z = atan2(r21, r11)

theta_x = atan2(R32, R33)
theta_y = atan2(-R31, np.sqrt((R32)**2 + (R33)**2))
theta_z = atan2(R21,R11)

print('Imfusion matrix', calibrated_matrix)
print('theta_x, theta_y, theta_z=', theta_x*180/pi, theta_y*180/pi, theta_z*180/pi)
############################################################




############################################################
#testing with 4 points, 7, 8, 10, 11
import numpy as np
from math import pi, atan2
T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
rotation_matrix_4pts = np.array([[0.6905398866515573, -0.16095335536408978, -0.7051586221129929, 325.7779680785976], [-0.4904756508740635, -0.8207310815915437, -0.29297461939430536, 172.07258692528444], [-0.5315903505923689, 0.5481737946186552, -0.6456912497862012, -747.1759751436877], [0, 0, 0, 1]])
matrix_with_calibrated_stylus = T_tool_tip@rotation_matrix_4pts
print(matrix_with_calibrated_stylus)
# l11 = np.array([[1,0,0,295.63906894], [0,1,0,214.27023654], [0,0,1,-688.37736541],[0,0,0,1]])
l11 = np.array([[295.63906894],[214.27023654],[-688.37736541],[1]])
# l10 = np.array([[1,0,0,255.29174604], [0,1,0,215.1138189], [0,0,1,-740.91453825],[0,0,0,1]])
# l8 =  np.array([[1,0,0,278.62649975], [0,1,0,161.00431415], [0,0,1,-660.46044652],[0,0,0,1]])
# l7 =  np.array([[1,0,0,263.29335044], [0,1,0,169.44191557], [0,0,1,-689.39610542],[0,0,0,1]])
# stl7 = np.linalg.pinv(rotation_matrix_4pts)@l7
# print ('stl7', stl7)
# stl8 = np.linalg.pinv(rotation_matrix_4pts)@l8
# print ('stl8', stl8)
# stl10 = np.linalg.pinv(rotation_matrix_4pts)@l10
# print ('stl10', stl10)
stl11 = np.linalg.pinv(rotation_matrix_4pts)@l11
print ('stl11', stl11)

#find rotation angles
R31 = rotation_matrix_4pts[2,0]
R32 = rotation_matrix_4pts[2,1]
R33 = rotation_matrix_4pts[2,2]
R21 = rotation_matrix_4pts[1,0]
R11 = rotation_matrix_4pts[0,0]
R12 = rotation_matrix_4pts[0,1]
R13 = rotation_matrix_4pts[0,2]

# theta_x = atan2(r32,r33), theta_y= atan2(-r31, sqrt(r32^2 + r33^2)), theta_z = atan2(r21, r11)

theta_x = atan2(R32, R33)
theta_y = atan2(-R31, np.sqrt((R32)**2 + (R33)**2))
theta_z = atan2(R21,R11)

print('Imfusion matrix', rotation_matrix_4pts)
print('theta_x, theta_y, theta_z=', theta_x*180/pi, theta_y*180/pi, theta_z*180/pi)