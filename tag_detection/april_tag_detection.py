import cv2
import math
import pickle
import asyncio
import numpy as np
import tag_location
import pupil_apriltags
import msg_to_location as loc
import esp_communication as esp
from pupil_apriltags import Detector
from scipy.spatial.transform import Rotation

#============================================================================
april_cm = 100.0   #convert tag transpose to cm
# A52
# focal = [253.43090116228416, 248.60296770187932]
# center = [337.27747302010226, 241.21048564436344]

#A73
focal = [258.01591950878856, 254.61961838592865]
center = [328.7437334131659, 234.27482836496304]


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
            for i in range(3):
                T[i] = int(T[i] * april_cm)
            relative_coordinates = np.array([T[2], T[0]]).reshape((2, 1))
            res.append([tag.tag_id, relative_coordinates, int(angles[1]), int(tag.center[0]), int(tag.center[1])])

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
def tag_is_valid(coordinates):
    d, x  = coordinates
    threshold =  0.68 * d - 2
    if d > 45 or d < 25 or abs(x) > threshold:
        return False
    return True

#============================================================================
async def main():
    vid = cv2.VideoCapture(1)

    while True:
        _ret, img = vid.read()
        if _ret:
            tags = get_tags(img)
            # if len(tags) > 0:
            if True:
                # print(loc.get_camera_location())
                camera_info = loc.get_camera_location()
                if camera_info:
                    # X_camera = co[0]
                    # Y_camera = co[1]
                    # X_camera = 0
                    # Y_camera = 0
                    rotation_matrix = camera_info[1]

                    for tag in tags:
                        await esp.send_two_values("MoveCar", 1, tag[1][1][0])
                        if not tag_is_valid(tag[1]):
                            print("ksetfgycdhjfgvuifhgdjfgxfkjnkuhvgv")
                            continue
                        tag_coordinates = tag_location.get_april_tag_location(tag[1], camera_info)

                        print("camera: ", camera_info[0], "\ntag relative: ", tag[1], "\ntag: ", tag_coordinates)

                        # cv2.putText(img,str(tag[0]),(tag[5],tag[6]-70),cv2.FONT_HERSHEY_COMPLEX,1,(240,100,255),1)
                        # cv2.circle(img,(tag[5],tag[6]),10,(240,165,255),3,5)
                        # if not tag[0] in seen_tags.keys():
                        #     # aprilTag coordinates, camera coordinates, aprirTag attributes
                        #     tag_coordinates = tag_location.get_april_tag_location(tag, X_camera, Y_camera)
                        #     # print(tag_coordinates, X_camera, Y_camera, tag[1], tag[2], tag[3])
                        #     seen_tags[tag[0]] = tag_coordinates
            
            cv2.imshow('img',img)
            key = cv2.waitKey(100)
            
            if key == ord('q'):
                break

        else:
            print("Frame not found !!")
            
    save_tag_locations()


if __name__ == "__main__":
    asyncio.run(main())

# test
# with open('/home/nargess/Documents/GitHub/VSLAM/seen_tags.pkl', 'rb') as f:
#     my_dict = pickle.load(f)

# print(my_dict)