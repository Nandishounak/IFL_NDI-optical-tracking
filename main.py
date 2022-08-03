from avg_pt_calculator import *
from find_stl_to_ndi_transform import *
from Euler_angles import *
import glob

if __name__ == '__main__':
    #initialize imfusion packages
    imfusion.init()


    # returns array of the paths of the imf files
    imf_folder_path= ('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/')
    imf_array = []
    for name in sorted(glob.glob('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/*.imf')):
        imf_array.append(name)
    print(imf_array)

#####['/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l01.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l02.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l04.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l05.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l07.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l08.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l10.imf',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/l11.imf']
######
    #create the empty .txt files for average point values to be stored after running the code
    arr_avg_pts=[]
    for txtfilecount in range(8):

        text = open(r"/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/" + str(txtfilecount+1) + ".txt", 'w')
        text.close()
    avg_pts_folder="/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/"
    for temp in sorted(glob.glob('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/*.txt')):
        arr_avg_pts.append(temp)
    print(arr_avg_pts) #['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt']
#####['/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/0.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/1.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/2.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/3.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/4.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/5.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/6.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/7.txt',
    # '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/8.txt']
#####


    #run the loop for extracting all the average points from imf tracking file
    matrix = []

    for point_counter in range(len(arr_avg_pts)):

        #initialize the average tracking positions class
        x = avg_tracking_positions()

        #load the T_tool_tip transform matrix file
        T= np.loadtxt("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/stylustransform.txt").reshape(4,1)

        #load the paths to the imf file generated from imfusion, the new file location where the average point matrix will be stored.
        print('this is counter', point_counter)
        temp_mat=x.main(imf_array[point_counter],
               arr_avg_pts[point_counter], T)
        matrix.append(temp_mat)

        print('this is counter', point_counter)

    print('matrix in main',matrix)
    #extract the matrix in correct form and export it
    tempmat1= np.reshape(matrix, (4,8))
    tempmat1= np.delete(tempmat1, 3, 1)
    tempmat1= np.delete(tempmat1, 6, 1)
    tempmat1= np.reshape(tempmat1, (8,3))
    mat=tempmat1.T
    print('matrix after slicing', mat, 'matrix shape', np.shape(mat))
    text = open(r"/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/" + "avg_pt_matrix_3x8.txt", 'w')
    np.savetxt(text, mat)
    text.close()

    #now we compute the rigid transformation matrix
    #Stl_landmark_matrix_3x8



    #compute the rigid registration
    rt = ndi_to_stl_transform()
    rot_mat, translation_mat = rt.main("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/avg_pt_matrix_3x8.txt", "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/Stl_landmark_matrix_3x8.txt")
    print('ndi to stl transform matrix',np.shape(rot_mat), np.shape(translation_mat))

    #compute the Euler angles
    angles = Euler_angles()
    theta_x, theta_y, theta_z = angles.Euler(rot_mat)
    print("angles in degrees- x, y, z ==>", theta_x, theta_y, theta_z)






