from avg_pt_calculator import *
from pathlib import Path
if __name__ == '__main__':
    #initialize imfusion packages
    imfusion.init()


    # This is the path where all the files are stored.
    imf_folder_path = "/home/nandishounak/Documents/IFL/ImFusionMhaExporter/imf_folder/"

    emptylist = []
    paths = Path(imf_folder_path)
    print('pathsorted', type(paths), paths)
    for root, dirs, files in os.walk(paths):
        # for file in files:
            emptylist.append(dirs)
            print('trying to print something')
    print('finally i am here', (emptylist))
    #store the filepaths in an array
    arr_imf = []
    for data_file in sorted(os.listdir(imf_folder_path)):
        # print(("this is before printing datafile"))
        arr_imf.append(data_file)
        # print(("this is after printing datafile"))
    print(arr_imf) #['l01.imf', 'l02.imf', 'l04.imf', 'l05.imf', 'l07.imf', 'l08.imf', 'l10.imf', 'l11.imf']

    #create the empty .txt files for avergae point values to be stored after running the code
    arr_avg_pts=[]
    for x in range(9):
        text = open(r"/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/" + str(x) + ".txt", 'w')
        text.close()
    avg_pts_folder="/home/nandishounak/Documents/IFL/ImFusionMhaExporter/avg_pts_folder/"
    for temp in sorted(os.listdir(avg_pts_folder)):
        arr_avg_pts.append(temp)
    print(arr_avg_pts) #['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt']

    #run the loop for computing all the points
    for point_counter in range(len(arr_imf)):

        #initialize the average tracking positions class
        x = avg_tracking_positions()

        #load the T_tool_tip transform matrix file
        # x.main("E:\IFL\data_0206\l1.imf", "E:\IFL\data_0206\_avgpts1_new.txt")
        T= np.loadtxt("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/stylustransform.txt").reshape(4,1)
        #load the paths to the imf file generated from imfusion, the new file location where the average point matrix will be stored.
        # x.main("/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l1.imf", "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts-1-test.txt", T)
        x.main(arr_imf[point_counter],
               arr_avg_pts[point_counter], T)



# folder = '/mnt/HDD1/shounak/test2'



# # sorted_sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
# print(sorted_sub_folders)
# print(type(sub_folders))




