import glob
from avg_pt_calculator import *

def avg_pts_matrix(imf_folder_path, avg_pts_folder, stylus_transform, transforms_folder):
    # imf_folder_path = ('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/*.imf')
    # note for users: change the path according to the imf path
    imf_arr = []
    for name in sorted(glob.glob(imf_folder_path)):
        imf_arr.append(name)
    print(imf_arr, "Imf arr works")


    # avg_pts_folder='/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/'
    arr_avg_pts=[]
    for txtfilecount in range(8):

        text = open(avg_pts_folder + str(txtfilecount+1) + ".txt", 'w')
        text.close()
    # avg_pts_folder="/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/"
    for temp in sorted(glob.glob(avg_pts_folder + '/*.txt')):
        arr_avg_pts.append(temp)
    print(arr_avg_pts, "arr_avg_pts is working")


    # run the loop for extracting all the average points from imf tracking file
    matrix = []
    x = avg_tracking_positions()
    print(type(imf_arr), 'this is before counter')

    for point_counter in range(len(arr_avg_pts)):

        # load the T_tool_tip transform matrix file
        T_tool_tip = np.loadtxt(stylus_transform).reshape(4, 1)

        # load the paths to the imf file generated from imfusion, the new file location where the average point matrix will be stored.
        print('this is counter', point_counter)

        # initialize the average tracking positions class

        temp_mat = x.main(imf_arr[point_counter],
                          arr_avg_pts[point_counter], T_tool_tip)
        matrix.append(temp_mat)

        print('this is end of counter', point_counter)

    # print('matrix in main', matrix)
    # extract the matrix in correct form and export it
    tempmat1 = np.reshape(matrix, (4, 8))
    tempmat1 = np.delete(tempmat1, 3, 1)
    tempmat1 = np.delete(tempmat1, 6, 1)
    tempmat1 = np.reshape(tempmat1, (8, 3))
    mat = tempmat1.T
    # print('matrix after slicing', mat, 'matrix shape', np.shape(mat))
    text = open(transforms_folder + "avg_pt_matrix_3x8.txt",
                'w')
    np.savetxt(text, mat)
    text.close()

    return arr_avg_pts
