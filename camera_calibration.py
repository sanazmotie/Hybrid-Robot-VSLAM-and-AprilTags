import cv2
import numpy as np

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
max_images = 15  # Stop after capturing 15 valid frames

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
    print(frame.shape)
    
    if cv2.waitKey(1) & 0xFF == ord('q') or captured_images >= max_images:
        print("Exiting loop...")
        break

cap.release()
cv2.destroyAllWindows()

if captured_images > 0:
    # Perform camera calibration
    print("Calibrating...")
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

    print("\nCalibration complete.")
    print("Camera Matrix : \n", camera_matrix)
    print("Distortion Coefficients : \n", dist_coeffs)
else:
    print("No valid images captured for calibration.")
