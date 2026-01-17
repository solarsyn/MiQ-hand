import cv2
import numpy as np
import time
import os

# Config
CALIB_FILE = "miq_homography.npy"
BOARD_SIZE = (800, 800)
NUM_FRAMES = 15
CAM_INDEX = 0  # 0 = CSI camera; change to RTSP URL if using phone bridge

def calibrate_playfield():
    if os.path.exists(CALIB_FILE):
        print("Loaded existing calibration from", CALIB_FILE)
        return np.load(CALIB_FILE)

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print("Camera not found — check connection or CSI enable in raspi-config")
        return None

    print(f"Capturing {NUM_FRAMES} clean frames... Hold steady on empty board for ~15 seconds.")
    frames = []
    start = time.time()
    while time.time() - start < 15:
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        time.sleep(0.1)

    cap.release()

    if len(frames) < 8:
        print("Not enough frames captured")
        return None

    # Average to reduce noise/flicker
    avg = np.mean(frames, axis=0).astype(np.uint8)
    gray = cv2.cvtColor(avg, cv2.COLOR_BGR2GRAY)

    # Contrast enhancement (helps shadows, projector spill, wood grain)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    edges = cv2.Canny(blurred, 40, 120)

    # HoughCircles - tuned for dartboard rings
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.3, minDist=180,
                               param1=50, param2=30,
                               minRadius=150, maxRadius=450)

    if circles is None:
        print("No circles detected — try: lower param2 (25-30), higher dp (1.5), brighter light, or phone flash burst")
        return None

    circles = np.round(circles[0, :]).astype("int")
    # Pick largest as outer ring
    outer = max(circles, key=lambda c: c[2])
    cx, cy, cr = outer

    print(f"Outer ring detected: center ({cx}, {cy}), radius {cr} px")

    # Sample 8 perimeter points for better homography stability
    angles = np.linspace(0, 360, 8, endpoint=False)
    src_pts = np.array([
        [cx + cr * np.cos(np.deg2rad(a)), cy + cr * np.sin(np.deg2rad(a))] for a in angles
    ], dtype='float32')

    # Ideal top-down square
    margin = 40
    dst_pts = np.array([
        [margin, margin],
        [BOARD_SIZE[0] - margin, margin],
        [BOARD_SIZE[0] - margin, BOARD_SIZE[1] - margin],
        [margin, BOARD_SIZE[1] - margin]
    ], dtype='float32')

    H, status = cv2.findHomography(src_pts, dst_pts)
    if status is None or np.sum(status) < 3:
        print("Homography failed — points unstable or collinear")
        return None

    np.save(CALIB_FILE, H)
    print("Calibration saved to", CALIB_FILE)

    # Quick warp preview to confirm
    warped = cv2.warpPerspective(avg, H, BOARD_SIZE)
    cv2.imshow("Warped Playfield (check bullseye centering)", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return H

if __name__ == "__main__":
    calibrate_playfield()
