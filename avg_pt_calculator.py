# import os
#
# # print(os.environ['PATH'])
#
# os.environ['PATH'] = 'C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite\\plugins;' + os.environ['PATH']
# # imfusion_suite = __import__("E:\\ImFusion\\ImFusion Suite\\Suite\\imfusion")
# print(os.environ['PATH'])
# import sys
# sys.path.append('C:\\Program Files\\ImFusion\\ImFusion_Suite\\Suite;')
# # print(sys.path)

# import imfusion


# os.environ['PATH'] = '/usr/include/ImFusion/Ext/Eigen/src/plugins;/usr/include/ImFusion;' + os.environ['PATH']

# PYTHONUNBUFFERED = 1;
# PYTHONPATH=%PYTHONPATH%;'E:\ImFusion\ImFusion Suite\Suite';
#########################################################

#########################################################
import os
os.environ['PATH'] = 'C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite\\plugins;' + os.environ['PATH']
os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ';C:\\Program Files\\ImFusion\\ImFusion Suite\\Suite;'+'E:\\IFL\\Imfusionenv\\venv\\Lib\\site-packages\\imfusion\\imfusion'
# print(os.environ['PATH'])

import sys
sys.path.append("E:\\IFL\\Imfusionenv\\venv\\Lib\\site-packages\\imfusion\\imfusion")
print (sys.path)
import numpy as np
import time
import imfusion
class avg_tracking_positions:
    def __call__(self, *args, **kwargs):
        return None;
    def stylus_transform(self, T_tool_tip):
        return T_tool_tip
    def get_tracking_positions(self, tracking_stream, stylus_transform):
        points = []
        T = self.stylus_transform(T_tool_tip=True)
        for i in range(tracking_stream.size()):
            calibrated_with_tool_tip = tracking_stream.matrix(i) @ T
            print('calibrated_with_tool_tip', calibrated_with_tool_tip)
            points.append(calibrated_with_tool_tip)
        return np.stack(points, axis=0)

    def average_points_positions(self, imfusion_file_path):
        imfusion_tracking_streams = imfusion.open(imfusion_file_path)
        point_list = []
        for tracking_stream in imfusion_tracking_streams:
            tracking_point = self.get_tracking_positions(tracking_stream, stylus_transform=None)
            print('tracking point', tracking_point)
            point_list.append(np.mean(tracking_point, axis=0))
        print('point list from get tracking positions after mean', point_list)
        return point_list

    def save_point_cloud(self, pc, filepath):
        if isinstance(pc, list):
            pc = np.stack(np.squeeze(pc, axis=0),axis=0)
        print('filepath saving the avg pose', filepath)
        print('pc', pc, pc.shape)
        np.savetxt(filepath, pc[0:3,:])

    def main(self, calibrated_phantom_point_path, averaged_points_path):

        # Extracting the phantom landmark positions
        phantom_landmarks = self.average_points_positions(calibrated_phantom_point_path)
        print('phantom landmarks', phantom_landmarks)
        self.save_point_cloud(phantom_landmarks, averaged_points_path)

if __name__ == '__main__':
    imfusion.init()


    x = avg_tracking_positions()
    x.main("E:\IFL\data_0206\l1.imf", "E:\IFL\data_0206\_avgpts1_new.txt")
    x.stylus_transform(np.array([[-18.6831], [0.0823379], [-157.464], [1]]))
