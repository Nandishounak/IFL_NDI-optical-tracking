"""Euler angle extraction from a 3x3 rotation matrix."""

from math import pi, atan2
import numpy as np


class Euler_angles:
    """Extract intrinsic XYZ Euler angles from a rotation matrix."""

    def Euler(self, rotation_matrix):
        """Return (theta_x, theta_y, theta_z) in radians.

        Parameters
        ----------
        rotation_matrix : np.ndarray, shape (3, 3)
            Rotation matrix from the rigid registration.

        Returns
        -------
        tuple of float
            Euler angles (theta_x, theta_y, theta_z) in radians.
        """
        R = rotation_matrix
        theta_x = atan2(R[2, 1], R[2, 2])
        theta_y = atan2(-R[2, 0], np.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
        theta_z = atan2(R[1, 0], R[0, 0])

        print(
            f"Euler angles (deg): "
            f"x={theta_x * 180 / pi:.2f}, "
            f"y={theta_y * 180 / pi:.2f}, "
            f"z={theta_z * 180 / pi:.2f}"
        )

        return theta_x, theta_y, theta_z
