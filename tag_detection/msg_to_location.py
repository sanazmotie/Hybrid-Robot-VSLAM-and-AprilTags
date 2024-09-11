import os
import time
import shutil
import msgpack
import numpy as np
from scipy.spatial.transform import Rotation as R


#def get_camera_location(msgPath = "C:\Users\Sanaz\Documents\GitHub\VSLAM\SLAM\build\map.msg"):
def get_camera_location(msgPath = "/home/nargess/Documents/GitHub/VSLAM/SLAM/build/map.msg"):
    try:
        with open(msgPath, 'rb') as f:
            data = f.read()
            msg = msgpack.unpackb(data)
            
    except ValueError:
        print("Incomplete data, retrying...")
        return False


    raw_keyfrms = msg["keyframes"]
    keyframe_list = list(raw_keyfrms.values())

    # Sort the list by the 'ts' key (time_stamp)
    keyfrms = sorted(keyframe_list, key=lambda kf: kf['ts'])

    keyfrm_points = []

    # for keyfrm in keyfrms:

    #     # get conversion from camera to world
    #     trans_cw = np.matrix(keyfrm["trans_cw"]).T
    #     rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()

    #     # compute conversion from world to camera
    #     rot_wc = rot_cw.T
    #     trans_wc = - rot_wc * trans_cw
    #     keyfrm_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))
    #     keyfrms_tum.append((keyfrm["ts"], trans_wc.tolist(), R.from_matrix(rot_wc).as_quat().tolist()))

    #     rots.append(rot_wc)
    #     transes.append(trans_wc)
        

    # keyfrm_points = np.array(keyfrm_points)


    keyfrm = keyfrms[-1]

    # get conversion from camera to world
    trans_cw = np.matrix(keyfrm["trans_cw"]).T
    rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()

    # compute conversion from world to camera
    rot_wc = rot_cw.T
    trans_wc = - rot_wc * trans_cw
    keyfrm_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))
    keyfrm_points = np.array(keyfrm_points)

    Y = keyfrm_points[:, 0]
    X = keyfrm_points[:, 2]
    Z = keyfrm_points[:, 1]

    coordinates = np.array([int(X[-1]*100), int(Y[-1]*100)]).reshape((2, 1))
    r = np.array([rot_cw[0][0], rot_cw[0][2], rot_cw[2][0], rot_cw[2][2]]).reshape(2,2)

    f.close()

    return coordinates, r





def robot_path_locations(msgPath = "/home/nargess/Documents/GitHub/VSLAM/SLAM/build/map.msg"):
    try:
        with open(msgPath, 'rb') as f:
            data = f.read()
            msg = msgpack.unpackb(data)
            
    except ValueError:
        print("Incomplete data, retrying...")
        return False


    raw_keyfrms = msg["keyframes"]
    keyframe_list = list(raw_keyfrms.values())

    # Sort the list by the 'ts' key (time_stamp)
    keyfrms = sorted(keyframe_list, key=lambda kf: kf['ts'])

    keyfrm_points = []

    for keyfrm in keyfrms:
        # get conversion from camera to world
        trans_cw = np.matrix(keyfrm["trans_cw"]).T
        rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()

        # compute conversion from world to camera
        rot_wc = rot_cw.T
        trans_wc = - rot_wc * trans_cw
        keyfrm_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))
        

    keyfrm_points = np.array(keyfrm_points)

    Y = keyfrm_points[:, 0]
    X = keyfrm_points[:, 2]
    Z = keyfrm_points[:, 1]


    X = [x * 100 for x in X]
    Y = [y * 100 for y in Y]


    f.close()
    return X, Y



if __name__ == "__main__":
    while True:
        res = get_camera_location()
        if res:
            print(res[0], "************", sep = '\n')