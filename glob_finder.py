"""Batch processing of .imf files to build the averaged point matrix."""

import glob
import numpy as np
from avg_pt_calculator import avg_tracking_positions


def avg_pts_matrix(imf_folder_path, avg_pts_folder, stylus_transform, transforms_folder):
    """Process all .imf files and produce a combined 3xN average-point matrix.

    Parameters
    ----------
    imf_folder_path : str
        Glob pattern for .imf files (e.g. "/path/to/folder/*.imf").
    avg_pts_folder : str
        Directory to store per-landmark averaged point files.
    stylus_transform : str
        Path to the stylus tip-offset transform .txt file.
    transforms_folder : str
        Directory where the combined avg_pt_matrix_3x8.txt will be written.

    Returns
    -------
    list of str
        Paths to the individual averaged-point files.
    """
    # Collect and sort .imf files
    imf_arr = sorted(glob.glob(imf_folder_path))
    print(f"Found {len(imf_arr)} .imf files")

    # Create empty output files for each landmark
    avg_pts_folder = avg_pts_folder.rstrip("/") + "/"
    arr_avg_pts = []
    for i in range(len(imf_arr)):
        filepath = avg_pts_folder + str(i + 1) + ".txt"
        open(filepath, "w").close()

    arr_avg_pts = sorted(glob.glob(avg_pts_folder + "*.txt"))
    print(f"Prepared {len(arr_avg_pts)} output files")

    # Process each landmark
    matrix = []
    tracker = avg_tracking_positions()

    for i in range(len(arr_avg_pts)):
        T_tool_tip = np.loadtxt(stylus_transform).reshape(4, 1)
        temp_mat = tracker.main(imf_arr[i], arr_avg_pts[i], T_tool_tip)
        matrix.append(temp_mat)

    # Reshape and export the combined matrix
    tempmat1 = np.reshape(matrix, (4, 8))
    tempmat1 = np.delete(tempmat1, 3, 1)
    tempmat1 = np.delete(tempmat1, 6, 1)
    tempmat1 = np.reshape(tempmat1, (8, 3))
    mat = tempmat1.T

    output_path = transforms_folder.rstrip("/") + "/avg_pt_matrix_3x8.txt"
    np.savetxt(output_path, mat)
    print(f"Saved combined matrix ({mat.shape}) to {output_path}")

    return arr_avg_pts
