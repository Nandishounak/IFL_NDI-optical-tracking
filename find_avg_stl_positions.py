import os
import numpy as np
import avg_pt_calculator
import imfusion

os.environ['PATH'] = '/usr/include/ImFusion/Ext/Eigen/src/plugins;/usr/include/ImFusion;' + os.environ['PATH']

# PYTHONUNBUFFERED = 1;PYTHONPATH=C:\Program Files\ImFusion\ImFusion Suite\Suite\;


class ndi_transform:
    def __call__(self, *args, **kwargs):
        return None;

    def rigid_transform_3D(self, A, B):   #computes the rigid transformation between two points, avg coordinate and stl coordinate
        assert A.shape == B.shape
        # print('A.shape, B.shape', A.shape, B.shape)
        # print(('A',A, 'B',B))

        num_rows, num_cols = A.shape
        if num_rows != 3:
            raise Exception(f"matrix A is not 3xN, it is {num_rows}x{num_cols}")

        num_rows, num_cols = B.shape
        if num_rows != 3:
            raise Exception(f"matrix B is not 3xN, it is {num_rows}x{num_cols}")

        # find mean column wise
        centroid_A = np.mean(A, axis=1)
        print('cenA \n', centroid_A, '\n')
        centroid_B = np.mean(B, axis=1)
        print('cenB \n', centroid_B, '\n')

        # ensure centroids are 3x1
        centroid_A = centroid_A.reshape(-1, 1)
        centroid_B = centroid_B.reshape(-1, 1)
        # print('centroid A after reshape \n',centroid_A, '\n', 'centroid B afetr reshape \n', centroid_B,'\n' )

        # subtract mean
        Am = A - centroid_A
        Bm = B - centroid_B
        # print('Am ->', Am,'\n', 'Bm->', Bm, '\n')
        H = Am @ np.transpose(Bm)
        # print('H',H)
        # H = A @ np.transpose(B)
        # print('H', H)


        # sanity check
        #if linalg.matrix_rank(H) < 3:
        #    raise ValueError("rank of H = {}, expecting 3".format(linalg.matrix_rank(H)))

        # find rotation
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T
        # print('U',U, '\n', 'S', S, '\n', 'Vt', Vt)

        # special reflection case
        if np.linalg.det(R) < 0:
            print("det(R) < R, reflection detected!, correcting for it ...")
            Vt[2, :] *= -1
            R = Vt.T @ U.T

        t = -R @ centroid_A + centroid_B
        # print('R, t', '\n', R, '\n', t, '\n')
        return R, t


    def get_tracking_positions(self, tracking_stream):
        print('tracking stream', tracking_stream)
        points = []
        # poses = []
        T_tool_tip =np.array([[-18.6831],[0.0823379],[-157.464],[1]])
        for i in range(tracking_stream.size()):
            # print('tracking stream matrix', tracking_stream.matrix(i)[:])
            # point = np.squeeze(tracking_stream.matrix(i)[0:3, -1])
            # print('point', point)
            calibrated_with_tool_tip = tracking_stream.matrix(i)@T_tool_tip
            print('calibrated_with_tool_tip', calibrated_with_tool_tip)
            # pose = np.squeeze(calibrated_with_tool_tip)
            points.append(calibrated_with_tool_tip)
            # poses.append(pose)
            # print('pose', pose, pose.shape)

            # print('tracking stream matrix', tracking_stream.matrix(i)[0:3, -1])

        # print('get tracking positions from tracking stream', np.stack(poses, axis=0))
        return np.stack(points, axis=0)
        # return np.stack(poses, axis=0)



    def average_points_positions(imfusion_file_path):
        imfusion_tracking_streams = imfusion.open(imfusion_file_path)
        # print('imfusion tracking streams', imfusion_tracking_streams)
        point_list = []
        # pose_list = []
        for tracking_stream in imfusion_tracking_streams:
            tracking_point = self.get_tracking_positions(tracking_stream)
            # tracking_pose = get_tracking_positions(tracking_stream)

            print('tracking point', tracking_point)
            # print('tracking poses', tracking_pose)
            point_list.append(np.mean(tracking_point, axis=0))
            # pose_list.append(tracking_pose.mean(axis=0, dtype=float))
        # np.squeeze(pose_list, axis=0)
        print('point list from get tracking positions after mean', point_list)
        # print('pose list from get tracking positions after mean', pose_list)
        return point_list
        # # extract last column for average point calculation
        # avg_point = np.squeeze(np.asarray(pose_list))
        # point_list.append(avg_point[:,3])
        # print('avgpt', avg_point[:,3])
        # return pose_list, avg_point[:,3]



    def save_point_cloud(pc, filepath):
        if isinstance(pc, list):
            pc = np.stack(np.squeeze(pc, axis=0),axis=0)
        # if isinstance(avgpt, list):
        #     avgpt = np.stack(avgpt, axis=0)
        print('filepath saving the avg pose', filepath)
        print('pc', pc, pc.shape)
        np.savetxt(filepath, pc[0:3,:])



    #for average point calculation
    def find_corresponding_point_transform(p1_path, p2_path):
        pc_1 = np.asarray(np.loadtxt(p1_path)).reshape(3,-1)
        # pc_1 = np.asarray(np.loadtxt(p1_path))
        pc_2 = np.asarray(np.loadtxt(p2_path)).reshape(3, -1)
        # pc_2 = np.asarray(np.loadtxt(p2_path))
        print('pc1', pc_1 , 'pc1.shape',pc_1.shape, 'pc_2',pc_2, 'pc2.shape',pc_2.shape)
        # R, t = rigid_transform_3D(np.transpose(pc_2), np.transpose(pc_1))
        R, t = self.rigid_transform_3D(pc_2, pc_1)
        return R, t

    def print_imfusion_matrix(R, t):
        print('t before flatten', t)
        t = t.flatten()
        print('t after flatten', t)
        print_string = "["

        for row in range(3):
            print_string += "["
            for col in range(3):
                print_string += str(R[row, col]) + ", "

            print_string += str(t[row]) + "], "

        print_string += "[0, 0, 0, 1]"

        print('print string', print_string)


    # def main(calibrated_phantom_point_path, averaged_points_path, tracking_points):
    def main(calibrated_phantom_point_path, averaged_points_path ):

        # Extracting the phantom landmark positions
        phantom_landmarks = average_points_positions(calibrated_phantom_point_path)
        print('phantom landmarks', phantom_landmarks)
        # save_point_cloud(phantom_landmarks, averaged_points_path)
        save_point_cloud(phantom_landmarks, averaged_points_path)

        # Compute the transformation from the phantom .stl model and the acquired landmarks - this is only a sanity
        # check for visualization, it is not needed for the calibration
        # R, t = find_corresponding_point_transform(averaged_points_path, stl_points_path)
        # print_imfusion_matrix(R, t)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    imfusion.init()

    calibrated_phantom_point_path1 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l1.imf"
    averaged_points_path1 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts1.txt"
    #
    # calibrated_phantom_point_path2 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l2.imf"
    # averaged_points_path2 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts2.txt"
    # averaged_pose_path2 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_3105/avg-pose2.txt"

    # calibrated_phantom_point_path4 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l4.imf"
    # averaged_points_path4 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts4.txt"
    # # averaged_pose_path4 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_3105/avg-pose4.txt"
    #
    # tracking_points_path5 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_3105/tracking-pts5.txt"
    # calibrated_phantom_point_path5 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l5.imf"
    # averaged_points_path5 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts5.txt"
    #
    # calibrated_phantom_point_path7 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l7.imf"
    # averaged_points_path7 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts7.txt"
    # averaged_pose_path7 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_3105/avg-pose7.txt"


    # calibrated_phantom_point_path8 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l8.imf"
    # averaged_points_path8 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts8.txt"

    # calibrated_phantom_point_path10 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l10.imf"
    # averaged_points_path10 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts10.txt"

    # calibrated_phantom_point_path11 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l11.imf"
    # averaged_points_path11 = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts11.txt"

    # stl_points_path = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_2605/StlPoint_l10.txt"
    #
    main(calibrated_phantom_point_path1, averaged_points_path1)
    # main(calibrated_phantom_point_path2, averaged_points_path2)
    # main(calibrated_phantom_point_path4, averaged_points_path4)
    # main(calibrated_phantom_point_path5, averaged_points_path5)
    # main(calibrated_phantom_point_path7, averaged_points_path7)
    # main(calibrated_phantom_point_path8, averaged_points_path8)
    # main(calibrated_phantom_point_path10, averaged_points_path10)
    # main(calibrated_phantom_point_path11, averaged_points_path11)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
