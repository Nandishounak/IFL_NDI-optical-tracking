import os
os.environ['PATH'] = '/usr/include/ImFusion/Ext/Eigen/src/plugins;/usr/include/ImFusion;' + os.environ['PATH']

import numpy as np
import imfusion
#
# # print(os.environ['PATH'])
#
# os.environ['PATH'] = 'C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite\\plugins;' + os.environ['PATH']
# # imfusion_suite = __import__("E:\\ImFusion\\ImFusion Suite\\Suite\\imfusion")
# print(os.environ['PATH'])
# import sys
# sys.path.append('C:\\Program Files\\ImFusion\\ImFusion_Suite\\Suite;')
# # print(sys.path)



# PYTHONUNBUFFERED = 1;
# PYTHONPATH=%PYTHONPATH%;'E:\ImFusion\ImFusion Suite\Suite';
#########################################################

#########################################################
# import os
# os.environ['PATH'] = 'C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite\\plugins;' + os.environ['PATH']
# os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ';C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;'+'E:\\IFL\\Imfusionenv\\venv\\Lib\\site-packages\\imfusion\\imfusion'
# # print(os.environ['PATH'])
#
# import sys
# sys.path.append("E:\\IFL\\Imfusionenv\\venv\\Lib\\site-packages\\imfusion\\imfusion")
# print (sys.path)
class avg_tracking_positions:
    def __call__(self, *args, **kwargs):
        return None;
    # def stylus_transform(self, T_tool_tip):
    #     return T_tool_tip
    def get_tracking_positions(self, tracking_stream, T):
        points = []
        # T = stylus_transform(self)
        # print ("this is T",T.shape)
        for i in range(tracking_stream.size()):
            calibrated_with_tool_tip = tracking_stream.matrix(i) @ T
            # print('calibrated_with_tool_tip', calibrated_with_tool_tip)
            points.append(calibrated_with_tool_tip)
        return np.stack(points, axis=0)

    def average_points_positions(self, imfusion_file_path,T):
        imfusion_tracking_streams = imfusion.open(imfusion_file_path)
        point_list = []
        for tracking_stream in imfusion_tracking_streams:
            tracking_point = self.get_tracking_positions(tracking_stream, T)
            # print('tracking point', tracking_point)
            point_list.append(np.mean(tracking_point, axis=0))
        print('point list from get tracking positions after mean', '\n', point_list)
        return point_list

    def save_point_cloud(self, pc, filepath):
        if isinstance(pc, list):
            pc = np.stack(np.squeeze(pc, axis=0),axis=0)
        print('filepath saving the avg points', filepath)
        print('pc', pc, pc.shape)
        np.savetxt(filepath, pc[0:3,:])
        point_matrix=[]
        point_matrix.append(pc)
        print('point matrix',point_matrix)
        return point_matrix



    def main(self, calibrated_phantom_point_path, averaged_points_path, T):

        # Extracting the phantom landmark positions
        phantom_landmarks = self.average_points_positions(calibrated_phantom_point_path,T)
        print('phantom landmarks-->', '\n', phantom_landmarks)
        pt_mat=self.save_point_cloud(phantom_landmarks, averaged_points_path)
        return pt_mat



if __name__ == '__main__':
    imfusion.init()


    x = avg_tracking_positions()
    # x.main("E:\IFL\data_0206\l1.imf", "E:\IFL\data_0206\_avgpts1_new.txt")
    T= np.loadtxt("/home/nandishounak/Documents/IFL/ImFusionMhaExporter/stylustransform.txt").reshape(4,1)
    # x.stylus_transform(np.array([[-18.6831], [0.0823379], [-157.464], [1]]))
    # x.get_tracking_positions(stytra)
    # print(stytra.shape)
    imfpath= "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l1.imf"
    x.main("/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/l1.imf", "/home/nandishounak/Documents/IFL/ImFusion_data/data_1905/Patient-01/data_0206/avg-pts-1-test.txt", T)