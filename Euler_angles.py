from math import pi, atan2
import numpy as np
class Euler_angles:
    def Euler(self, rotation_matrix_8pts):
        R31 = rotation_matrix_8pts[2, 0]
        R32 = rotation_matrix_8pts[2, 1]
        R33 = rotation_matrix_8pts[2, 2]
        R21 = rotation_matrix_8pts[1, 0]
        R11 = rotation_matrix_8pts[0, 0]
        R12 = rotation_matrix_8pts[0, 1]
        R13 = rotation_matrix_8pts[0, 2]

        theta_x = atan2(R32, R33)
        theta_y = atan2(-R31, np.sqrt((R32) ** 2 + (R33) ** 2))
        theta_z = atan2(R21, R11)
        print('theta_x, theta_y, theta_z=', theta_x * 180 / pi, theta_y * 180 / pi, theta_z * 180 / pi)

        return theta_x, theta_y, theta_z

