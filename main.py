from avg_pt_calculator import *
from find_stl_to_ndi_transform import *
from Euler_angles import *
from glob_finder import *

if __name__ == '__main__':
    #initialize imfusion packages
    imfusion.init()


    # returns array of the paths of the imf files
    # imf_folder_path= ('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/')
    # imf_array = []
    # for name in sorted(glob.glob('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/*.imf')):
    #     imf_array.append(name)
    # print(imf_array)

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
    # arr_avg_pts=[]
    # for txtfilecount in range(8):
    #
    #     text = open(r"/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/" + str(txtfilecount+1) + ".txt", 'w')
    #     text.close()
    # avg_pts_folder="/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/"
    # for temp in sorted(glob.glob('/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/*.txt')):
    #     arr_avg_pts.append(temp)
    # print(arr_avg_pts)
    #
    #['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt']
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
    imf_folder = "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder_0508/" #path where imf files are stored
    avg_pts_folder = '/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/' #path where the average points from different landmarks will be stored as separate files

    stylus_transform = "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/stylustransform.txt" #load the path of the stylus transform
    transforms_folder_path= "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/" #enter the path where the transform matrix will be stored after extraction
    avg_pts_matrix(imf_folder+'/*.imf', avg_pts_folder
                   ,stylus_transform, transforms_folder_path) #calling the imf_array function to return the imf files in an array for the next extraction step
 #calling the avg_pts_array to return the list of average points paths in an array, and the matrix containing the average points




    #now we compute the rigid transformation matrix
    #Stl_landmark_matrix_3x8



    #compute the rigid registration
    rt = ndi_to_stl_transform()

    rot_mat, translation_mat = rt.main("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/avg_pt_matrix_3x8.txt",
                                       "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/transforms_folder/Stl_landmark_matrix_3x8.txt")
    # print('ndi to stl transform matrix',np.shape(rot_mat), np.shape(translation_mat))

    #compute the Euler angles
    angles = Euler_angles()
    theta_x, theta_y, theta_z = angles.Euler(rot_mat)
    print("angles in radians- x, y, z ==>", theta_x, theta_y, theta_z)


    #sanity check
    #mse error
    # landmark2 = open("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/2.txt", 'r')
    # print("lm2",landmark2)
#     mse4 = stl2 = np.linalg.pinv(rot_mat)@
# print ('stl2', stl2)






