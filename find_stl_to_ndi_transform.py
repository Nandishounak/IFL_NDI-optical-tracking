import os
import numpy as np
import time
import imfusion
os.environ['PATH'] = '/usr/include/ImFusion/Ext/Eigen/src/plugins;/usr/include/ImFusion;' + os.environ['PATH']

# PYTHONUNBUFFERED = 1;PYTHONPATH=C:\Program Files\ImFusion\ImFusion Suite\Suite\;


class ndi_to_stl_transform:
    def __call__(self, *args, **kwargs):
        return None;

    def rigid_transform_3D(self, A, B):
        assert A.shape == B.shape
        print('A.shape, B.shape', A.shape, B.shape)
        print(('A',A, 'B',B))

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
        print('centroid A after reshape \n',centroid_A, '\n', 'centroid B afetr reshape \n', centroid_B,'\n' )

        # subtract mean
        Am = A - centroid_A
        Bm = B - centroid_B
        print('Am ->', Am,'\n', 'Bm->', Bm, '\n')
        H = Am @ np.transpose(Bm)
        print('H',H)
        # H = A @ np.transpose(B)
        # print('H', H)


        # sanity check
        #if linalg.matrix_rank(H) < 3:
        #    raise ValueError("rank of H = {}, expecting 3".format(linalg.matrix_rank(H)))

        # find rotation
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T
        print('U',U, '\n', 'S', S, '\n', 'Vt', Vt)

        # special reflection case
        if np.linalg.det(R) < 0:
            print("det(R) < R, reflection detected!, correcting for it ...")
            Vt[2, :] *= -1
            R = Vt.T @ U.T

        t = -R @ centroid_A + centroid_B
        print('R, t', '\n', R, '\n', t, '\n')
        return R, t


    def get_tracking_positions(self, tracking_stream):
        print(tracking_stream)
        points = []
        for i in range(tracking_stream.size()):
            point = np.squeeze(tracking_stream.matrix(i)[0:3, -1])
            points.append(point)
        print('get tracking positions from tracking stream', np.stack(points, axis=0))
        return np.stack(points, axis=0)


    def average_points_positions(self, imfusion_file_path):
        imfusion_tracking_streams = imfusion.open(imfusion_file_path)

        point_list = []
        for tracking_stream in imfusion_tracking_streams:
            tracking_point = self.get_tracking_positions(tracking_stream)
            point_list.append(np.mean(tracking_point, axis=0))
        print('point list from get tracking positions after mean', point_list)
        return point_list


    def save_point_cloud(self, pc, filepath):
        if isinstance(pc, list):
            pc = np.stack(pc, axis=0)

        np.savetxt(filepath, pc)
        print('filepath saving the point cloud',filepath)
        print('pc', pc, pc.shape)


    #for corresponding transform
    def find_corresponding_point_transform(self, p1_path, p2_path):
        # pc_1 = np.asarray(np.loadtxt(p1_path)).reshape(3,-1)
        pc_1 = np.asarray(np.loadtxt(p1_path))
        # pc_2 = np.asarray(np.loadtxt(p2_path)).reshape(3, -1)
        pc_2 = np.asarray(np.loadtxt(p2_path))
        print('pc1', pc_1 , 'pc1.shape',pc_1.shape, 'pc_2',pc_2, 'pc2.shape',pc_2.shape)
        # R, t = self.rigid_transform_3D(np.transpose(pc_2), np.transpose(pc_1))
        R, t = self.rigid_transform_3D(pc_2, pc_1)

        return R, t


    def print_imfusion_matrix(self, R, t):
        print("R=", R)
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


    def main(self, imfusion_matrix, stl_matrix):

        # Extracting the phantom landmark positions
        # phantom_landmarks = average_points_positions(calibrated_phantom_point_path)
        # save_point_cloud(phantom_landmarks, averaged_points_path)

        # Compute the transformation from the phantom .stl model and the acquired landmarks - this is only a sanity
        # check for visualization, it is not needed for the calibration
        R, t = self.find_corresponding_point_transform(imfusion_matrix, stl_matrix)
        self.print_imfusion_matrix(R, t)
        return R, t


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    imfusion.init()
    rt= ndi_to_stl_transform()

    imfusion_matrix = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/Imfusion_matrix_8pts_3x8.txt"
    stl_matrix = "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/Stl_landmark_matrix_1245781011_3x8.txt"

    rt.main(imfusion_matrix, stl_matrix)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
