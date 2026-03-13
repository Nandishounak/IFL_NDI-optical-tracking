"""Compute the rigid transformation between NDI tracking and STL phantom coordinates."""

import os
import numpy as np
import imfusion

os.environ["PATH"] = (
    "/usr/include/ImFusion/Ext/Eigen/src/plugins;"
    "/usr/include/ImFusion;"
    + os.environ["PATH"]
)


class ndi_to_stl_transform:
    """SVD-based rigid registration from NDI average points to STL landmarks."""

    def rigid_transform_3D(self, A, B):
        """Compute the rigid transform (R, t) such that B ≈ R @ A + t.

        Uses SVD-based least-squares with reflection correction.

        Parameters
        ----------
        A : np.ndarray, shape (3, N)
            Source point set.
        B : np.ndarray, shape (3, N)
            Target point set.

        Returns
        -------
        R : np.ndarray, shape (3, 3)
            Rotation matrix.
        t : np.ndarray, shape (3, 1)
            Translation vector.
        """
        assert A.shape == B.shape

        num_rows, num_cols = A.shape
        if num_rows != 3:
            raise Exception(f"matrix A is not 3xN, it is {num_rows}x{num_cols}")
        num_rows, num_cols = B.shape
        if num_rows != 3:
            raise Exception(f"matrix B is not 3xN, it is {num_rows}x{num_cols}")

        # Compute centroids
        centroid_A = np.mean(A, axis=1).reshape(-1, 1)
        centroid_B = np.mean(B, axis=1).reshape(-1, 1)

        # Subtract centroids
        Am = A - centroid_A
        Bm = B - centroid_B

        # SVD of cross-covariance matrix
        H = Am @ np.transpose(Bm)
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T

        # Correct for reflection
        if np.linalg.det(R) < 0:
            print("det(R) < 0, reflection detected — correcting...")
            Vt[2, :] *= -1
            R = Vt.T @ U.T

        t = -R @ centroid_A + centroid_B
        print(f"Rotation:\n{R}\nTranslation:\n{t}\n")
        return R, t

    def find_corresponding_point_transform(self, p1_path, p2_path):
        """Load two point matrices from files and compute the rigid transform.

        Parameters
        ----------
        p1_path : str
            Path to the averaged NDI points matrix (3xN).
        p2_path : str
            Path to the STL landmark matrix (3xN).

        Returns
        -------
        R : np.ndarray, shape (3, 3)
        t : np.ndarray, shape (3, 1)
        """
        pc_1 = np.asarray(np.loadtxt(p1_path))
        pc_2 = np.asarray(np.loadtxt(p2_path))
        R, t = self.rigid_transform_3D(pc_2, pc_1)
        return R, t

    def print_imfusion_matrix(self, R, t):
        """Print the 4x4 transformation matrix in ImFusion-compatible format.

        Parameters
        ----------
        R : np.ndarray, shape (3, 3)
        t : np.ndarray, shape (3, 1)
        """
        t = t.flatten()
        print_string = "["
        for row in range(3):
            print_string += "["
            for col in range(3):
                print_string += str(R[row, col]) + ", "
            print_string += str(t[row]) + "], "
        print_string += "[0, 0, 0, 1]"
        print(f"ImFusion transformation matrix:\n{print_string}")

    def main(self, imfusion_matrix, stl_matrix):
        """Run rigid registration and print the ImFusion-format matrix.

        Parameters
        ----------
        imfusion_matrix : str
            Path to averaged NDI point matrix file.
        stl_matrix : str
            Path to STL landmark matrix file.

        Returns
        -------
        R : np.ndarray, shape (3, 3)
        t : np.ndarray, shape (3, 1)
        """
        R, t = self.find_corresponding_point_transform(imfusion_matrix, stl_matrix)
        self.print_imfusion_matrix(R, t)
        return R, t
