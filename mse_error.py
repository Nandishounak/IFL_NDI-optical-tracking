import numpy as np
class mse_error:
    def error(self, rotation_matrix, translat_matrix, stl_landmarks, avg_pt_matrix):
        computed_stl_landmarks = []
        mse=[]
        pointlist=["pt1", "pt2", "pt4", "pt5", "pt7", "pt8", "pt10", "pt11"]
        #apply some restructuring for calculations
        last_col = np.ones(8).reshape((1,8))
        last_col2 = [[0,0,0,1]]
        stl_landmarks=np.concatenate((stl_landmarks, last_col), axis=0)
        avg_pt_matrix=np.concatenate((avg_pt_matrix, last_col), axis=0)
        print(stl_landmarks)
        # print("shape of rot and transl matrix=", np.shape(rotation_matrix), np.shape(translat_matrix))

        trf_matrix = np.concatenate((rotation_matrix, translat_matrix), axis=1)
        trf_matrix = np.concatenate((trf_matrix, last_col2), axis=0)
        # print("am I working>>",stl_landmarks, trf_matrix, avg_pt_matrix)
        assert np.shape(stl_landmarks)==(4,8)
        assert np.shape(trf_matrix) == (4,4)
        for i in range(8):
            counter_array = avg_pt_matrix[:,i].reshape(4,1)
            # print("shape of counter array",counter_array, np.shape(counter_array))
            computed_stl_landmarks=np.linalg.pinv(trf_matrix)@counter_array
            print("computed_stl_landmarks",pointlist[i], "-->", "\n", computed_stl_landmarks, "\n", "real_stl_landmarks",  pointlist[i], "-->", "\n", stl_landmarks[:,i].reshape(4,1))
            # print("shape of both", np.shape(computed_stl_landmarks), np.shape(stl_landmarks[:,i].reshape(4,1)))
            assert np.shape(computed_stl_landmarks) == np.shape(stl_landmarks[:,i].reshape(4,1))
            # print("real value of Stl landmark=", stl_landmarks[:,i], '\n', "computed value of Stl landmark=", computed_stl_landmarks[:,i])

            mse= np.sqrt((stl_landmarks[0,i] - computed_stl_landmarks[0])**2+(stl_landmarks[1,i] - computed_stl_landmarks[1])**2+(stl_landmarks[2,i] - computed_stl_landmarks[2])**2+(stl_landmarks[3,i] - computed_stl_landmarks[3])**2)
            print("error=", mse)

        return None