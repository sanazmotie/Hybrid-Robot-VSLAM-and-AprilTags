import os
import time
import shutil
import msgpack
import numpy as np
from scipy.spatial.transform import Rotation as R


#def get_camera_location(msgPath = "C:\Users\Sanaz\Documents\GitHub\VSLAM\SLAM\build\map.msg"):
def get_camera_location(msgPath = "/home/nargess/Documents/GitHub/VSLAM/SLAM/build/map.msg"):

    # dst = os.path.join(os.path.dirname(msgPath), "map_backup.msg")
    # shutil.copy(msgPath, dst)

    try:
        with open(msgPath, 'rb') as f:
            data = f.read()
            msg = msgpack.unpackb(data)
            
    except ValueError:
        print("Incomplete data, retrying...")
        # time.sleep(0.1)
        return False


    raw_keyfrms = msg["keyframes"]
    new_keyfrms = {}
    for k in raw_keyfrms.keys():
        new_keyfrms[int(k)] = raw_keyfrms[k]




    keyframe_list = list(raw_keyfrms.values())
    # Sort the list by the 'ts' key
    keyfrms = sorted(keyframe_list, key=lambda kf: kf['ts'])


    # #sorted keyframes 
    # keyfrms = {k: new_keyfrms[k] for k in sorted(new_keyfrms)}

    # print(keyfrms[1])

    keyfrms_tum = []
    keyfrm_points = []
    landmark_points = []
    rots = []
    transes = []

    ROT = []
    TRANS = []

    for keyfrm in keyfrms:

        # get conversion from camera to world
        trans_cw = np.matrix(keyfrm["trans_cw"]).T
        rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()

        # compute conversion from world to camera
        rot_wc = rot_cw.T
        trans_wc = - rot_wc * trans_cw
        keyfrm_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))
        keyfrms_tum.append((keyfrm["ts"], trans_wc.tolist(), R.from_matrix(rot_wc).as_quat().tolist()))

        rots.append(rot_wc)
        transes.append(trans_wc)
        

    keyfrm_points = np.array(keyfrm_points)




    last_keyframe = keyfrms[-1]
    # get conversion from camera to world
    trans_cw = np.matrix(keyfrm["trans_cw"]).T
    rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()
    rot_wc = rot_cw.T
    trans_wc = - rot_wc * trans_cw

    # print("Matrices: ", "trans_cw: ", trans_cw, "trans_wc: ", trans_wc, "rot_cw: ", rot_cw, "rot_wc: ", rot_wc, sep= "\n")




    # compute conversion from world to camera
    rot_wc = rot_cw.T



    # rotation_matrix = [[1,0,0],[0,-1,0],[0,0,-1]]
    # rnp = np.array(rotation_matrix)
    # keyfrm_points = np.dot(keyfrm_points,rnp)


    Y = keyfrm_points[:, 0]
    X = keyfrm_points[:, 2]
    Z = keyfrm_points[:, 1]

    f.close()
    # print(X, Y)
    # print(keyfrms[-1]['ts'])
    coordinates = np.array([int(X[-1]*100), int(Y[-1]*100)]).reshape((2, 1))

    # print("******     rot cw 30  ***********", rot_cw, sep="\n")


    r = np.array([rot_cw[0][0], rot_cw[0][2], rot_cw[2][0], rot_cw[2][2]]).reshape(2,2)

    # print("r: ", r)


    return coordinates, r
    # return 0, 0, rots[-1], transes[-1]


get_camera_location()

