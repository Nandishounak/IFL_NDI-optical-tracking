"""
Main script for NDI Polaris Vicra to ImFusion Suite calibration.

Computes the transformation matrix from NDI optical tracking coordinates
to ImFusion Suite coordinates using 8 wire-phantom landmark points.
"""

import argparse
import numpy as np

from find_stl_to_ndi_transform import ndi_to_stl_transform
from Euler_angles import Euler_angles
from glob_finder import avg_pts_matrix
from mse_error import mse_error


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute NDI-to-ImFusion transformation matrix."
    )
    parser.add_argument(
        "--imf-folder",
        required=True,
        help="Path to folder containing .imf tracking files.",
    )
    parser.add_argument(
        "--avg-pts-folder",
        required=True,
        help="Path to folder where averaged landmark points will be stored.",
    )
    parser.add_argument(
        "--stylus-transform",
        required=True,
        help="Path to the stylus tip-offset transform .txt file.",
    )
    parser.add_argument(
        "--transforms-folder",
        required=True,
        help="Path to folder where the output transform matrix will be stored.",
    )
    parser.add_argument(
        "--stl-matrix",
        default=None,
        help="Path to STL landmark matrix .txt file (for rigid registration and error evaluation).",
    )
    return parser.parse_args()


def main():
    import imfusion
    imfusion.init()

    args = parse_args()

    # Step 1: Compute average tracking positions at each landmark
    imf_glob = args.imf_folder.rstrip("/") + "/*.imf"
    avg_pts_matrix(imf_glob, args.avg_pts_folder, args.stylus_transform, args.transforms_folder)

    # Step 2 (optional): Compute rigid registration and evaluate error
    if args.stl_matrix:
        avg_pt_path = args.transforms_folder.rstrip("/") + "/avg_pt_matrix_3x8.txt"
        stl_landmark_matrix = np.loadtxt(args.stl_matrix)

        rt = ndi_to_stl_transform()
        rot_mat, translation_mat = rt.main(avg_pt_path, args.stl_matrix)

        angles = Euler_angles()
        theta_x, theta_y, theta_z = angles.Euler(rot_mat)
        print(f"Euler angles (rad): x={theta_x:.4f}, y={theta_y:.4f}, z={theta_z:.4f}")

        err = mse_error()
        err.error(rot_mat, translation_mat, stl_landmark_matrix, np.loadtxt(avg_pt_path))


if __name__ == "__main__":
    main()
