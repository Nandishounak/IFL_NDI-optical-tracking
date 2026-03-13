"""Compute averaged tracking positions from ImFusion .imf files."""

import os
os.environ["PATH"] = (
    "/usr/include/ImFusion/ext/Eigen/src/plugins;"
    "/usr/include/ImFusion;"
    + os.environ["PATH"]
)

import numpy as np
import imfusion


class avg_tracking_positions:
    """Extract and average NDI tracking positions from ImFusion streams."""

    def get_tracking_positions(self, tracking_stream, T):
        """Compute calibrated tip positions for every frame in a tracking stream.

        Parameters
        ----------
        tracking_stream : imfusion.TrackingStream
            A single tracking stream loaded from an .imf file.
        T : np.ndarray, shape (4, 1)
            Stylus tip-offset transform vector.

        Returns
        -------
        np.ndarray
            Stacked calibrated positions, shape (N, 4, 1).
        """
        points = []
        for i in range(tracking_stream.size()):
            if T.all() != np.eye(4).all():
                calibrated = tracking_stream.matrix(i) @ T
            else:
                calibrated = tracking_stream(i) @ np.eye(4)
            points.append(calibrated)
        return np.stack(points, axis=0)

    def average_points_positions(self, imfusion_file_path, T):
        """Average the tracking positions across all frames per stream.

        Parameters
        ----------
        imfusion_file_path : str
            Path to a single .imf file.
        T : np.ndarray, shape (4, 1)
            Stylus tip-offset transform vector.

        Returns
        -------
        list of np.ndarray
            Mean position for each tracking stream in the file.
        """
        tracking_streams = imfusion.open(imfusion_file_path)
        point_list = []
        for stream in tracking_streams:
            positions = self.get_tracking_positions(stream, T)
            point_list.append(np.mean(positions, axis=0))
        return point_list

    def save_point_cloud(self, pc, filepath):
        """Save averaged point cloud to a text file.

        Parameters
        ----------
        pc : list of np.ndarray
            Point cloud data.
        filepath : str
            Output file path.

        Returns
        -------
        list of np.ndarray
            The saved point matrix.
        """
        if isinstance(pc, list):
            pc = np.stack(np.squeeze(pc, axis=0), axis=0)
        np.savetxt(filepath, pc[0:3, :])
        point_matrix = [pc]
        return point_matrix

    def main(self, calibrated_phantom_point_path, averaged_points_path, T):
        """Run the full averaging pipeline for a single landmark.

        Parameters
        ----------
        calibrated_phantom_point_path : str
            Path to the .imf file for this landmark.
        averaged_points_path : str
            Path where the averaged point file will be saved.
        T : np.ndarray, shape (4, 1)
            Stylus tip-offset transform vector.

        Returns
        -------
        list of np.ndarray
            The saved point matrix.
        """
        phantom_landmarks = self.average_points_positions(calibrated_phantom_point_path, T)
        pt_mat = self.save_point_cloud(phantom_landmarks, averaged_points_path)
        return pt_mat
