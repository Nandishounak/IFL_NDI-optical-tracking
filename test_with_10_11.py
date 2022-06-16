import numpy as np
from math import  pi, atan2
#rotation matrix for 10 and 11
import numpy as np
from math import  pi, atan2

rot_mat_1011= np.array([[0.41885774943862114, 0.03252093567132876, -0.9074693242629606, 232.82339538675697],
                         [0.8059997833430381, 0.4469770438720677, 0.388041069350093, 288.29753503394187],
                         [0.4182374146178089, -0.8939540877441353, 0.16100793154177828, -705.1726476387346],
                         [0, 0, 0, 1]])

X_stl10 = np.array ([[72.92],[-5.00], [20.50],[1]])
X_stl11 = np.array ([[72.92],[-5.00], [-39.50],[1]])

l10 = np.array( [[ 194.07076025 ],
 [230.73007377],
 [-729.77302244],
                [1]]) #4x1

l11 = np.array([[ 227.40652415],
 [ 216.47543714],
 [-735.68762721],
                [1]])
stl10 = np.linalg.pinv(rot_mat_1011)@l10
print ('stl10', stl10)
stl11 = np.linalg.pinv(rot_mat_1011)@l11
print ('stl11', stl11)

#error
mse10 = np.sum((stl10[1:] - X_stl10[1:])**2)
mse11= np.sum((stl11[1:] - X_stl11[1:])**2)