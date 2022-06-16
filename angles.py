import numpy as np
from math import (
    asin, pi, atan2, cos
)
rotation_matrix = np.array ([[ 0.20243729, -0.91953164, -0.33686896],
 [ 0.49209472,  0.39292375, -0.77682283],
 [ 0.84667699, -0.00851353,  0.53203909]]) #with 6points

# rotation_matrix1 = np.array([[-0.22064269920312332, -0.4617600053263411, 0.859124261541587, 234.72254148475884], [0.9598344488925274, -0.2593061487344828, 0.10713613744982821, -194.45439187068186], [0.17330502014522942, 0.8482558686560958, 0.500427168809762, -197.8008351273745], [0, 0, 0, 1]]) #with 2 points, 10 & 11
R31 = rotation_matrix[2,0]
R32 = rotation_matrix[2,1]
R33 = rotation_matrix[2,2]
R21 = rotation_matrix[1,0]
R11 = rotation_matrix[0,0]
R12 = rotation_matrix[0,1]
R13 = rotation_matrix[0,2]

if R31 != 1 and R31 != -1:
     pitch_1 = -1*asin(R31)
     pitch_2 = pi - pitch_1
     roll_1 = atan2( R32 / cos(pitch_1) , R33 /cos(pitch_1) )
     roll_2 = atan2( R32 / cos(pitch_2) , R33 /cos(pitch_2) )
     yaw_1 = atan2( R21 / cos(pitch_1) , R11 / cos(pitch_1) )
     yaw_2 = atan2( R21 / cos(pitch_2) , R11 / cos(pitch_2) )

     # IMPORTANT NOTE here, there is more than one solution but we choose the first for this case for simplicity !
     # You can insert your own domain logic here on how to handle both solutions appropriately (see the reference publication link for more info).
     pitch = pitch_1
     roll = roll_1
     yaw = yaw_1
else:
     yaw = 0 # anything (we default this to zero)
     if R31 == -1:
        pitch = pi/2
        roll = yaw + atan2(R12,R13)
     else:
        pitch = -pi/2
        roll = -1*yaw + atan2(-1*R12,-1*R13)

# convert from radians to degrees
roll = roll*180/pi
pitch = pitch*180/pi
yaw = yaw*180/pi

rxyz_deg = [roll , pitch , yaw]

