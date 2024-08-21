import cv2
import math
import pickle
import numpy as np
import tag_location
import pupil_apriltags
import msg_to_location as loc
from pupil_apriltags import Detector
from scipy.spatial.transform import Rotation

#============================================================================
april_cm = 100.0   #convert tag transpose to cm
# A52
# focal = [253.43090116228416, 248.60296770187932]
# center = [337.27747302010226, 241.21048564436344]

#A73
focal = [320.2204033062567, 231.2339953851215]
center = [249.55028318243194, 251.35081038684598]


at_detector = Detector(
    families="tag36h11",
    nthreads=4,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.8,
    debug=0,
)
#============================================================================
seen_tags = {}

#============================================================================

def get_tags(img):
    tags = at_detector.detect(
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
        estimate_tag_pose=True,
        camera_params=(focal[0], focal[1], center[0],center[1]),
        tag_size=0.094
    )

    res = []
    if len(tags) > 0:
        for tag in tags:
            r =  Rotation.from_matrix(tag.pose_R)
            angles = r.as_euler("zyx",degrees=True)
            T = tag.pose_t.reshape((3)).tolist()
            # T2[0][0], T2[2][0] = T2[2][0], T2[0][0]
            # for i in range(3):
            #     T[i] = int(T[i] * april_cm)
            res.append([tag.tag_id, T[0], T[1], T[2], int(angles[1]), int(tag.center[0]), int(tag.center[1])])

    return res

"""
tag:
0-id
1-x cm
2-y bala- paiin+ cm
3-fasele
4-rotation
5,6- xy vasat tasvir bar hasbe pixel
"""

#============================================================================

def save_tag_locations(pth = 'seen_tags.pkl'):
    with open(pth, 'wb') as f:
        pickle.dump(seen_tags, f)


#============================================================================

vid = cv2.VideoCapture(0)

while True:
    _ret, img = vid.read()
    if _ret:
        tags = get_tags(img)
        # if len(tags) > 0:
        if True:
            # print(loc.get_camera_location())
            co = loc.get_camera_location()
            if co:
                X_camera = co[0]
                Y_camera = co[1]
                # X_camera = 0
                # Y_camera = 0

                print(X_camera, Y_camera)
                


                # rot = co[2]
                # trans = co[3]

                for tag in tags:

                    print("*************************************************************************")
                #     # print(tag)


                    A = tag[3] + math.sqrt(X_camera**2 + Y_camera**2)
                    B = abs(tag[1])
                    C = math.sqrt(A**2 + B**2)
                    theta = math.atan(X_camera/Y_camera)
                    alpha = math.atan(B/A)
                    beta = 90 - alpha - theta
                    X_tag = C * math.sin(beta)
                    Y_tag = C * math.cos(beta)


                #     # Compute the tag position in the world coordinate system

                #     # print(T_world)
                #     # print("***************************")
                #     # tag_x = T_world[0, 0] * 100  # convert to cm
                #     # tag_y = T_world[2, 0] * 100

                #     # Convert to a list for easier readability
                #     # tag_position_world_list = tag_position_world.flatten().tolist()

                    print(X_tag, Y_tag, X_camera, Y_camera)
                    # print(tag[1:4], A, B, C, theta, alpha, beta, sep="\n")



                #     cv2.putText(img,str(tag[0]),(tag[5],tag[6]-70),cv2.FONT_HERSHEY_COMPLEX,1,(240,100,255),1)
                #     cv2.circle(img,(tag[5],tag[6]),10,(240,165,255),3,5)
                #     if not tag[0] in seen_tags.keys():
                #         # aprilTag coordinates, camera coordinates, aprirTag attributes
                #         tag_coordinates = tag_location.get_april_tag_location(tag, X_camera, Y_camera)
                #         # print(tag_coordinates, X_camera, Y_camera, tag[1], tag[2], tag[3])
                #         seen_tags[tag[0]] = tag_coordinates
        
        cv2.imshow('img',img)
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break

    else:
        print("Frame not found !!")
        
save_tag_locations()

# test
# with open('/home/nargess/Documents/GitHub/VSLAM/seen_tags.pkl', 'rb') as f:
#     my_dict = pickle.load(f)

# print(my_dict)