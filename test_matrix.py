import numpy as np
import matplotlib.pyplot as plt


#T_cam_tool =np.array ([[2.1474, 2.49, 1.919, 2.207], [2.073, 2.038, 1.643, 1.672], [-1.082, -1.075, -1.13, -1.1132], [1, 1, 1, 1]])
#for the landmark points 7,8,10,11
X_ndi =np.array([[216.400,257.59,220.51,259.03],[243.061,246.71,257.52,242.49],[-1007.001, -1005.94,-1085.49,-1081.34],[1, 1, 1, 1]])
print('X_avg_pts=',X_ndi)
# X_ndi2 = np.array([[1.869930959504803525e+02, 2.407022498357057998e+02, 1.828847682943508062e+02, 2.017031198960148117e+02],[-2.316018003451187610e+02, -2.337430756308815774e+02, -2.295291639323316701e+02, -2.199589825606927604e+02],[-1.094580870019316990e+03, -1.095315907751112945e+03, -1.041311693856054262e+03, -1.028490689134763898e+03],[1, 1, 1 ,1]])
T_tool_tip =np.array([[1,0,0,-18.6831],[0,1,0,0.0823379],[0, 0, 1,-157.464],[0,0,0,1]])
print('T_tool_tip=', T_tool_tip)
#A = T_tool_tip@X_avgpts
#print(A)
X_stl = np.array ([[-72.92, -72.92, -72.92, -72.92],[45.00, 45.00, 5.00, -5.00], [20.50, -9.50, 20.50, -39.50],[1,1,1,1]])
print('X_stl=', X_stl)
X_stl2= np.array([[145.46, 145.46, 145.06, 145.06],[-5.02, -5.02, 45.00, 45.00],[15.52, -39.51, 20.50, -9.50],[1, 1, 1, 1]])
# T_i = T_tool_tip@X_stl
# T_i2= T_tool_tip@X_stl2
# print('T_i=', T_i)
# print('T_i2', T_i2)
# X_transformedstl = np.linalg.lstsq(T_tool_tip, X_ndi)
#print(X_transformedstl)

# X_imfusion = X_ndi@np.linalg.pinv(X_avgpts)
# print('Inverse of X_avgpts=', np.linalg.pinv(X_avgpts))
# print('X_imfusuion=', X_imfusion)


# T_imf = np.dot(X_ndi, np.linalg.pinv(T_i))
# # print('Inverse of X_ndi=', np.linalg.pinv(X_ndi))
# print('X_cam_tool=', T_imf)
#
# T_imf2 = np.dot(X_ndi2, np.linalg.pinv(T_i2))
# print('T_cam_tool2=', np.around(T_imf2).astype(float))

# test_array = np.array([[5, 5, 5, 5], [6,6,6,6], [7,7,7,7],[0,0,0,1]])
# test_array_2 = np.array([[4,4,3,3],[2,3,4,5],(5,6,9,3),[1,1,1,1]])
# test_output = test_array@test_array_2
# print(test_output)
# A = test_output@np.linalg.inv(test_array_2)
# print(A)
# A_inverse_A = np.dot(test_array_2, (np.linalg.inv(test_array_2)))
# print(np.around(A_inverse_A).astype(int))
# print(np.linalg.det(test_array_2))


#########################################################
X_rigid_reg = np.array([[263.29335044, 278.62649975, 255.29174604, 295.63906894], [169.44191557, 161.00431415, 215.1138189, 214.27023654],[-689.39610542, -660.46044652, -740.91453825, -688.37736541],[1,1,1,1]])
# T_intermediate = T_tool_tip@X_stl
# print(T_intermediate)

#X_ndi = calibration matrix * X_stl
#temp = X_rigid_reg@T_tool_tip
#print(temp)
T_cam_tip = X_rigid_reg@np.linalg.pinv(X_stl)
print(T_cam_tip)
cam_tip_inv = np.linalg.pinv(T_cam_tip)
print('cam_tip_inv', cam_tip_inv)
X_calculated_stl = cam_tip_inv@X_rigid_reg

# LSE = np.linalg.lstsq(X_rigid_reg, X_ndi)
# print(LSE)