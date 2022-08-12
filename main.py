import numpy as np

from find_stl_to_ndi_transform import *
from Euler_angles import *
from glob_finder import *
from mse_error import *

if __name__ == '__main__':
    #initialize imfusion packages
    imfusion.init()

    imf_folder = "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder_0508/" #path where imf files are stored
    avg_pts_folder = '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/' #path where the average points from different landmarks (imf --> avg pts) will be stored as separate files

    stylus_transform = "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/stylustransform.txt" #load the path of the stylus transform (T_tool_tip)
    # x.stylus_transform(np.array([[-18.6831], [0.0823379], [-157.464], [1]])) --> store the txt file of the pointer sych that it reads as a matrix 4x1
    transforms_folder_path= "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/" #enter the path where the transform matrix will be stored after extraction
    avg_pts_matrix(imf_folder+'/*.imf', avg_pts_folder
                   ,stylus_transform, transforms_folder_path) #calling the avg_pts_matrix function to return the matrix containing the average points




    #now we compute the rigid transformation matrix
    #we have the Stl_landmark_matrix_3x8 stored as a .txt file
    stl_landmark_matrix = np.loadtxt("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/Stl_landmark_matrix_3x8.txt")
    print("stl matrix", stl_landmark_matrix, '\n', np.shape(stl_landmark_matrix))


    #compute the rigid registration
    rt = ndi_to_stl_transform()

    rot_mat, translation_mat = rt.main("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/avg_pt_matrix_3x8.txt",
                                       "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/Stl_landmark_matrix_3x8.txt")
    # print('ndi to stl transform matrix',np.shape(rot_mat), np.shape(translation_mat))

    #compute the Euler angles
    angles = Euler_angles()
    theta_x, theta_y, theta_z = angles.Euler(rot_mat)
    print("angles in radians- x, y, z ==>", theta_x, theta_y, theta_z)

    #compute error
    Err = mse_error() #calling the error function
    Err.error(rot_mat, translation_mat, stl_landmark_matrix, avg_pt_matrix=np.loadtxt("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/avg_pt_matrix_3x8.txt"))








