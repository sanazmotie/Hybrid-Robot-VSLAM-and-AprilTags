This project is maintained by [Nargess Seifi](https://github.com/Nargess-Seifi) and [Sanaz Motie](https://github.com/sanazmotie).

## Overview

**april_tag_detection.py:** Detects AprilTags in video frames and calculates their position and orientation relative to the camera. The detected tags' information is displayed on the video stream, and the locations of newly detected tags are stored in a dictionary.

**msg_to_location.py:** Extracts the camera's position from a .msg file, which contains SLAM data. The camera's X and Y coordinates are returned in centimeters.

**tag_location.py:** Computes the global location of an AprilTag based on its position relative to the camera and the camera's coordinates.

## Camera Calibration

To calibrate the camera, follow these steps:

1. **Update camera_calibration.py:**
   - Change the path to the target configuration file in the code. (config_file_path)
   - Set your camera number appropriately in the code. (cv2.VideoCapture(0))

2. **Run the Calibration Script:**
   - Execute the script.

3. **Capture Chessboard Images:**
   - Position the camera to capture fifteen frames of the chessboard (9*6) from different angles.
   - The camera captures a frame every 3 seconds.
4. **update april_tag_detection.py**
   - Update the focal and center variables according to the values provided in the configuration file generated from the calibration process.

Once completed, the camera calibration will be ready for use.

## Acknowledgements

This project includes code modified from [Ujwal Nandanwar](https://github.com/un0038998)'s original work.
