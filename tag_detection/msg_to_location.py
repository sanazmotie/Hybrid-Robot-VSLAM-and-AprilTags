import msgpack
import numpy as np
from scipy.spatial.transform import Rotation as R


def get_current_location(msgPath = "/home/nargess/Documents/GitHub/VSLAM/SLAM/build/map.msg"):
    with open(msgPath, "rb") as f:
        u = msgpack.Unpacker(f)
        msg = u.unpack()

    raw_keyfrms = msg["keyframes"]
    new_keyfrms = {}
    for k in raw_keyfrms.keys():
        new_keyfrms[int(k)] = raw_keyfrms[k]

    #sorted keyframes 
    keyfrms = {k: new_keyfrms[k] for k in sorted(new_keyfrms)}

    keyfrms_tum = []
    keyfrm_points = []
    landmark_points = []
    for keyfrm in keyfrms.values():
        # get conversion from camera to world
        trans_cw = np.matrix(keyfrm["trans_cw"]).T
        rot_cw = R.from_quat(keyfrm["rot_cw"]).as_matrix()
        # compute conversion from world to camera
        rot_wc = rot_cw.T
        trans_wc = - rot_wc * trans_cw
        keyfrm_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))
        keyfrms_tum.append((keyfrm["ts"], trans_wc.tolist(), R.from_matrix(rot_wc).as_quat().tolist()))
    keyfrm_points = np.array(keyfrm_points)

    X = keyfrm_points[:, 0]
    Y = keyfrm_points[:, 2]

    return X[-1], Y[-1]
