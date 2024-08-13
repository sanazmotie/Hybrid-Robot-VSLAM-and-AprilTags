This project is maintained by [Nargess Seifi](https://github.com/Nargess-Seifi) and [Sanaz Motie](https://github.com/sanazmotie).

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

Once completed, the camera calibration will be ready for use.
