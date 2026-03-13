"""Compute registration error between computed and ground-truth STL landmarks."""

import numpy as np


class mse_error:
    """Evaluate the point-wise Euclidean error after rigid registration."""

    LANDMARK_LABELS = ["pt1", "pt2", "pt4", "pt5", "pt7", "pt8", "pt10", "pt11"]

    def error(self, rotation_matrix, translat_matrix, stl_landmarks, avg_pt_matrix):
        """Print per-landmark Euclidean distance error.

        Parameters
        ----------
        rotation_matrix : np.ndarray, shape (3, 3)
            Rotation from rigid registration.
        translat_matrix : np.ndarray, shape (3, 1)
            Translation from rigid registration.
        stl_landmarks : np.ndarray, shape (3, 8)
            Ground-truth STL phantom landmark positions.
        avg_pt_matrix : np.ndarray, shape (3, 8)
            Averaged NDI tracking positions.
        """
        # Build 4x4 transformation matrix
        last_col = np.ones(8).reshape((1, 8))
        stl_h = np.concatenate((stl_landmarks, last_col), axis=0)
        avg_h = np.concatenate((avg_pt_matrix, last_col), axis=0)

        trf_matrix = np.concatenate((rotation_matrix, translat_matrix), axis=1)
        trf_matrix = np.concatenate((trf_matrix, [[0, 0, 0, 1]]), axis=0)

        assert stl_h.shape == (4, 8)
        assert trf_matrix.shape == (4, 4)

        errors = []
        for i in range(8):
            target = avg_h[:, i].reshape(4, 1)
            computed = np.linalg.pinv(trf_matrix) @ target
            real = stl_h[:, i].reshape(4, 1)

            dist = np.sqrt(np.sum((real[:3] - computed[:3]) ** 2))
            errors.append(dist)
            print(f"{self.LANDMARK_LABELS[i]}: error = {dist:.4f} mm")

        mean_error = np.mean(errors)
        print(f"\nMean error: {mean_error:.4f} mm")
