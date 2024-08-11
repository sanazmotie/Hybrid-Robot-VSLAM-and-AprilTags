import msgpack
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.linalg import inv
from scipy.spatial.transform import Rotation as R
import open3d as o3d

with open("/home/nargess/Documents/GitHub/VSLAM/SLAM/build/map.msg", "rb") as f:
    u = msgpack.Unpacker(f)
    msg = u.unpack()


keyfrms = msg["keyframes"]
landmarks = msg["landmarks"]

new_keyfrms = {}
for k in keyfrms.keys():
    new_keyfrms[int(k)] = keyfrms[k]

sorted_keyfrms = {k: new_keyfrms[k] for k in sorted(new_keyfrms)}


print("injaaaaaaaaaaaaaaaaaaaaaa\n", sorted_keyfrms.keys())

keyfrms = sorted_keyfrms.copy()


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

landmark_points = []
for lm in landmarks.values():
    landmark_points.append(lm["pos_w"])
landmark_points = np.array(landmark_points)

# keyfrms_tum.sort(key=lambda k: k[0])
# for keyfrm in keyfrms_tum:
#     print("{} {} {} {} {} {} {} {}".format(keyfrm[0], keyfrm[1][0][0], keyfrm[1][1][0], keyfrm[1][2][0], keyfrm[2][0], keyfrm[2][1], keyfrm[2][2], keyfrm[2][3]))


print("0 **********************************************************\n", keyfrm_points[:, 0])
print("1 **********************************************************\n", keyfrm_points[:, 1])
print("2 **********************************************************\n", keyfrm_points[:, 2])

rotation_matrix = [[1,0,0],[0,-1,0],[0,0,-1]]
rnp = np.array(rotation_matrix)
keyfrm_points = np.dot(keyfrm_points,rnp)
landmark_points = np.dot(landmark_points,rnp)


z = np.zeros(keyfrm_points[:, 1].shape)
# z = keyfrm_points[:, 1]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
# ax.plot(keyfrm_points[:, 0], z, keyfrm_points[:, 2], "o-", markersize=3)
ax.scatter3D(landmark_points[:, 0], landmark_points[:, 1], landmark_points[:, 2], s=1, c="r")
# plt.show()


num_points = keyfrm_points.shape[0]
colors = plt.cm.Blues(np.linspace(0, 1, num_points))  # Use 'Greys' colormap


ax.plot(
    keyfrm_points[0:1, 0], 
    [z[0]], 
    keyfrm_points[0:1, 2], 
    "x", 
    color="red", 
    markersize=8
)

# Plot each segment with a different color
for i in range(num_points - 1):
    ax.plot(
        keyfrm_points[i:i+2, 0], 
        [z[i], z[i+1]], 
        keyfrm_points[i:i+2, 2], 
        "o", 
        color=colors[i], 
        markersize=3
    )

plt.show()


# , keyfrm_points[:, 2]


pcd1 = o3d.geometry.PointCloud()
pcd1.points = o3d.utility.Vector3dVector(keyfrm_points)
colors1 = np.repeat(np.array([[0., 1., 0.]]), keyfrm_points.shape[0], axis=0)
pcd1.colors = o3d.utility.Vector3dVector(colors1)
pcd2 = o3d.geometry.PointCloud()
pcd2.points = o3d.utility.Vector3dVector(landmark_points)
colors2 = np.repeat(np.array([[1., 0., 0.]]), landmark_points.shape[0], axis=0)
pcd2.colors = o3d.utility.Vector3dVector(colors2)
o3d.visualization.draw_geometries([pcd1, pcd2, o3d.geometry.TriangleMesh.create_coordinate_frame()])
