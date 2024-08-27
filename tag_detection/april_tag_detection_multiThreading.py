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
from concurrent.futures import ThreadPoolExecutor

#============================================================================
april_cm = 100.0   # Convert tag transpose to cm

# Camera parameters
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
            r = Rotation.from_matrix(tag.pose_R)
            angles = r.as_euler("zyx", degrees=True)
            T = tag.pose_t.reshape((3)).tolist()
            for i in range(3):
                T[i] = int(T[i] * april_cm)
            relative_coordinates = np.array([T[2], T[0]]).reshape((2, 1))
            res.append([tag.tag_id, relative_coordinates, int(angles[1]), int(tag.center[0]), int(tag.center[1])])

    return res

#============================================================================

def save_tag_locations(pth='seen_tags.pkl'):
    with open(pth, 'wb') as f:
        pickle.dump(seen_tags, f)

#============================================================================
def tag_is_valid(coordinates):
    d, x = coordinates
    threshold = 0.68 * d - 2
    if d > 45 or d < 25 or abs(x) > threshold:
        return False
    return True

#============================================================================

def send_tag_updates_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_tag_updates())
    loop.close()


async def send_tag_updates():
    while True:
        await esp.send_two_values("MoveCar", 1, 2)
        await asyncio.sleep(0)  # Sleep for 10ms, adjust as necessary

#============================================================================
def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(send_tag_updates_loop)
        
        vid = cv2.VideoCapture(1)
        
        while True:
            _ret, img = vid.read()
            if _ret:
                tags = get_tags(img)
                if len(tags) > 0:
                    camera_info = loc.get_camera_location()
                    if camera_info:
                        for tag in tags:
                            if not tag_is_valid(tag[1]):
                                continue
                            tag_coordinates = tag_location.get_april_tag_location(tag[1], camera_info)
                            print("camera: ", camera_info[0], "\ntag relative: ", tag[1], "\ntag: ", tag_coordinates)

                cv2.imshow('img', img)
                key = cv2.waitKey(200)
                
                if key == ord('q'):
                    break
            else:
                print("Frame not found !!")
        
        save_tag_locations()

if __name__ == "__main__":
    main()
