import cv2
import numpy as np
import yaml

# Define the chessboard size
chessboard_size = (9, 6)
frame_size = (640, 480)

# Termination criteria for corner sub-pixel refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all images
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane

cap = cv2.VideoCapture(0)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size[1])

captured_images = 0
max_images = 20  # Stop after capturing 15 valid frames

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)

        # Refine the corner positions
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(frame, chessboard_size, corners2, ret)
        captured_images += 1
        print(f"Captured {captured_images}/{max_images} images")

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(2000) & 0xFF == ord('q') or captured_images >= max_images:
        print("Exiting loop...")
        break

cap.release()
cv2.destroyAllWindows()

if captured_images > 0:
    # Perform camera calibration
    print("Calibrating...")
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

    print("here is the ret value: ", ret)

    print("\nCalibration complete.")
    # print("Camera Matrix : \n", camera_matrix)
    # print("Distortion Coefficients : \n", dist_coeffs)


    # Update the YAML configuration file
    config_data = {
        "Camera": {
            "name": "Nargess' Webcam",
            "setup": "monocular",
            "model": "perspective",
            "fx": float(camera_matrix[0, 0]),
            "fy": float(camera_matrix[1, 1]),
            "cx": float(camera_matrix[0, 2]),
            "cy": float(camera_matrix[1, 2]),
            "k1": float(dist_coeffs[0, 0]),
            "k2": float(dist_coeffs[0, 1]),
            "p1": float(dist_coeffs[0, 2]),
            "p2": float(dist_coeffs[0, 3]),
            "k3": float(dist_coeffs[0, 4]),
            "fps": 30.0,
            "cols": 640,
            "rows": 480,
            "color_order": "RGB"
        },
        "Preprocessing": {
            "min_size": 800
        },
        "Feature": {
            "name": "default ORB feature extraction setting",
            "scale_factor": 1.2,
            "num_levels": 8,
            "ini_fast_threshold": 20,
            "min_fast_threshold": 7
        },
        "Mapping": {
            "baseline_dist_thr_ratio": 0.02,
            "redundant_obs_ratio_thr": 0.9,
            "num_covisibilities_for_landmark_generation": 20,
            "num_covisibilities_for_landmark_fusion": 20
        },
        "PangolinViewer": {
            "keyframe_size": 0.05,
            "keyframe_line_width": 1,
            "graph_line_width": 1,
            "point_size": 2,
            "camera_size": 0.08,
            "camera_line_width": 3,
            "viewpoint_x": 0,
            "viewpoint_y": -0.9,
            "viewpoint_z": -1.9,
            "viewpoint_f": 400
        }
    }


    print(config_data)
    

    # Specify the path to the config YAML file
    config_file_path = "/home/nargess/Documents/GitHub/VSLAM/SLAM/A52S_wide_config_poshteBargh1.yaml"

    # Write the updated config data to the YAML file
    with open(config_file_path, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)

    print(f"Configuration file '{config_file_path}' updated successfully.")
else:
    print("No valid images captured for calibration.")
